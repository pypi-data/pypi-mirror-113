import warnings
from abc import ABCMeta

import torch

from tools.GLOBAL_LOG import flog
from tools.boxes.f_boxes import bbox_iou_v3, ltrb2xywh, xywh2ltrb
from tools.datas.f_data_pretreatment4np import f_recover_normalization4ts
from tools.f_calc_adv import f_cre_grid_cells


def match4atss(gltrb_i_b, anc_ltrb_i, nums_dim_t_list, glabels_b=None,
               img_ts=None, is_visual=False):
    '''
    这里默认都是 input 尺寸 且是batch
    核心作用:
        1. 使正例框数量都保持一致 保障小目标也能匹配到多个anc
        2. 用最大一个iou的均值和标准差,计算阀值,用IOU阀值初选正样本
        3. 确保anc中心点在gt框中

    :param gltrb_i_b:
    :param anc_ltrb_i:
    :param nums_dim_t_list:
        [1600, 400, 100] 这个是每个特图对应的维度数 用于索引 如果只有一层可以优化掉
    :param glabels_b: 暂时没用 可视化
    :param img_ts: 可视化
    :param is_visual:  可视化
    :return:
        mask_pos : [2100] 正例mask
        anc_max_iou: [2100] anc 对应的最大IOU值
        g_pos_index: [2100] anc 对应GT的索引
    '''
    device = gltrb_i_b.device

    # 计算 iou
    anc_xywh_i = ltrb2xywh(anc_ltrb_i)
    # num_anc = anc_xywh_i.shape[0]
    # (anc 个,boxes 个) torch.Size([3, 10647])
    ious_ag = bbox_iou_v3(anc_ltrb_i, gltrb_i_b)
    num_gt = gltrb_i_b.shape[0]  # 正样本个数

    # 全部ANC的距离
    gxywh_i_b = ltrb2xywh(gltrb_i_b)
    # 中间点绝对距离 多维广播 (anc 个,boxes 个)  torch.Size([32526, 7])
    distances = (anc_xywh_i[:, None, :2] - gxywh_i_b[None, :, :2]).pow(2).sum(-1).sqrt()

    # 每层 anc 数是一致的
    num_atss_topk = 9  # 这个 topk = 要 * 该层的anc数

    idxs_candidate = []  # 这个用来保存最一层所匹配的最小距离anc的索引  每层9个
    index_start = 0  # 这是每层的anc偏移值
    for i, num_dim_feature in enumerate(nums_dim_t_list):  # [24336, 6084, 1521, 441, 144]
        '''每一层的每一个GT选 topk * anc数'''
        index_end = index_start + num_dim_feature
        # 取出某层的所有anc距离  中间点绝对距离 (anc 个,boxes 个)  torch.Size([32526, 7]) -> [nn, 7]
        distances_per_level = distances[index_start:index_end, :]
        # 确认该层的TOPK 不能超过该层总 anc 数 这里是一个数
        topk = min(num_atss_topk, num_dim_feature)
        # 选 topk个最小的 每个gt对应对的anc的index torch.Size([24336, box_n])---(anc,gt) -> torch.Size([topk, 1])
        _, topk_idxs_per_level = distances_per_level.topk(topk, dim=0, largest=False)  # 只能在某一维top
        idxs_candidate.append(topk_idxs_per_level + index_start)
        index_start = index_end

    # 用于计算iou均值和方差 候选人，候补者；应试者 torch.Size([405, 1])
    idxs_candidate = torch.cat(idxs_candidate, dim=0)
    '''--- 选出每层每个anc对应的距离中心最近topk iou值 ---'''
    # ***************这个是ids选择 这个是多维筛选 ious---[anc,ngt]    [405, ngt] [0,1...ngt]-> [405,ngt]
    ious_candidate = ious_ag[idxs_candidate, torch.arange(num_gt)]  # 这里是index 蒙板取数的方法
    mask_distances = torch.zeros_like(distances, device=device, dtype=torch.bool)
    # [2000,ngt]
    mask_distances[idxs_candidate, torch.arange(idxs_candidate.shape[1])] = True

    if is_visual:
        # ***********  debug 可视  匹配29个正例可视化  *****************
        from tools.picture.f_show import f_show_od_ts4plt_v3
        # 多个gt 对应一个anc 进行转换显示
        mask_pos = torch.zeros(mask_distances.shape[0], device=device, dtype=torch.bool)
        mask_distances_t = mask_distances.t()  # [32526 , 3] -> [3, 32526]
        for m_pos_iou in mask_distances_t:  # 拉平 每个 32526
            # 遍历GT 直接进行一个或操作 更新 mask
            mask_pos = torch.logical_or(m_pos_iou, mask_pos)
        f_show_od_ts4plt_v3(img_ts, g_ltrb=gltrb_i_b,
                            p_ltrb=anc_ltrb_i[mask_pos],
                            is_normal=True,
                            )

    '''--- 用最大一个iou的均值和标准差,计算阀值 ---'''
    # 统计每一个 GT的均值 std [ntopk,ngt] -> [ngt] 个
    _iou_mean_per_gt = ious_candidate.mean(dim=0)  # 除维
    _iou_std_per_gt = ious_candidate.std(dim=0)
    _iou_thresh_per_gt = _iou_mean_per_gt + _iou_std_per_gt
    '''--- 用IOU阀值初选正样本 ---'''
    # torch.Size([32526, 1]) ^^ ([ngt] -> [1,ngt]) -> [32526,ngt]
    mask_pos4iou = ious_ag >= _iou_thresh_per_gt[None, :]  # 核心是这个选

    '''--- 中心点需落在GT中间 需要选出 anc的中心点-gt的lt为正, gr的rb-anc的中心点为正  ---'''
    # torch.Size([32526, 1, 2])
    dlt = anc_xywh_i[:, None, :2] - gltrb_i_b[None, :, :2]
    drb = gltrb_i_b[None, :, 2:] - anc_xywh_i[:, None, :2]
    # [32526, 1, 2] -> [32526, 1, 4] -> [32526, 1]
    mask_pos4in_gt = torch.all(torch.cat([dlt, drb], dim=-1) > 0.01, dim=-1)
    mask_pos_iou = torch.logical_and(torch.logical_and(mask_distances, mask_pos4iou), mask_pos4in_gt)

    '''--- 生成最终正例mask [32526, ngt] -> [32526] ---'''
    mask_pos = torch.zeros(mask_pos_iou.shape[0], device=device, dtype=torch.bool)
    mask_pos_iou = mask_pos_iou.t()  # [32526 , 3] -> [3, 32526]
    for m_pos_iou in mask_pos_iou:  # 拉平 每个 32526
        mask_pos = torch.logical_or(m_pos_iou, mask_pos)

    '''--- 确定anc匹配 一个锚框被多个真实框所选择，则其归于iou较高的真实框  ---'''
    # (anc 个,boxes 个) torch.Size([3, 10647])
    anc_max_iou, g_index = ious_ag.max(dim=1)  # 存的是 bboxs的index

    if is_visual:
        # ***********  debug 可视  多重过滤后个正例可视化  *****************
        from tools.picture.f_show import f_show_od_ts4plt_v3
        f_show_od_ts4plt_v3(img_ts, g_ltrb=gltrb_i_b,
                            p_ltrb=anc_ltrb_i[mask_pos],
                            is_normal=True,
                            )

    return mask_pos, anc_max_iou, g_index


