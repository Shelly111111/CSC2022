# 划分训练集/验证集/测试集，并生成文件名列表
# 注意，作为演示，本项目仅使用原数据集的训练集，即用来测试的数据也来自原数据集的训练集

import random
import os.path as osp
from os import listdir
from tqdm import tqdm

import cv2


# 随机数生成器种子
RNG_SEED = 77571
# 调节此参数控制训练集数据的占比
TRAIN_RATIO = 0.9
# 调节此参数控制验证集数据的占比
VAL_RATIO = 0.05
# 使用的样本个数（选取排序靠前的样本）
NUM_SAMPLES_TO_USE = 10000
# 数据集路径
DATA_DIR = '../data/terrainclassification/train_and_label'

# 分割类别
CLASSES = (
    'cls0',
    'cls1',
    'cls2',
    'cls3',
    'bg'
)


def reset_pixels(name):
    path = osp.join(DATA_DIR, 'lab_train', name)
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    im[im==255] = CLASSES.index('bg')
    cv2.imwrite(path, im)


def write_rel_paths(phase, names, out_dir):
    """将文件相对路径存储在txt格式文件中"""
    with open(osp.join(out_dir, phase+'.txt'), 'w') as f:
        for name in names:
            f.write(
                ' '.join([
                    osp.join('img_train', name.replace('.png', '.jpg')),
                    osp.join('lab_train', name)
                ])
            )
            f.write('\n')


random.seed(RNG_SEED)

names = listdir(osp.join(DATA_DIR, 'lab_train'))
# 将值为255的无效像素重设为背景类
for name in tqdm(names):
    reset_pixels(name)
# 对文件名进行排序，以确保多次运行结果一致
names.sort()
if NUM_SAMPLES_TO_USE is not None:
    names = names[:NUM_SAMPLES_TO_USE]
random.shuffle(names)
len_train = int(len(names)*TRAIN_RATIO)
len_val = int(len(names)*VAL_RATIO)
write_rel_paths('train', names[:len_train], DATA_DIR)
write_rel_paths('val', names[len_train:len_train+len_val], DATA_DIR)
write_rel_paths('test', names[len_train+len_val:], DATA_DIR)

# 写入类别信息
with open(osp.join(DATA_DIR, 'labels.txt'), 'w') as f:
    for cls in CLASSES:
        f.write(cls+'\n')

print("数据集划分已完成。")
