import random
import os
import os.path as osp
from copy import deepcopy
from functools import partial

import numpy as np
import paddle
import paddlers as pdrs
from paddlers import transforms as T
from PIL import Image
from skimage.io import imread, imsave
from tqdm import tqdm
from matplotlib import pyplot as plt

# 定义全局变量
# 可在此处调整实验所用超参数

# 随机种子
SEED = 199

# 数据集路径
DATA_DIR = '../data/'
# 实验路径。实验目录下保存输出的模型权重和结果
EXP_DIR = '../data/exp/'
# 保存最佳模型的路径
BEST_CKP_PATH = osp.join(EXP_DIR, 'best_model', 'model.pdparams')

# 训练的epoch数
NUM_EPOCHS = 930
# 每多少个epoch保存一次模型权重参数
SAVE_INTERVAL_EPOCHS = 1
# 初始学习率
LR = 0.001
# 学习率衰减步长（注意，单位为迭代次数而非epoch数），即每多少次迭代将学习率衰减
DECAY_STEP = 1000
# 训练阶段 batch size
TRAIN_BATCH_SIZE = 1
# 推理阶段 batch size
INFER_BATCH_SIZE = 1
# 裁块大小
CROP_SIZE = 512
# 模型推理阶段使用的滑窗步长
STRIDE = 64
# 影像原始大小
ORIGINAL_SIZE = (1024, 1024)

# 调用PaddleRS API一键构建模型
model = pdrs.tasks.BIT(
    # 模型输出类别数
    num_classes=2,
    # 是否使用混合损失函数，默认使用交叉熵损失函数训练
    use_mixed_loss=False,
    # 模型输入通道数
    in_channels=3,
    # 模型使用的骨干网络，支持'resnet18'或'resnet34'
    backbone='resnet34',
    # 骨干网络中的resnet stage数量
    n_stages=4,
    # 是否使用tokenizer获取语义token
    use_tokenizer=True,
    # token的长度
    token_len=4,
    # 若不使用tokenizer，则使用池化方式获取token。此参数设置池化模式，有'max'和'avg'两种选项，分别对应最大池化与平均池化
    pool_mode='max',
    # 池化操作输出特征图的宽和高（池化方式得到的token的长度为pool_size的平方）
    pool_size=2,
    # 是否在Transformer编码器中加入位置编码（positional embedding）
    enc_with_pos=True,
    # Transformer编码器使用的注意力模块（attention block）个数
    enc_depth=1,
    # Transformer编码器中每个注意力头的嵌入维度（embedding dimension）
    enc_head_dim=64,
    # Transformer解码器使用的注意力模块个数
    dec_depth=8,
    # Transformer解码器中每个注意力头的嵌入维度
    dec_head_dim=8
)

# 定义推理阶段使用的数据集

class InferDataset(paddle.io.Dataset):
    """
    变化检测推理数据集。

    Args:
        data_dir (str): 数据集所在的目录路径。
        transforms (paddlers.transforms.Compose): 需要执行的数据变换操作。
    """

    def __init__(
        self,
        data_dir,
        transforms
    ):
        super().__init__()

        self.data_dir = data_dir
        self.transforms = deepcopy(transforms)

        pdrs.transforms.arrange_transforms(
            model_type='changedetector',
            transforms=self.transforms,
            mode='test'
        )

        with open(osp.join(data_dir, 'test.txt'), 'r') as f:
            lines = f.read()
            lines = lines.strip().split('\n')

        samples = []
        names = []
        for line in lines:
            items = line.strip().split(' ')
            items = list(map(pdrs.utils.path_normalization, items))
            item_dict = {
                'image_t1': osp.join(data_dir, items[0]),
                'image_t2': osp.join(data_dir, items[1])
            }
            samples.append(item_dict)
            names.append(osp.basename(items[0]))

        self.samples = samples
        self.names = names

    def __getitem__(self, idx):
        sample = deepcopy(self.samples[idx])
        output = self.transforms(sample)
        return paddle.to_tensor(output[0]), \
               paddle.to_tensor(output[1])

    def __len__(self):
        return len(self.samples)


# 考虑到原始影像尺寸较大，以下类和函数与影像裁块-拼接有关。

