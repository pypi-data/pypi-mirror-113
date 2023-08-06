from abc import abstractmethod

import torch
from torch import nn


def nms(boxes, scores, iou_threshold):
    ''' IOU大于0.5的抑制掉
         boxes (Tensor[N, 4])) – bounding boxes坐标. 格式：(ltrb
         scores (Tensor[N]) – bounding boxes得分
         iou_threshold (float) – IoU过滤阈值
     返回:NMS过滤后的bouding boxes索引（降序排列）
     '''
    return torch.ops.torchvision.nms(boxes, scores, iou_threshold)


def batched_nms(boxes_ltrb, scores, idxs, threshold_iou):
    '''
    多 labels nms
    :param boxes_ltrb: 拉平所有类别的box重复的 n*20类,4
    :param scores: torch.Size([16766])
    :param idxs:  真实类别index 通过手动创建匹配的 用于表示当前 nms的类别 用于统一偏移 技巧
    :param threshold_iou:float 0.5
    :return:
    '''
    if boxes_ltrb.numel() == 0:  # 维度全乘
        return torch.empty((0,), dtype=torch.int64, device=boxes_ltrb.device)

    # torchvision.ops.boxes.batched_nms(boxes, scores, lvl, nms_thresh)
    # 根据最大的一个值确定每一类的偏移
    max_coordinate = boxes_ltrb.max()  # 选出每个框的 坐标最大的一个值
    # idxs 的设备和 boxes 一致 , 真实类别index * (1+最大值) 则确保同类框向 左右平移 实现隔离
    offsets = idxs.to(boxes_ltrb) * (max_coordinate + 1)
    # boxes 加上对应层的偏移量后，保证不同类别之间boxes不会有重合的现象
    boxes_for_nms = boxes_ltrb + offsets[:, None]
    keep = nms(boxes_for_nms, scores, threshold_iou)
    return keep


def batch_nms(ids_batch1, p_boxes_ltrb1, p_labels1, p_scores1, threshold_nms):
    '''
    以每一个batch 为index 对 每一类进行偏移
    :param ids_batch1: [nn]
    :param p_boxes_ltrb1: [nn,4] float32
    :param p_labels1: [nn]
    :param p_scores1: [nn]
    :param threshold_nms:
    :return:
    '''
    device = p_boxes_ltrb1.device
    p_labels_unique = p_labels1.unique()  # nn -> n
    ids_batch2 = torch.tensor([], device=device)
    p_scores2 = torch.tensor([], device=device)
    p_labels2 = torch.tensor([], device=device)
    p_boxes_ltrb2 = torch.empty((0, 4), dtype=torch.float, device=device)

    for lu in p_labels_unique:  # 必须每类处理
        # 过滤类别
        _mask = p_labels1 == lu
        _ids_batch = ids_batch1[_mask]
        _p_scores = p_scores1[_mask]
        _p_labels = p_labels1[_mask]
        _p_boxes_ltrb = p_boxes_ltrb1[_mask]
        keep = batched_nms(_p_boxes_ltrb, _p_scores, _ids_batch, threshold_nms)
        # 极大抑制
        ids_batch2 = torch.cat([ids_batch2, _ids_batch[keep]])
        p_scores2 = torch.cat([p_scores2, _p_scores[keep]])
        p_labels2 = torch.cat([p_labels2, _p_labels[keep]])
        p_boxes_ltrb2 = torch.cat([p_boxes_ltrb2, _p_boxes_ltrb[keep]])
        # print('12')
    return ids_batch2, p_boxes_ltrb2, p_labels2, p_scores2


def batch_nms4kp(ids_batch1, p_boxes_ltrb1, p_labels1, p_scores1, p_keypoints1, threshold_nms):
    '''
    分类 nms
    :param ids_batch1: [nn]
    :param p_boxes_ltrb1: [nn,4] float32
    :param p_labels1: [nn]
    :param p_scores1: [nn]
    :param device:
    :param threshold_nms:
    :return:
    '''
    p_labels_unique = p_labels1.unique()  # nn -> n
    ids_batch2 = torch.tensor([], device=device)
    p_scores2 = torch.tensor([], device=device)
    p_labels2 = torch.tensor([], device=device)
    p_boxes_ltrb2 = torch.empty((0, 4), dtype=torch.float, device=device)
    # 这个不需要数量
    p_keypoints2 = torch.empty((0, cfg.NUM_KEYPOINTS * 2), dtype=torch.float, device=device)

    for lu in p_labels_unique:  # 必须每类处理
        # 过滤类别
        _mask = p_labels1 == lu
        _ids_batch = ids_batch1[_mask]
        _p_scores = p_scores1[_mask]
        _p_labels = p_labels1[_mask]
        _p_boxes_ltrb = p_boxes_ltrb1[_mask]
        keep = batched_nms(_p_boxes_ltrb, _p_scores, _ids_batch, threshold_nms)
        # 极大抑制
        ids_batch2 = torch.cat([ids_batch2, _ids_batch[keep]])
        p_scores2 = torch.cat([p_scores2, _p_scores[keep]])
        p_labels2 = torch.cat([p_labels2, _p_labels[keep]])
        p_boxes_ltrb2 = torch.cat([p_boxes_ltrb2, _p_boxes_ltrb[keep]])
        if p_keypoints1 is not None:
            _p_keypoints = p_keypoints1[_mask]
            p_keypoints2 = torch.cat([p_keypoints2, _p_keypoints[keep]])
        else:
            p_keypoints2 = None
        # print('12')
    return ids_batch2, p_boxes_ltrb2, p_keypoints2, p_labels2, p_scores2,