def decode4nanodet(grids_xy_input, p_tltrb, max_size_hw=None):
    '''

    :param grids_xy_input: torch.Size([2100, 2])
    :param p_tltrb: torch.Size([3, 2100, 4])
    :param max_size_hw: 预测时使用
    :return:
    '''
    # torch.Size([3, 2100])
    x1 = grids_xy_input[:, 0] - p_tltrb[..., 0]
    y1 = grids_xy_input[:, 1] - p_tltrb[..., 1]
    x2 = grids_xy_input[:, 0] + p_tltrb[..., 2]
    y2 = grids_xy_input[:, 1] + p_tltrb[..., 3]
    if max_size_hw is not None:
        x1 = x1.clamp(min=0, max=max_size_hw[1])
        y1 = y1.clamp(min=0, max=max_size_hw[0])
        x2 = x2.clamp(min=0, max=max_size_hw[1])
        y2 = y2.clamp(min=0, max=max_size_hw[0])
    # torch.Size([3, 2100]) x4 torch.Size([3, 2100,4])
    return torch.stack([x1, y1, x2, y2], -1)


def encode4nanodet(grids_xy_input, g_ltrb, max_val, eps=0.1, mask_debug=None):
    '''
    编码针对特图
    :param grids_xy_input:  torch.Size([2100, 2])
    :param g_ltrb:  torch.Size([3, 2100, 4])
    :param max_val: 限制匹配的正例 最大距离 在0~7 之内
    :param mask_debug:  用于查看 GT 与 匹配的点 的ltrb距离是否会超过7
    :param eps:
    :return:
    '''
    from tools.GLOBAL_LOG import flog
    left = grids_xy_input[:, 0] - g_ltrb[..., 0]
    top = grids_xy_input[:, 1] - g_ltrb[..., 1]
    right = g_ltrb[..., 2] - grids_xy_input[:, 0]
    bottom = g_ltrb[..., 3] - grids_xy_input[:, 1]
    g_tltrb = torch.stack([left, top, right, bottom], -1)
    flog.debug('正例 g_ltrb min=%f  max=%f' % (g_tltrb[mask_debug].min(), g_tltrb[mask_debug].max()))
    if max_val is not None:
        g_tltrb = g_tltrb.clamp(min=0, max=max_val - eps)
    return g_tltrb


