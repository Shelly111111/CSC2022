# 导入需要用到的库

import os.path as osp

import paddle
import paddlers as pdrs
from paddlers import transforms as T


# 定义全局变量

# 数据集存放目录
DATA_DIR = '../data/objectdetection/'
# 测试集`file_list`文件路径
TEST_FILE_LIST_PATH = '../data/objectdetection/test.txt'
# 数据集类别信息文件路径
LABEL_LIST_PATH = '../data/objectdetection/labels.txt'
# 实验目录，保存输出的模型权重和结果
EXP_DIR =  '../data/od_exp/'
# 目标类别
CLASS = 'playground'
# 模型验证阶段输入影像尺寸
INPUT_SIZE = 608

eval_transforms = T.Compose([
    # 使用双三次插值将输入影像缩放到固定大小
    T.Resize(
        target_size=INPUT_SIZE, interp='CUBIC'
    ),
    # 验证阶段与训练阶段的归一化方式必须相同
    T.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )
])


# 构建PP-YOLO模型
model = pdrs.tasks.PPYOLO(num_classes=1)

# 构建测试集
test_dataset = pdrs.datasets.VOCDetection(
    data_dir=DATA_DIR,
    file_list=TEST_FILE_LIST_PATH,
    label_list=LABEL_LIST_PATH,
    transforms=eval_transforms,
    shuffle=False
)

# 为模型加载历史最佳权重
state_dict = paddle.load(osp.join(EXP_DIR, 'best_model/model.pdparams'))
model.net.set_state_dict(state_dict)

# 执行测试
test_result = model.evaluate(test_dataset)
print(
    "测试集上指标：bbox mAP为{:.2f}".format(
        test_result['bbox_map'], 
    )
)
