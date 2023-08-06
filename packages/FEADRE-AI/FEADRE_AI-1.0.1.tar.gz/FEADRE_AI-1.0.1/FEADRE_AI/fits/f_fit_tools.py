import datetime
import json
import math
import os
import tempfile
import time
from collections import deque

import cv2
import numpy as np
import torch
import torch.nn as nn
from pycocotools.cocoeval import COCOeval
from torch.cuda.amp import GradScaler, autocast
from tqdm import tqdm

from tools.GLOBAL_LOG import flog
from tools.boxes.f_boxes import ltrb2ltwh
from tools.fits.fcocoeval import FCOCOeval
from tools.picture.f_show import f_show_od_np4plt_v3


class FModelBase(nn.Module):
    def __init__(self, net, losser, preder):
        super(FModelBase, self).__init__()
        self.net = net
        self.losser = losser
        self.preder = preder

    def forward(self, datas_batch):
        imgs_ts_4d, targets = datas_batch
        outs = self.net(imgs_ts_4d)

        ''' 多尺度图片归一化支持 '''
        device = imgs_ts_4d.device
        batch, c, h, w = imgs_ts_4d.shape
        toones_wh_ts_input = []
        if targets is not None and 'toone' in targets[0]:  # 多尺度归一
            for target in targets:
                toones_wh_ts_input.append(torch.tensor(target['toone'], device=device))
            toones_wh_ts_input = torch.stack(toones_wh_ts_input, 0)
        else:
            toones_wh_ts_input = torch.empty(batch, 2, device=device, dtype=torch.float)  # 实际为准
            toones_wh_ts_input[:, :] = torch.tensor(imgs_ts_4d.shape[2:4][::-1], device=device)

        if self.training:
            if targets is None:
                raise ValueError("In training mode, targets should be passed")
            loss_total, log_dict = self.losser(outs, targets, imgs_ts_4d, toones_wh_ts_input)
            '''------ 验证 loss 由FitExecutor 处理 ------'''

            return loss_total, log_dict
        else:
            with torch.no_grad():  # 这个没用
                # outs模型输出  返回 ids_batch, p_boxes_ltrb, p_keypoints, p_labels, p_scores
                reses = self.preder(outs, imgs_ts_4d, targets, toones_wh_ts_input)

            return reses, imgs_ts_4d, targets, toones_wh_ts_input


