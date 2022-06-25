# 导入需要用到的库

import random
import os.path as osp

import cv2
import numpy as np
import paddle
import paddlers as pdrs
from paddlers import transforms as T
from matplotlib import pyplot as plt
from PIL import Image

# 定义全局变量

# 数据集存放目录
DATA_DIR = '../data/terrainclassification/train_and_label/'
# 测试集`file_list`文件路径
TEST_FILE_LIST_PATH = '../data/terrainclassification/train_and_label/test.txt'
# 数据集类别信息文件路径
LABEL_LIST_PATH = '../data/terrainclassification/train_and_label/labels.txt'
# 实验目录，保存输出的模型权重和结果
EXP_DIR =  '../data/tc_exp/'

eval_transforms = T.Compose([
    T.Resize(target_size=256),
    # 验证阶段与训练阶段的数据归一化方式必须相同
    T.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

# 构建DeepLab V3+模型，使用ResNet-50作为backbone
model = pdrs.tasks.DeepLabV3P(
    input_channel=3,
    num_classes=5,
    backbone='ResNet50_vd'
)

# 构建测试集
test_dataset = pdrs.datasets.SegDataset(
    data_dir=DATA_DIR,
    file_list=TEST_FILE_LIST_PATH,
    label_list=LABEL_LIST_PATH,
    transforms=eval_transforms,
    num_workers=0,
    shuffle=False
)


# 为模型加载历史最佳权重
state_dict = paddle.load(osp.join(EXP_DIR, 'best_model/model.pdparams'))
model.net.set_state_dict(state_dict)

# 执行测试
test_result = model.evaluate(test_dataset)
print(
    "测试集上指标：mIoU为{:.2f}，OAcc为{:.2f}，Kappa系数为{:.2f}".format(
        test_result['miou'], 
        test_result['oacc'],
        test_result['kappa'],
    )
)
print("各类IoU分别为："+', '.join('{:.2f}'.format(iou) for iou in test_result['category_iou']))
print("各类Acc分别为："+', '.join('{:.2f}'.format(acc) for acc in test_result['category_acc']))
print("各类F1分别为："+', '.join('{:.2f}'.format(f1) for f1 in test_result['category_F1-score']))