class WindowGenerator:
    def __init__(self, h, w, ch, cw, si=1, sj=1):
        self.h = h
        self.w = w
        self.ch = ch
        self.cw = cw
        if self.h < self.ch or self.w < self.cw:
            raise NotImplementedError
        self.si = si
        self.sj = sj
        self._i, self._j = 0, 0

    def __next__(self):
        # 列优先移动（C-order）
        if self._i > self.h:
            raise StopIteration
        
        bottom = min(self._i+self.ch, self.h)
        right = min(self._j+self.cw, self.w)
        top = max(0, bottom-self.ch)
        left = max(0, right-self.cw)

        if self._j >= self.w-self.cw:
            if self._i >= self.h-self.ch:
                # 设置一个非法值，使得迭代可以early stop
                self._i = self.h+1
            self._goto_next_row()
        else:
            self._j += self.sj
            if self._j > self.w:
                self._goto_next_row()

        return slice(top, bottom, 1), slice(left, right, 1)

    def __iter__(self):
        return self

    def _goto_next_row(self):
        self._i += self.si
        self._j = 0

    
def crop_patches(dataloader, ori_size, window_size, stride):
    """
    将`dataloader`中的数据裁块。

    Args:
        dataloader (paddle.io.DataLoader): 可迭代对象，能够产生原始样本（每个样本中包含任意数量影像）。
        ori_size (tuple): 原始影像的长和宽，表示为二元组形式(h,w)。
        window_size (int): 裁块大小。
        stride (int): 裁块使用的滑窗每次在水平或垂直方向上移动的像素数。

    Returns:
        一个生成器，能够产生iter(`dataloader`)中每一项的裁块结果。一幅图像产生的块在batch维度拼接。例如，当`ori_size`为1024，而
            `window_size`和`stride`均为512时，`crop_patches`返回的每一项的batch_size都将是iter(`dataloader`)中对应项的4倍。
    """

    for ims in dataloader:
        ims = list(ims)
        h, w = ori_size
        win_gen = WindowGenerator(h, w, window_size, window_size, stride, stride)
        all_patches = []
        for rows, cols in win_gen:
            # NOTE: 此处不能使用生成器，否则因为lazy evaluation的缘故会导致结果不是预期的
            patches = [im[...,rows,cols] for im in ims]
            all_patches.append(patches)
        yield tuple(map(partial(paddle.concat, axis=0), zip(*all_patches)))


def recons_prob_map(patches, ori_size, window_size, stride):
    """从裁块结果重建原始尺寸影像，与`crop_patches`相对应"""
    # NOTE: 目前只能处理batch size为1的情况
    h, w = ori_size
    win_gen = WindowGenerator(h, w, window_size, window_size, stride, stride)
    prob_map = np.zeros((h,w), dtype=np.float)
    cnt = np.zeros((h,w), dtype=np.float)
    # XXX: 需要保证win_gen与patches具有相同长度。此处未做检查
    for (rows, cols), patch in zip(win_gen, patches):
        prob_map[rows, cols] += patch
        cnt[rows, cols] += 1
    prob_map /= cnt
    return prob_map


# 若输出目录不存在，则新建之（递归创建目录）
out_dir = osp.join(EXP_DIR, 'out')
if not osp.exists(out_dir):
    os.makedirs(out_dir)

# 为模型加载历史最佳权重
state_dict = paddle.load(BEST_CKP_PATH)
# 同样通过net属性访问组网对象
model.net.set_state_dict(state_dict)

# 实例化测试集
test_dataset = InferDataset(
    DATA_DIR,
    # 注意，测试阶段使用的归一化方式需与训练时相同
    T.Compose([
        T.Normalize(
            mean=[0.5, 0.5, 0.5],
            std=[0.5, 0.5, 0.5]
        )
    ])
)

# 创建DataLoader
test_dataloader = paddle.io.DataLoader(
    test_dataset,
    batch_size=1,
    shuffle=False,
    num_workers=0,
    drop_last=False,
    return_list=True
)
test_dataloader = crop_patches(
    test_dataloader,
    ORIGINAL_SIZE,
    CROP_SIZE,
    STRIDE
)

model.net.eval()
len_test = len(test_dataset.names)
with paddle.no_grad():
    for name, (t1, t2) in tqdm(zip(test_dataset.names, test_dataloader), total=len_test):
        shape = paddle.shape(t1)
        pred = paddle.zeros(shape=(shape[0],2,*shape[2:]))
        for i in range(0, shape[0], INFER_BATCH_SIZE):
            pred[i:i+INFER_BATCH_SIZE] = model.net(t1[i:i+INFER_BATCH_SIZE], t2[i:i+INFER_BATCH_SIZE])[0]
        # 取softmax结果的第1（从0开始计数）个通道的输出作为变化概率
        prob = paddle.nn.functional.softmax(pred, axis=1)[:,1]
        # 由patch重建完整概率图
        prob = recons_prob_map(prob.numpy(), ORIGINAL_SIZE, CROP_SIZE, STRIDE)
        # 默认将阈值设置为0.5，即，将变化概率大于0.5的像素点分为变化类
        out = (prob>0.5)*255
        out = out.astype(np.uint8)

        imsave(osp.join(out_dir, name), out, check_contrast=False)