def match_yolo1_od(g_ltrb_input_b, g_labels_b, size_wh_t_ts, device, cfg, img_ts_input, toone_wh_ts_input=None):
    '''
    匹配 gyolo 如果需要计算IOU 需在这里生成
    :param g_ltrb_input_b: ltrb
    :param g_labels_b:
    :param grid: 13
    :param device:
    :return:
    '''
    num_gt = g_ltrb_input_b.shape[0]
    g_txywh_t, weights, indexs_colrow_t = encode_yolo1_od(g_ltrb_input_b, size_wh_t_ts, cfg)

    g_cls_b_ = torch.zeros((size_wh_t_ts[1], size_wh_t_ts[0], cfg.NUM_CLASSES), device=device)
    g_weight_b_ = torch.zeros((size_wh_t_ts[1], size_wh_t_ts[0], 1), device=device)
    g_txywh_t_b_ = torch.zeros((size_wh_t_ts[1], size_wh_t_ts[0], 4), device=device)

    labels_index = (g_labels_b - 1).long()
    indexs_colrow_t = indexs_colrow_t.long()  # index需要long类型

    for i in range(num_gt):
        g_cls_b_[indexs_colrow_t[i, 1], indexs_colrow_t[i, 0], labels_index[i]] = 1  # 构建 onehot
        g_weight_b_[indexs_colrow_t[i, 1], indexs_colrow_t[i, 0]] = weights[i]
        g_txywh_t_b_[indexs_colrow_t[i, 1], indexs_colrow_t[i, 0]] = g_txywh_t[i]

    g_cls_b_ = g_cls_b_.reshape(-1, cfg.NUM_CLASSES)
    g_weight_b_ = g_weight_b_.reshape(-1, 1)
    g_txywh_t_b_ = g_txywh_t_b_.reshape(-1, 4)

    '''可视化验证'''
    if cfg.IS_VISUAL:
        mask_pos_1d = (g_weight_b_ > 0).any(-1)  # [169]

        # [2] -> [1,2] -> [ngt,2]
        sizes_wh_t_ts = size_wh_t_ts.unsqueeze(0).repeat(num_gt, 1)

        flog.debug('size_wh_t_ts = %s', size_wh_t_ts)
        flog.debug('toone_wh_ts_input = %s', toone_wh_ts_input)
        flog.debug('g_txywh_t = %s', g_txywh_t)
        flog.debug('indexs_colrow_t = %s', indexs_colrow_t)
        flog.debug('对应index = %s', indexs_colrow_t[0, 1] * size_wh_t_ts[0] + indexs_colrow_t[0, 0])
        flog.debug('对应index = %s', torch.where(g_weight_b_ > 0))

        flog.debug('g_ltrb_input_b = %s', g_ltrb_input_b)

        grid_wh = [size_wh_t_ts[0].item(), size_wh_t_ts[1].item()]
        # 预测时需要sigmoid  这里的 g_txywh_t_b_ 已 sigmoid
        p_ltrb_t = decode_yolo1_od(p_txywh_t_sigmoidxy=g_txywh_t_b_, grid_wh=grid_wh,
                                   toones_wh_ts_t=sizes_wh_t_ts, is_to_one=False)
        p_ltrb_t_pos = p_ltrb_t[mask_pos_1d]

        from f_tools.pic.enhance.f_data_pretreatment4np import f_recover_normalization4ts

        img_ts = f_recover_normalization4ts(img_ts_input)
        from torchvision.transforms import functional as transformsF
        img_pil = transformsF.to_pil_image(img_ts).convert('RGB')
        import numpy as np
        img_np = np.array(img_pil)

        # 特图 -> input
        # img_wh_ts_x2 = torch.tensor(img_np.shape[:2][::-1], device=device).repeat(2)
        p_ltrb_input_pos = p_ltrb_t_pos * cfg.STRIDE

        flog.debug('p_ltrb_input_pos = %s', p_ltrb_input_pos)
        flog.debug(' ----------------------------------------- ')
        f_show_od_np4plt_v2(img_np,
                            gboxes_ltrb=g_ltrb_input_b.cpu(),
                            pboxes_ltrb=p_ltrb_input_pos.cpu(),
                            is_recover_size=False,
                            grid_wh_np=size_wh_t_ts.cpu().numpy())

    return g_cls_b_, g_weight_b_, g_txywh_t_b_


