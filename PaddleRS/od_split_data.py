# 划分训练集/验证集/测试集，并生成文件名列表
# 所有样本从RSOD数据集的playground子集中选取

import random
import os.path as osp
from os import listdir


# 随机数生成器种子
RNG_SEED = 52980
# 调节此参数控制训练集数据的占比
TRAIN_RATIO = 0.9
# 调节此参数控制验证集数据的占比
VAL_RATIO = 0.05
# 数据集路径
DATA_DIR = '../data/objectdetection/'

# 目标类别
CLASS = 'playground'


def write_rel_paths(phase, names, out_dir):
    """将文件相对路径存储在txt格式文件中"""
    with open(osp.join(out_dir, phase+'.txt'), 'w') as f:
        for name in names:
            f.write(
                ' '.join([
                    osp.join(CLASS, 'JPEGImages', name),
                    osp.join(CLASS, 'Annotation', 'xml', name.replace('.jpg', '.xml'))
                ])
            )
            f.write('\n')


random.seed(RNG_SEED)

names = listdir(osp.join(DATA_DIR, CLASS, 'JPEGImages'))
# 对文件名进行排序，以确保多次运行结果一致
names.sort()
random.shuffle(names)
len_train = int(len(names)*TRAIN_RATIO)
len_val = int(len(names)*VAL_RATIO)
write_rel_paths('train', names[:len_train], DATA_DIR)
write_rel_paths('val', names[len_train:len_train+len_val], DATA_DIR)
write_rel_paths('test', names[len_train+len_val:], DATA_DIR)

# 写入类别信息
with open(osp.join(DATA_DIR, 'labels.txt'), 'w') as f:
    f.write(CLASS+'\n')

print("数据集划分已完成。")
