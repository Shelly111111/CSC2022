# 划分训练集/验证集/测试集，并生成文件名列表

import random
import os.path as osp
from os import listdir
from glob import glob
from tqdm import tqdm

import cv2


# 随机数生成器种子
RNG_SEED = 56961
# 调节此参数控制训练集数据的占比
TRAIN_RATIO = 0.9
# 数据集路径
DATA_DIR = '../data/massroad'

# 分割类别
CLASSES = (
    'background',
    'road',
)

def write_rel_paths(phase, names, out_dir, prefix):
    """将文件相对路径存储在txt格式文件中"""
    with open(osp.join(out_dir, phase+'.txt'), 'w') as f:
        for name in names:
            f.write(
                ' '.join([
                    osp.join(prefix, 'input', name),
                    osp.join(prefix, 'output', name)
                ])
            )
            f.write('\n')


random.seed(RNG_SEED)

train_prefix = osp.join('road_segmentation_ideal', 'training')
test_prefix = osp.join('road_segmentation_ideal', 'testing')
train_names = listdir(osp.join(DATA_DIR, train_prefix, 'output'))
train_names = list(filter(lambda n: n.endswith('.png'), train_names))
test_names = listdir(osp.join(DATA_DIR, test_prefix, 'output'))
test_names = list(filter(lambda n: n.endswith('.png'), test_names))
# 对文件名进行排序，以确保多次运行结果一致
train_names.sort()
test_names.sort()
random.shuffle(train_names)
len_train = int(len(train_names)*TRAIN_RATIO)
write_rel_paths('train', train_names[:len_train], DATA_DIR, train_prefix)
write_rel_paths('val', train_names[len_train:], DATA_DIR, train_prefix)
write_rel_paths('test', test_names, DATA_DIR, test_prefix)

# 写入类别信息
with open(osp.join(DATA_DIR, 'labels.txt'), 'w') as f:
    for cls in CLASSES:
        f.write(cls+'\n')

print("数据集划分已完成。")


# 将GT中的255改写为1，便于训练

train_prefix = osp.join('road_segmentation_ideal', 'training')
test_prefix = osp.join('road_segmentation_ideal', 'testing')

train_paths = glob(osp.join(DATA_DIR, train_prefix, 'output', '*.png'))
test_paths = glob(osp.join(DATA_DIR, test_prefix, 'output', '*.png'))
for path in tqdm(train_paths+test_paths):
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    im[im>0] = 1
    # 原地改写
    cv2.imwrite(path, im)