class Predicting_Base(nn.Module):
    '''
    由 f_fit_eval_base 运行至net模型主Center 再由模型主Center调用
    返回到 f_fit_eval_base
    '''

    def __init__(self, mode_vis, thr_pred_conf=0.05,
                 thr_pred_nms=0.5, select_topk=500) -> None:
        '''

        :param mode_vis:  这里是nms的 模式 bbox keypoints
        :param thr_pred_conf:
        :param thr_pred_nms:
        :param select_topk:
        '''
        super(Predicting_Base, self).__init__()
        self.mode_vis = mode_vis
        self.thr_pred_conf = thr_pred_conf  # 阀值
        self.thr_pred_nms = thr_pred_nms  # 阀值
        self.select_topk = select_topk  # 初选个数

    @abstractmethod
    def get_pscores(self, model_outs):
        '''

        :param model_outs: p_init 处理后
        :return:
            pscores : 这个用于判断 生成 mask_pos
            plabels : 这个用于二阶段
            pconf : 用于显示conf的统计值
        '''

    @abstractmethod
    def get_stage_res(self, model_outs, mask_pos, pscores, plabels, imgs_ts_4d, targets, toones_wh_ts_input):
        '''

        :param model_outs:
        :param mask_pos:
        :param pscores:
        :param plabels:
        :param imgs_ts_4d:
        :param targets:
        :param toones_wh_ts_input: 实际归一化尺寸
        :return:
            ids_batch1 : 返回第二阶段
            pboxes_ltrb1 :
            plabels1 :
            pscores1 :
        '''

    def forward(self, model_outs, imgs_ts_4d=None, targets=None, toones_wh_ts_input=None):
        '''
        由 FModelBase 已处理  toones_wh_ts_input
        :param model_outs: 模型的输出
        :return:
        '''

        ''' 进行数据的处理 传递到 get_pscores get_stage_res 中'''
        model_outs = self.p_init(model_outs)

        ''' 返回分数 和 plabels    pconf可返回任意值 用于没有目标时分析值域 '''
        pscores, plabels, pconf = self.get_pscores(model_outs)

        mask_pos = pscores > self.thr_pred_conf
        if not torch.any(mask_pos):  # 如果没有一个对象
            print('该批次没有找到目标 max:{0:.2f} min:{0:.2f} mean:{0:.2f}'.format(pconf.max().item(),
                                                                          pconf.min().item(),
                                                                          pconf.mean().item(),
                                                                          ))
            return [None] * 5

        if pscores.shape[-1] > self.select_topk:  # 并行取top100 与mask_pos 进行and操作
            # 最大1000个
            ids_topk = pscores.topk(self.select_topk, dim=-1)[1]  # torch.Size([32, 1000])
            mask_topk = torch.zeros_like(mask_pos)
            mask_topk[torch.arange(ids_topk.shape[0])[:, None], ids_topk] = True
            mask_pos = torch.logical_and(mask_pos, mask_topk)

        # ids_batch1, pboxes_ltrb1, plabels1, pscores1,pkp_keypoint
        reses = self.get_stage_res(model_outs, mask_pos, pscores, plabels, imgs_ts_4d, targets, toones_wh_ts_input)

        if self.mode_vis == 'bbox':  # 单人脸
            assert len(reses) == 4, 'res = self.get_stage_res(outs, mask_pos, pscores, plabels) 数据错误'
            ids_batch2, p_boxes_ltrb2, p_labels2, p_scores2 = batch_nms(reses[0],
                                                                        reses[1],
                                                                        reses[2],
                                                                        reses[3],
                                                                        self.thr_pred_nms)
            return ids_batch2, p_boxes_ltrb2, None, p_labels2, p_scores2,
        elif self.mode_vis == 'keypoints':
            assert len(reses) == 5, 'res = self.get_stage_res(outs, mask_pos, pscores, plabels) 数据错误'
            ids_batch2, p_boxes_ltrb2, p_keypoints2, p_labels2, p_scores2 = batch_nms4kp(
                ids_batch1=reses[0],
                p_boxes_ltrb1=reses[1],
                p_labels1=reses[2],
                p_scores1=reses[3],
                p_keypoints1=reses[4],
                threshold_nms=self.thr_pred_nms)
            return ids_batch2, p_boxes_ltrb2, p_keypoints2, p_labels2, p_scores2
        else:
            raise Exception('self.mode_vis = %s 错误' % self.mode_vis)
