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
DATA_DIR = '../data/massroad/'
# 测试集`file_list`文件路径
TEST_FILE_LIST_PATH = '../data/massroad/test.txt'
# 数据集类别信息文件路径
LABEL_LIST_PATH = '../data/massroad/labels.txt'
# 实验目录，保存输出的模型权重和结果
EXP_DIR =  '../data/te_exp/'

# 构建DeepLab V3+模型，使用ResNet-50作为backbone
model = pdrs.tasks.DeepLabV3P(
    input_channel=3,
    num_classes=2,
    backbone='ResNet50_vd'
)

eval_transforms = T.Compose([
    T.Resize(target_size=1488),
    # 验证阶段与训练阶段的数据归一化方式必须相同
    T.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

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
    "测试集上指标：IoU为{:.2f}，Acc为{:.2f}，Kappa系数为{:.2f}, F1为{:.2f}".format(
        test_result['category_iou'][1], 
        test_result['category_acc'][1],
        test_result['kappa'],
        test_result['category_F1-score'][1]
    )
)

# 预测结果可视化
# 重复运行本单元可以查看不同结果

def read_image(path):
    im = cv2.imread(path)
    return im[...,::-1]


def show_images_in_row(ims, fig, title='', quantize=False):
    n = len(ims)
    fig.suptitle(title)
    axs = fig.subplots(nrows=1, ncols=n)
    for idx, (im, ax) in enumerate(zip(ims, axs)):
        # 去掉刻度线和边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

        if isinstance(im, str):
            im = read_image(im)
        if quantize:
            im = (im*255).astype('uint8')
        if im.ndim == 2:
            im = np.tile(im[...,np.newaxis], [1,1,3])
        ax.imshow(im)


# 需要展示的样本个数
num_imgs_to_show = 4
# 随机抽取样本
chosen_indices = random.choices(range(len(test_dataset)), k=num_imgs_to_show)

# 参考 https://stackoverflow.com/a/68209152
fig = plt.figure(constrained_layout=True)
fig.suptitle("Test Results")

subfigs = fig.subfigures(nrows=3, ncols=1)

# 读取输入影像并显示
im_paths = [test_dataset.file_list[idx]['image'] for idx in chosen_indices]
show_images_in_row(im_paths, subfigs[0], title='Image')

# 获取模型预测输出
with paddle.no_grad():
    model.net.eval()
    preds = []
    for idx in chosen_indices:
        input, mask = test_dataset[idx]
        input = paddle.to_tensor(input).unsqueeze(0)
        logits, *_ = model.net(input)
        pred = paddle.argmax(logits[0], axis=0)
        preds.append(pred.numpy())
show_images_in_row(preds, subfigs[1], title='Pred', quantize=True)

# 读取真值标签并显示
im_paths = [test_dataset.file_list[idx]['mask'] for idx in chosen_indices]
show_images_in_row(im_paths, subfigs[2], title='GT', quantize=True)

# 渲染结果
fig.canvas.draw()
Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