class FitExecutor():
    def __init__(self, cfg, model, fun_loss, save_weight_name, path_save_weight,
                 optimizer=None, dataloader_train=None, lr_scheduler=None,
                 end_epoch=None, is_mixture_fit=True, lr_val_base=1e-3,
                 is_writer=False,
                 num_save_interval=10, print_freq=10,
                 dataloader_val=None,
                 dataloader_test=None, maps_def_max=None,
                 num_vis_z=None, mode_vis=None,
                 ) -> None:
        '''

        :param model:
        :param fun_loss: 回调 loss 处理
        :param save_weight_name:
        :param path_save_weight:
        :param optimizer:
        :param dataloader_train:
        :param lr_scheduler:
        :param end_epoch:
        :param is_mixture_fit:
        :param lr_val_base:
        :param is_writer:
        :param num_save_interval:
        :param print_freq:
        :param dataloader_val:
        :param dataloader_test:
        '''
        super().__init__()
        self.dataloader_train = dataloader_train
        self.model = model
        self.optimizer = optimizer
        self.lr_scheduler = lr_scheduler
        self.end_epoch = end_epoch
        self.is_mixture_fit = is_mixture_fit
        self.lr_val_base = lr_val_base

        self.fun_loss = fun_loss
        self.cfg = cfg

        # 测试属性
        self.dataloader_test = dataloader_test
        self.num_vis_z = num_vis_z
        self.mode_vis = mode_vis  # 'keypoints','bbox'
        self.maps_def_max = maps_def_max

        # 验证
        self.dataloader_val = dataloader_val

        assert os.path.exists(path_save_weight), 'path_save_weight 不存在 %s' % path_save_weight
        self.save_weight_name = save_weight_name
        self.path_save_weight = path_save_weight
        self.num_save_interval = num_save_interval
        self.print_freq = print_freq

        if is_writer:

            from torch.utils.tensorboard import SummaryWriter
            c_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
            _path = os.path.join(path_save_weight, c_time)

            flog.debug('---- use tensorboard --- %s', _path)
            os.makedirs(_path, exist_ok=True)
            self.tb_writer = SummaryWriter(_path)
        else:
            self.tb_writer = None

    def frun(self, start_epoch):
        for epoch in range(start_epoch, self.end_epoch + 1, 1):  # 从1开始
            save_val = None
            ''' ------------------- 训练代码  --------------------- '''
            if self.dataloader_train is not None and self.cfg.IS_TRAIN:
                t0_test = time.time()
                loss_val_obj = self.ftrain(dataloader_train=self.dataloader_train,
                                           optimizer=self.optimizer,
                                           epoch=epoch, end_epoch=self.end_epoch,
                                           fun_loss=self.fun_loss, model=self.model,
                                           lr_val_base=self.lr_val_base, tb_writer=self.tb_writer,
                                           is_mixture_fit=self.is_mixture_fit, print_freq=self.print_freq)
                save_val = loss_val_obj.avg

                print(' ----- 训练用时 %s ----- ' % str(datetime.timedelta(seconds=int(time.time() - t0_test))))

            if save_val is not None \
                    and self.dataloader_train is not None \
                    and (epoch % self.num_save_interval) == 0:
                print('训练完成正在保存模型...')
                save_weight(
                    path_save=self.path_save_weight,
                    model=self.model,
                    name=self.save_weight_name,
                    loss=save_val,  # 这个正常是一样的有的
                    optimizer=self.optimizer,
                    lr_scheduler=self.lr_scheduler,
                    epoch=epoch)

            ''' ------------------- 验证代码  --------------------- '''
            if self.dataloader_val is not None and self.cfg.IS_VAL and self.is_open(epoch, self.cfg.NUMS_VAL_DICT):
                t0_test = time.time()
                loss_val_obj = self.fval(dataloader_val=self.dataloader_val,
                                         epoch=epoch, end_epoch=self.end_epoch,
                                         fun_loss=self.fun_loss, model=self.model,
                                         tb_writer=self.tb_writer, print_freq=self.print_freq
                                         )
                print(' ----- 验证用时 %s ----- ' % str(datetime.timedelta(seconds=int(time.time() - t0_test))))

            ''' ------------------- 测试代码  --------------------- '''
            if self.dataloader_test is not None and self.cfg.IS_TEST and self.is_open(epoch, self.cfg.NUMS_TEST_DICT):
                t0_test = time.time()
                maps_val = self.ftest(model=self.model, dataloader_test=self.dataloader_test,
                                      epoch=epoch, is_vis_all=self.cfg.IS_VISUAL, mode_vis=self.mode_vis,
                                      num_vis_z=self.num_vis_z, tb_writer=None, )

                if maps_val is not None and self.maps_def_max is not None:
                    # 更新 self.maps_def_max 值
                    if maps_val[0] > self.maps_def_max[0]:
                        self.maps_def_max[0] = maps_val[0]
                        self.maps_def_max[1] = max(self.maps_def_max[1], maps_val[1])
                    elif maps_val[1] > self.maps_def_max[1]:
                        self.maps_def_max[0] = max(self.maps_def_max[0], maps_val[0])
                        self.maps_def_max[1] = maps_val[1]
                    else:
                        continue
                    save_weight(
                        path_save=self.path_save_weight,
                        model=self.model,
                        name=self.save_weight_name,
                        loss=save_val,  # 这个正常是一样的有的
                        optimizer=self.optimizer,
                        lr_scheduler=self.lr_scheduler,
                        epoch=epoch,
                        maps_val=self.maps_def_max,
                    )
                print(' ----- 测试用时 %s ----- ' % str(datetime.timedelta(seconds=int(time.time() - t0_test))))

    def fval(self, dataloader_val, epoch, end_epoch,
             model=None, fun_loss=None,
             print_freq=1, tb_writer=None,
             ):
        # 这个在 epoch 中
        loss_val_obj = SmoothedValue()
        print('\n-------------------- 验证 fval 开始 %s -------------------------' % epoch)
        epoch_size = len(dataloader_val)
        batch = dataloader_val.batch_size

        t0 = time.time()
        for i, datas_batch in enumerate(dataloader_val):
            t1 = time.time()

            with torch.no_grad():
                if fun_loss is not None:
                    # 这里是回调
                    loss_total, log_dict = fun_loss(datas_batch)
                else:
                    loss_total, log_dict = model(datas_batch)

            loss_val_obj.update(loss_total.item())

            if i % (print_freq * batch) == 0:
                self.print_log(end_epoch=end_epoch, epoch=epoch,
                               epoch_size=epoch_size, iter_i=i,
                               log_dict=log_dict, loss_val=loss_val_obj.avg,
                               t0=t0, t1=t1, title='val')

            if tb_writer is not None:
                self.tb_writing4train_val(tb_writer=tb_writer, log_dict=log_dict,
                                          epoch=epoch, epoch_size=epoch_size, iter_i=i, lr=None)

            # 更新时间用于获取 data 时间
            t0 = time.time()

        return loss_val_obj

    def ftrain(self, dataloader_train, optimizer, epoch, end_epoch,
               fun_loss=None, model=None,
               lr_val_base=1e-3, tb_writer=None,
               is_mixture_fit=False, print_freq=1):
        # 这个在 epoch 中
        loss_val_obj = SmoothedValue()
        print('-------------------- 训练 ftrain 开始 %s -------------------------' % epoch)
        epoch_size = len(dataloader_train)
        batch = dataloader_train.batch_size
        scaler = GradScaler(enabled=is_mixture_fit)

        t0 = time.time()
        for i, datas_batch in enumerate(dataloader_train):
            t1 = time.time()

            if epoch < 2:
                now_lr = lr_val_base * pow((i + epoch * epoch_size) * 1. / (1 * epoch_size), 4)
                self.update_lr(optimizer, now_lr)
            elif epoch == 1:
                self.update_lr(optimizer, lr_val_base)

            with autocast(enabled=is_mixture_fit):
                if fun_loss is not None:
                    # 这里是回调
                    loss_total, log_dict = fun_loss(datas_batch)
                else:
                    loss_total, log_dict = model(datas_batch)

            loss_val_obj.update(loss_total.item())

            scaler.scale(loss_total).backward()
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()

            if i % (print_freq * batch) == 0:
                self.print_log(end_epoch=end_epoch, epoch=epoch,
                               epoch_size=epoch_size, iter_i=i,
                               log_dict=log_dict, loss_val=loss_val_obj.avg,
                               lr=optimizer.param_groups[0]['lr'],
                               t0=t0, t1=t1, title='train')

            if tb_writer is not None:
                self.tb_writing4train_val(tb_writer=tb_writer, log_dict=log_dict,
                                          epoch=epoch, epoch_size=epoch_size, iter_i=i,
                                          lr=optimizer.param_groups[0]['lr'])

            # 更新时间用于获取 data 时间
            t0 = time.time()

        return loss_val_obj

    def ftest(self, model, dataloader_test, epoch, is_vis_all, mode_vis, num_vis_z, tb_writer=None):
        '''
        ['segm', 'bbox', 'keypoints']
        :param epoch:
        :return:
        '''
        print('-------------------- 测试 ftest 开始 %s -------------------------' % epoch)
        model.eval()

        num_no_pos_z = 0  # 没发现目标的计数器
        res_z = {}  # 保存 全部的coco结果
        num_vis_now = 0  # 已可视化的临时值
        ids_data_all = []  # dataloader_test 的所有图片ID

        # with torch.no_grad() 这个由模型处理
        pbar = tqdm(dataloader_test, desc='%s' % epoch, postfix=dict, mininterval=0.1)
        for datas_batch in pbar:
            # 由模型 FModelBase 处理数据后输出
            reses, imgs_ts_4d, targets, toones_wh_ts_input = model(datas_batch)
            # 这里输出的都是归一化尺寸
            ids_batch, p_ltrbs, p_kps, p_labels, p_scores = reses

            ''' 整批没有目标 提示和处理 '''
            if p_labels is None or len(p_labels) == 0:
                num_no_pos_z += len(dataloader_test)
                flog.info('本批没有目标 当前共有: %s 张图片未检出', num_no_pos_z)
                # if num_no_pos > 3:  # 如果3个批都没有目标则放弃
                #     return
                # else:  # 没有目标就下一个
                #     num_no_pos += 1
                pbar.set_description("未检出数: %s" % num_no_pos_z)
                continue

            ''' 有目标进行如下操作 提取该批真实ID及尺寸 '''
            size_f_batch = []  # 用于修复box
            ids_img_batch = []
            for target in targets:  # 通过target 提取ID 和 size
                ids_data_all.append(target['image_id'])
                ids_img_batch.append(target['image_id'])
                size_f_batch.append(target['size'].clone().detach())  # tnesor

            _res_batch = {}  # 每一批的coco 结果 临时值

            # 每一张图的 id 与批次顺序保持一致 选出匹配
            for i, (size, image_id) in enumerate(zip(size_f_batch, ids_img_batch)):
                # 图片与 输出的对应
                mask = ids_batch == i  # 构建 batch 次的mask
                ''' 单张图没有目标 计数提示 '''
                if not torch.any(mask):
                    # flog.warning('没有预测出框 %s', files_txt)
                    num_no_pos_z += 1
                    pbar.set_description("未检出数: %s" % num_no_pos_z)
                else:
                    ''' 已检出 是否可视化逻辑 '''
                    if is_vis_all or num_vis_now < num_vis_z:
                        num_vis_now += 1
                        # 多尺度处理逻辑
                        if 'toone' in targets[i]:
                            size_wh_toone_ts_x2 = targets[i]['toone'].repeat(2)  # input尺寸
                        else:
                            size_wh_toone_ts_x2 = torch.tensor(imgs_ts_4d.shape[-2:][::-1]).repeat(2)  # 实际为准
                        self.show_pic(dataloader_test=dataloader_test,
                                      size_wh_toone_ts_x2=size_wh_toone_ts_x2,
                                      target=targets[i], image_id=image_id, mode_vis=mode_vis,
                                      p_labels_pos=p_labels[mask],
                                      p_ltrbs_pos=p_ltrbs[mask], p_scores_pos=p_scores[mask])

                    # 归一化->file尺寸  coco需要 ltwh
                    boxes_ltwh = ltrb2ltwh(p_ltrbs[mask] * size.repeat(2)[None])
                    _res_batch[image_id] = {
                        'boxes': boxes_ltwh,  # coco loadRes 会对ltwh 转换成 ltrb
                        'labels': p_labels[mask],
                        'scores': p_scores[mask],
                    }
                    # 更新进度条值
                    d = {
                        'pos': len(boxes_ltwh),  # 框个数
                        'max': round(p_scores[mask].max().item() * 100, 1),  # 分数
                        # 'min': round(p_scores.min().item(), 1),
                        'mean': round(p_scores[mask].mean().item() * 100, 1),
                    }
                    pbar.set_postfix(**d)

            if len(_res_batch) > 0:  # 有检测出的目标
                res_z.update(_res_batch)  # 字典叠加

        res_coco_standard = []  # 最终的 coco 标准格式 一个ID可能 有多个目标
        # res_z 每一个ID可能有多个目标 每个目标形成一条 id对应数据
        for i, (image_id, g_target) in enumerate(res_z.items()):
            labels = g_target['labels'].type(torch.int).tolist()
            boxes_ltwh = g_target['boxes'].tolist()
            score = g_target['scores'].tolist()
            for i in range(len(labels)):
                # catid转换
                category_id = dataloader_test.dataset.classes_train2coco[labels[i]]
                res_coco_standard.append(
                    {"image_id": image_id, "category_id": category_id, "bbox": boxes_ltwh[i], "score": score[i]})

        if len(res_coco_standard) > 0:  # 有 coco 结果
            # 这个保存 AP50的结果
            maps_val = self.run_cocoeval(dataloader_test=dataloader_test, epoch=epoch,
                                         ids_data_all=ids_data_all,
                                         num_no_pos_z=num_no_pos_z,
                                         res_coco_standard=res_coco_standard,
                                         tb_writer=tb_writer)

        else:
            # 没有 coco 结果
            if tb_writer is not None:
                self.tr_writing4test(epoch=epoch, num_no_pos_z=num_no_pos_z,
                                     tb_writer=tb_writer, coco_eval_obj=None)
            maps_val = [0, 0]

        return maps_val

    def print_log(self, end_epoch, epoch,
                  epoch_size, iter_i, log_dict, loss_val,
                  t0, t1, lr=math.nan, title='title', ):
        '''

        :param end_epoch:
        :param epoch:
        :param epoch_size: 一个 epoch 需迭代的次数
        :param iter_i:  当前迭代次数
        :param log_dict:
        :param loss_val:
        :param lr: 当前学习率
        :param t0: 最开始的时间 这个是秒
        :param t1:  数据加载完成时间
        :param title:  标题
        :return:
        '''
        show_loss_str = []
        for k, v, in log_dict.items():
            show_loss_str.append(
                "{}: {:.4f} ||".format(k, v)
            )

        iter_time = time.time() - t0
        residue_time = iter_time * (epoch_size - iter_i + 1)  # 剩余时间

        d = {
            'title': title,
            'epoch': epoch,
            'end_epoch': end_epoch,
            'iter_i': iter_i + 1,
            'iter_epoch': epoch_size,
            'iter_z': (epoch - 1) * epoch_size + iter_i + 1,
            'lr': lr,
            'loss': loss_val,
            'loss_str': str(show_loss_str),
            'data_time': t1 - t0,
            'iter_time': iter_time,
            'residue_time': str(datetime.timedelta(seconds=int(residue_time))),
        }

        s = '[{title} {epoch}/{end_epoch}] ' \
            '[Iter {iter_i}/{iter_epoch}/{iter_z}] ' \
            '[lr: {lr:.6f}] [Loss: {loss:.2f} || {loss_str}] ' \
            '[time: {data_time:.2f}/{iter_time:.2f}/{residue_time}]'

        print(s.format(**d), flush=True)

    def update_lr(self, optimizer, now_lr):
        for param_group in optimizer.param_groups:
            param_group['lr'] = now_lr

    def is_open(self, epoch, nums_dict):
        '''
        是否开启 验证或测试
        :param epoch:
        :param nums_dict: NUMS_TEST_DICT = {2: 1, 35: 1, 50: 1}
        :return:
        '''

        #  {2: 1, 35: 1, 50: 1}  -> 2,35,50 ->  50,35,2
        s_keys = sorted(list(nums_dict), reverse=True)
        for s_key in s_keys:
            if epoch < s_key:
                continue
            else:
                eval_interval = nums_dict[s_key]
                if epoch % eval_interval != 0:
                    # 满足epoch 无需验证退出
                    break
                return True

    def run_cocoeval(self, dataloader_test, epoch, ids_data_all, num_no_pos_z, res_coco_standard, tb_writer):
        maps_val = []
        coco_gt = dataloader_test.dataset.coco_obj
        # 第一个元素指示操作该临时文件的安全级别，第二个元素指示该临时文件的路径
        _, tmp = tempfile.mkstemp()  # 创建临时文件
        json.dump(res_coco_standard, open(tmp, 'w'))
        coco_dt = coco_gt.loadRes(tmp)
        '''
                    _summarizeDets()->_summarize() 
                        _summarizeDets 函数中调用了12次 _summarize
                        结果在 self.eval['precision'] , self.eval['recall']中 
                    '''
        coco_eval_obj = FCOCOeval(coco_gt, coco_dt, 'bbox')  # 这个添加了每个类别的map分
        # coco_eval_obj = COCOeval(coco_gt, coco_dt, ann_type)
        coco_eval_obj.params.imgIds = ids_data_all  # 多显卡id合并更新
        coco_eval_obj.evaluate()
        coco_eval_obj.accumulate()
        coco_stats, print_coco = coco_eval_obj.summarize()
        print(print_coco)
        clses_name = list(dataloader_test.dataset.classes_ids)
        coco_eval_obj.print_clses(clses_name)
        maps_val.append(coco_eval_obj.stats[1])  # 添加ap50
        maps_val.append(coco_eval_obj.stats[7])
        if tb_writer is not None:
            # Precision_iou
            self.tr_writing4test(epoch=epoch, num_no_pos_z=num_no_pos_z,
                                 tb_writer=tb_writer, coco_eval_obj=coco_eval_obj)
        return maps_val

    def tr_writing4test(self, epoch, num_no_pos_z, tb_writer, coco_eval_obj=None):
        if coco_eval_obj is not None:
            _d = {
                'IoU=0.50:0.95': coco_eval_obj.stats[0],
                'IoU=0.50': coco_eval_obj.stats[1],
                'IoU=0.75': coco_eval_obj.stats[2],
            }
            tb_writer.add_scalars('mAP/Precision_iou', _d, epoch + 1)
            # Recall_iou
            _d = {
                'maxDets=  1': coco_eval_obj.stats[6],
                'maxDets= 10': coco_eval_obj.stats[7],
                'maxDets=100': coco_eval_obj.stats[8],
            }
            tb_writer.add_scalars('mAP/Recall_iou', _d, epoch + 1)
            # 小中大
            _d = {
                'p_large': coco_eval_obj.stats[5],
                'r_large': coco_eval_obj.stats[11],
            }
            tb_writer.add_scalars('mAP/large', _d, epoch + 1)
            _d = {
                'p_medium': coco_eval_obj.stats[4],
                'r_medium': coco_eval_obj.stats[10],
            }
            tb_writer.add_scalars('mAP/medium', _d, epoch + 1)
            _d = {
                'p_small': coco_eval_obj.stats[3],
                'r_small': coco_eval_obj.stats[9],
            }
            tb_writer.add_scalars('mAP/small', _d, epoch + 1)
        # 一个图只有一个值
        tb_writer.add_scalar('mAP/num_no_pos', num_no_pos_z, epoch + 1)  # 未检出的图片数

    def tb_writing4train_val(self, tb_writer, epoch, epoch_size, iter_i, log_dict, lr=None):
        # 主进程写入   不验证时写
        iter = epoch_size * (epoch - 1) + iter_i + 1
        for k, v, in log_dict.items():
            tb_writer.add_scalar('loss_iter/%s' % k, v, iter)
        if lr is not None:
            tb_writer.add_scalar('loss_iter/lr', lr, iter)

    def show_pic(self, dataloader_test, size_wh_toone_ts_x2,
                 target, image_id, mode_vis,
                 p_labels_pos, p_ltrbs_pos, p_scores_pos):

        coco = dataloader_test.dataset.coco_obj
        img_info = coco.loadImgs([image_id])
        file_img = os.path.join(dataloader_test.dataset.path_img, img_info[0]['file_name'])
        img_np_file = cv2.imread(file_img)
        img_np_file = cv2.cvtColor(img_np_file, cv2.COLOR_BGR2RGB)
        # import skimage.io as io
        # h,w,c
        # img_np = io.imread(file_img)
        size_wh_file = np.array(img_np_file.shape[:2][::-1])
        size_wh_file_x2 = np.tile(size_wh_file, 2)  # 图片真实尺寸
        p_boxes_ltrb_f = p_ltrbs_pos.cpu() * size_wh_file_x2

        g_texts = []
        for i, p_label in enumerate(p_labels_pos):
            name_cat = dataloader_test.dataset.ids_classes[(p_label.long() + 1).item()]
            s = name_cat + ':' + str(p_scores_pos[i].cpu().item())
            g_texts.append(s)

        if mode_vis == 'bbox':  # 单人脸
            f_show_od_np4plt_v3(
                img_np_file, p_ltrb=p_boxes_ltrb_f,
                g_ltrb=target['boxes'].cpu() / size_wh_toone_ts_x2 * size_wh_file_x2,
                g_texts=g_texts,
                is_recover_size=False,
            )
        elif mode_vis == 'keypoints':
            size_wh_file_x5 = np.tile(size_wh_file, self.cfg.NUM_KEYPOINTS)  # 图片真实尺寸
            raise Exception('待完善 keypoints')
            # p_keypoints_f = p_kps_pos.cpu() * size_wh_file_x5
            # f_show_kp_np4plt(img_np_file, p_boxes_ltrb_f,
            #                  kps_xy_input=p_keypoints_f,
            #                  mask_kps=torch.ones_like(p_keypoints_f, dtype=torch.bool),
            #                  # 测试集 GT默认不归一化,是input模型尺寸
            #                  g_ltrb=target['boxes'].cpu() / size_wh_toone_ts_x2 * size_wh_file_x2,
            #                  plabels_text=p_labels_pos,
            #                  p_scores_float=p_scores_pos.tolist(),
            #                  is_recover_size=False)
        else:
            raise Exception('self.cfg.MODE_VIS = %s 错误' % self.cfg.MODE_VIS)


