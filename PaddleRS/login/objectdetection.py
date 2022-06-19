from django.shortcuts import HttpResponse
import base64
import cv2
import numpy as np
import os.path as osp

import cv2
import numpy as np
import paddle
import paddlers as pdrs
from paddlers import transforms as T
from paddlers.tasks.utils.visualize import visualize_detection
from copy import deepcopy


#paddle.device.set_device('cpu')


# 定义全局变量
# 可在此处调整实验所用超参数

# 实验目录，保存输出的模型权重和结果
EXP_DIR =  '../data/od_exp/'
# 目标类别
CLASS = 'playground'
# 模型验证阶段输入影像尺寸
INPUT_SIZE = 608
# 保存最佳模型的路径
BEST_CKP_PATH = osp.join(EXP_DIR, 'best_model', 'model.pdparams')

# 构建PP-YOLO模型
model = pdrs.tasks.PPYOLO(num_classes=1)

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

class InferDataset(paddle.io.Dataset):
    """
    变化检测推理数据集。

    Args:
        data (str): 数据。
        transforms (paddlers.transforms.Compose): 需要执行的数据变换操作。
    """

    def __init__(
        self,
        data,
        transforms
    ):
        super().__init__()

        self.data = data
        self.transforms = deepcopy(transforms)

        pdrs.transforms.arrange_transforms(
            model_type='detector',
            transforms=self.transforms,
            mode='test'
        )
        t1 = data['img'][0].strip('data:false;base64,')
        t1 = base64.b64decode(t1)
        t1 = cv2.imdecode(np.frombuffer(t1, np.uint8), cv2.IMREAD_COLOR)
        samples = []
        item_dict = {
            'image': t1
        }
        samples.append(item_dict)

        self.samples = samples

    def __getitem__(self, idx):
        sample = deepcopy(self.samples[idx])
        output = self.transforms(sample)
        output['image'] = paddle.to_tensor(output['image']).transpose([2,0,1]).unsqueeze(0)
        output['im_shape'] = paddle.to_tensor(output['im_shape']).unsqueeze(0)
        output['scale_factor'] = paddle.to_tensor(output['scale_factor']).unsqueeze(0)
        return output

    def __len__(self):
        return len(self.samples)


# 为模型加载历史最佳权重
state_dict = paddle.load(BEST_CKP_PATH)
# 同样通过net属性访问组网对象
model.net.set_state_dict(state_dict)

model.net.eval()
model.labels = [CLASS]

# Create your views here.
def recvImg(request):
  data = dict(request.POST)
  # 实例化测试集
  #test_dataset = InferDataset(
  #    data,
  #    # 注意，测试阶段使用的归一化方式需与训练时相同
  #    eval_transforms
  #)
  t1 = data['img'][0].strip('data:false;base64,')
  t1 = base64.b64decode(t1)
  t1 = cv2.imdecode(np.frombuffer(t1, np.uint8), cv2.IMREAD_COLOR)
  with paddle.no_grad():
    #for input in test_dataset:
    t1 = cv2.resize(t1[...,::-1], (INPUT_SIZE, INPUT_SIZE), interpolation=cv2.INTER_CUBIC)
    out = model.predict(t1,eval_transforms)
    out = visualize_detection(
        np.array(t1), out, 
        color=np.asarray([[0,255,0]], dtype=np.uint8), 
        threshold=0.2, save_dir=None
    )
    cv2.imwrite('od_out.png',out)
  retval,img_buffer = cv2.imencode('.jpg', out)
  return HttpResponse('data:false;base64,'+str(base64.b64encode(img_buffer))[2:-1])
