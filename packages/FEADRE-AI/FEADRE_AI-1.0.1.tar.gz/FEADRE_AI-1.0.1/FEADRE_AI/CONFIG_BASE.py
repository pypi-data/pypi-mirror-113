class FCFG_BASE:
    # 训练验证
    IS_MIXTURE_FIT = True  # 半精度训练
    IS_TRAIN = True  # 开启训练
    IS_VAL = True  # 开启验证

    IS_TEST = True  # 开启测试
    IS_VISUAL = False  # 可视化模式 关联训练 和测试
    MODE_VIS = 'bbox'  # 验证的 计算模式 'keypoints','bbox' 关系到 可视化 nms等
    NUM_VIS_Z = 3  # 测试时可视化的图片数 超过就不再可视

    IS_DEBUG = False  # 调试模式

    PTOPK = 500  # 预测时 取分数最高的前500个进行

    # 频率参数
    PRINT_FREQ = 1  # 打印频率 与 batch*PRINT_FREQ
    NUMS_VAL_DICT = {2: 1, 35: 1, 50: 1}  # 验证起始和频率
    NUMS_TEST_DICT = {2: 1, 35: 1, 50: 1}  # 测试的起始和频率
    NUM_SAVE_INTERVAL = 1  # 保存频率
    MAPS_DEF_MAX = [0.5, 0.5]  # MAP的最大值 触发保存

    # 数据集
    # BATCH_TRAIN = 3
    # BATCH_VAL = 1

    # 数据增强
    IS_MULTI_SCALE = False  # 开启多尺寸训练 只要用数据增强必须有
    MULTI_SCALE_VAL = [200, 300]  # 多尺寸训练的尺寸范围

    # 其它动态参数
    PATH_SAVE_WEIGHT = ''

    def __str__(self) -> str:
        s = '---------------- CFG参数 ------------------\n'
        for name in dir(self):
            if not name.startswith('__'):
                s += ('\t' + name + ' : ' + str(getattr(self, name)) + '\n')
        return s