class SmoothedValue(object):
    """
    记录一系列统计量
    Track a series of values and provide access to smoothed values over a
    window or the global series average.
    """

    def __init__(self, window_size=20, fmt=None):
        if fmt is None:
            fmt = "{median:.4f} ({global_avg:.4f})"
        self.deque = deque(maxlen=window_size)  # deque简单理解成加强版list
        self.total = 0.0
        self.count = 0
        self.fmt = fmt

    def update(self, value, n=1):
        self.deque.append(value)
        self.count += n
        self.total += value * n

    # def synchronize_between_processes(self):
    #     """
    #     Warning: does not synchronize the deque!
    #     """
    #     if not fis_mgpu():
    #         return
    #     t = torch.tensor([self.count, self.total], dtype=torch.float64, device="cuda")
    #     dist.barrier()
    #     dist.all_reduce(t)
    #     t = t.tolist()
    #     self.count = int(t[0])
    #     self.total = t[1]

    @property
    def median(self):  # @property 是装饰器，这里可简单理解为增加median属性(只读)
        d = torch.tensor(list(self.deque))
        return d.median().item()

    @property
    def avg(self):
        d = torch.tensor(list(self.deque), dtype=torch.float32)
        return d.mean().item()

    @property
    def global_avg(self):
        return self.total / self.count

    @property
    def max(self):
        return max(self.deque)

    @property
    def value(self):
        return self.deque[-1]

    def __str__(self):
        return self.fmt.format(
            median=self.median,
            avg=self.avg,
            global_avg=self.global_avg,
            max=self.max,
            value=self.value)


