import torch
import torch.nn.functional as F
import numpy as np

from tools.datas.dataset_coco import CustomCocoDataset


class CLS4collate_fn:
    # fdatas_l1
    def __init__(self, is_multi_scale):
        self.is_multi_scale = is_multi_scale

    def __call__(self, batch_datas):
        '''
        在这里重写collate_fn函数
        batch_datas: tuple[[tensor_img,dict_targets],...,[tensor_img,dict_targets]]
        '''
        # 训练才进这里
        if self.is_multi_scale:
            batch = len(batch_datas)
            imgs_list = []
            targets_list = []
            # 打开 tuple 数据
            for i, (img_ts, target) in enumerate(batch_datas):
                # flog.warning('fun4dataloader测试  %s %s %s ', target, len(target['boxes']), len(target['labels']))
                imgs_list.append(img_ts)
                targets_list.append(target)

            pad_imgs_list = []

            # 这里的最大一定能被32整除
            h_list = [int(s.shape[1]) for s in imgs_list]
            w_list = [int(s.shape[2]) for s in imgs_list]
            max_h = np.array(h_list).max()
            max_w = np.array(w_list).max()
            # self.cfg.tcfg_batch_size = [max_w, max_h] # 这样用多进程要报错
            for i in range(batch):
                img_ts = imgs_list[i]
                # 右下角添加 target 无需处理
                img_ts_pad = F.pad(img_ts, (0, int(max_w - img_ts.shape[2]), 0, int(max_h - img_ts.shape[1])), value=0.)
                pad_imgs_list.append(img_ts_pad)

                # debug 代码
                # fshow_pic_ts4plt(pad_img)  # 可视化 前面不要归一化
                # fshow_kp_ts4plt(pad_img,
                #                 targets_list[i]['boxes'],
                #                 targets_list[i]['keypoints'],
                #                 mask_kps=targets_list[i]['kps_mask'],
                #                 is_recover_size=False
                #                 )  # 可视化
                # f_show_od_ts4plt(img_ts_pad, targets_list[i]['boxes'], is_recover_size=False)
                # print('多尺度%s ' % str(pad_img.shape))

            imgs_ts_4d = torch.stack(pad_imgs_list)
        else:
            imgs_ts_3d = batch_datas[0][0]
            # 包装整个图片数据集 (batch,3,416,416) 转换到显卡
            imgs_ts_4d = torch.empty((len(batch_datas), *imgs_ts_3d.shape)).to(imgs_ts_3d)
            targets_list = []
            for i, (img, target) in enumerate(batch_datas):
                # flog.warning('fun4dataloader测试  %s %s %s ', target, len(target['boxes']), len(target['labels']))
                imgs_ts_4d[i] = img
                targets_list.append(target)
        return imgs_ts_4d, targets_list


def cre_dataloader(path_img_train=None, file_json_train=None, transform_train=None, mode_train=None, batch_train=None,
                   path_img_val=None, file_json_val=None, transform_val=None, mode_val=None, batch_val=None,
                   path_img_test=None, file_json_test=None, transform_test=None, mode_test=None, batch_test=None,
                   is_multi_scale=False, num_workers=None,
                   ):
    dataloader_train, dataloader_val, dataloader_test = None, None, None
    if file_json_train is not None:
        dataloader_train = _cre_data_load(batch_train, file_json_train, is_multi_scale,
                                          mode_train, num_workers, path_img_train,
                                          transform_train)
    if file_json_val is not None:
        dataloader_val = _cre_data_load(batch_val, file_json_val, is_multi_scale,
                                        mode_val, num_workers, path_img_val,
                                        transform_val)
    if file_json_test is not None:
        dataloader_test = _cre_data_load(batch_test, file_json_test, is_multi_scale,
                                         mode_test, num_workers, path_img_test,
                                         transform_test)
    return dataloader_train, dataloader_val, dataloader_test


def _cre_data_load(batch_train, file_json_train, is_multi_scale, mode_train, num_workers, path_img_train,
                   transform_train):
    dataset_train = CustomCocoDataset(
        file_json=file_json_train,
        path_img=path_img_train,
        mode=mode_train,
        transform=transform_train,
        mode_balance_data=None,
    )
    dataloader_train = torch.utils.data.DataLoader(
        dataset_train,
        batch_size=batch_train,
        num_workers=num_workers,
        shuffle=True,
        pin_memory=True,  # 不使用虚拟内存 GPU要报错
        # drop_last=True,  # 除于batch_size余下的数据
        # collate_fn=lambda x: fun_dataloader(x, cfg),
        collate_fn=CLS4collate_fn(is_multi_scale),
    )
    return dataloader_train
