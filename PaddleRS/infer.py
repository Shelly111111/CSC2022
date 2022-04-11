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


# 推理过程主循环
info("模型推理开始")

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
        out = quantize(prob>0.5)

        imsave(osp.join(out_dir, name), out, check_contrast=False)

info("模型推理完成")


# 推理结果展示
# 重复运行本单元可以查看不同结果

def show_images_in_row(im_paths, fig, title=''):
    n = len(im_paths)
    fig.suptitle(title)
    axs = fig.subplots(nrows=1, ncols=n)
    for idx, (path, ax) in enumerate(zip(im_paths, axs)):
        # 去掉刻度线和边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

        im = imread(path)
        ax.imshow(im)


# 需要展示的样本个数
num_imgs_to_show = 4
# 随机抽取样本
chosen_indices = random.choices(range(len_test), k=num_imgs_to_show)

# 参考 https://stackoverflow.com/a/68209152
fig = plt.figure(constrained_layout=True)
fig.suptitle("Inference Results")

subfigs = fig.subfigures(nrows=3, ncols=1)

# 读入第一时相影像
im_paths = [osp.join(DATA_DIR, test_dataset.samples[idx]['image_t1']) for idx in chosen_indices]
show_images_in_row(im_paths, subfigs[0], title='Image 1')

# 读入第二时相影像
im_paths = [osp.join(DATA_DIR, test_dataset.samples[idx]['image_t2']) for idx in chosen_indices]
show_images_in_row(im_paths, subfigs[1], title='Image 2')

# 读入变化图
im_paths = [osp.join(out_dir, test_dataset.names[idx]) for idx in chosen_indices]
show_images_in_row(im_paths, subfigs[2], title='Change Map')

# 渲染结果
fig.canvas.draw()
Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