def save_weight(path_save, model, name, loss=None, optimizer=None, lr_scheduler=None, epoch=0, maps_val=None):
    if path_save and os.path.exists(path_save):
        sava_dict = {
            'model': model.state_dict(),
            'optimizer': optimizer.state_dict() if optimizer else None,
            'lr_scheduler': lr_scheduler.state_dict() if lr_scheduler else None,
            'epoch': epoch}
        if maps_val is not None:
            if loss is not None:
                l = round(loss, 2)
            else:
                l = ''
            file_weight = os.path.join(path_save, (name + '-{}_{}_{}_{}.pth')
                                       .format(epoch + 1,
                                               l,
                                               'p' + str(round(maps_val[0] * 100, 1)),
                                               'r' + str(round(maps_val[1] * 100, 1)),
                                               ))
        else:
            file_weight = os.path.join(path_save, (name + '-{}_{}.pth').format(epoch, round(loss, 3)))
        torch.save(sava_dict, file_weight)
        flog.info('保存成功 %s', file_weight)


def load_weight(file_weight, model, optimizer=None, lr_scheduler=None,
                device=torch.device('cpu'), is_mgpu=False, ffun=None):
    start_epoch = 1
    if file_weight and os.path.exists(file_weight):
        checkpoint = torch.load(file_weight, map_location=device)

        '''对多gpu的k进行修复'''
        # if 'model' in checkpoint:
        #     pretrained_dict_y = checkpoint['model']
        # else:
        #     pretrained_dict_y = checkpoint

        ''' debug '''
        # if ffun is not None:
        #     pretrained_dict = ffun(pretrained_dict_y)
        # else:
        #     pretrained_dict = pretrained_dict_y

        dd = {}

        # # 多GPU处理
        # ss = 'module.'
        # for k, v in pretrained_dict.items():
        #     if is_mgpu:
        #         if ss not in k:
        #             dd[ss + k] = v
        #         else:
        #             dd = pretrained_dict_y
        #             break
        #             # dd[k] = v
        #     else:
        #         dd[k.replace(ss, '')] = v

        '''重组权重'''
        # load_weights_dict = {k: v for k, v in weights_dict.items()
        #                      if model.state_dict()[k].numel() == v.numel()}

        keys_missing, keys_unexpected = model.load_state_dict(dd, strict=False)
        if len(keys_missing) > 0 or len(keys_unexpected):
            flog.error('missing_keys %s', keys_missing)  # 这个是 model 的属性
            flog.error('unexpected_keys %s', keys_unexpected)  # 这个是 pth 的属性
        if optimizer:
            optimizer.load_state_dict(checkpoint['optimizer'])
        if lr_scheduler and checkpoint['lr_scheduler']:
            lr_scheduler.load_state_dict(checkpoint['lr_scheduler'])

        if 'epoch' in checkpoint:
            start_epoch = checkpoint['epoch']
        else:
            start_epoch = 1

        flog.warning('已加载 feadre 权重文件为 %s', file_weight)
    return start_epoch