def encode_yolo1_od(g_ltrb_input_b, size_wh_t_ts, cfg):
    # ltrb -> xywh 原图归一化   编码xy与yolo2一样的
    g_xywh_input = ltrb2xywh(g_ltrb_input_b)
    g_xywh_t = g_xywh_input / cfg.STRIDE
    cxys_t = g_xywh_t[:, :2]
    whs_t = g_xywh_t[:, 2:]
    whs_one = whs_t / size_wh_t_ts

    # 转换到特图的格子中
    indexs_colrow_t = cxys_t.floor()
    g_txy_t = cxys_t - indexs_colrow_t
    g_twh_t = whs_t.log()
    g_txywh_t = torch.cat([g_txy_t, g_twh_t], dim=-1)

    # 值在 1~2 之间 放大小的
    weights = 2.0 - torch.prod(whs_one, dim=-1)

    return g_txywh_t, weights, indexs_colrow_t


def decode_yolo1_od(p_txywh_t_sigmoidxy, grid_wh, toones_wh_ts_t, is_to_one):
    '''
    解码出来是特图
    :param p_txywh_t_sigmoidxy:  必须 c 是最后一维
    :return: 输出原图归一化
    '''
    device = p_txywh_t_sigmoidxy.device
    # 单一格子偏移 + 特图格子偏移
    p_xy_t = p_txywh_t_sigmoidxy[..., :2] + f_cre_grid_cells((grid_wh[1], grid_wh[0]), is_swap=True, num_repeat=1).to(
        device)
    p_wh_t = p_txywh_t_sigmoidxy[..., 2:].exp()
    p_xywh_t = torch.cat([p_xy_t, p_wh_t], -1)
    p_ltrb_t = xywh2ltrb(p_xywh_t)
    if is_to_one:
        # torch.Size([2, 169, 4])  ^^ batch,1,4
        p_ltrb_one = torch.true_divide(p_ltrb_t, toones_wh_ts_t.repeat(1, 2).unsqueeze(1))  # 特图-》 one
        return p_ltrb_one
    return p_ltrb_t
