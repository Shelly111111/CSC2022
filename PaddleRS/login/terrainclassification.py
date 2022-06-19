from django.shortcuts import HttpResponse
import base64
import cv2
import numpy as np
import os
import os.path as osp
from copy import deepcopy
from functools import partial

import numpy as np
import paddle
import paddlers as pdrs
from paddlers import transforms as T


#paddle.device.set_device('cpu')


# 定义全局变量
# 可在此处调整实验所用超参数

# 实验目录，保存输出的模型权重和结果
EXP_DIR =  '../data/tc_exp/'
# 保存最佳模型的路径
BEST_CKP_PATH = osp.join(EXP_DIR, 'best_model', 'model.pdparams')

# 构建DeepLab V3+模型，使用ResNet-50作为backbone
model = pdrs.tasks.DeepLabV3P(
    input_channel=3,
    num_classes=5,
    backbone='ResNet50_vd'
)

eval_transforms = T.Compose([
    T.Resize(target_size=256),
    # 验证阶段与训练阶段的数据归一化方式必须相同
    T.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
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
            model_type='segmenter',
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
        return paddle.to_tensor(output)

    def __len__(self):
        return len(self.samples)


# 为模型加载历史最佳权重
state_dict = paddle.load(BEST_CKP_PATH)
# 同样通过net属性访问组网对象
model.net.set_state_dict(state_dict)

model.net.eval()

def get_lut():
    lut = np.zeros((256,3), dtype=np.uint8)
    lut[0] = [255, 0, 0]
    lut[1] = [30, 255, 142]
    lut[2] = [60, 0, 255]
    lut[3] = [255, 222, 0]
    lut[4] = [0, 0, 0]
    return lut

# Create your views here.
def recvImg(request):
  data = dict(request.POST)
  lut=get_lut()
  # 实例化测试集
  test_dataset = InferDataset(
      data,
      # 注意，测试阶段使用的归一化方式需与训练时相同
      eval_transforms
  )
  with paddle.no_grad():
    for input in test_dataset:
      logits, *_ = model.net(input)
      out = paddle.argmax(logits[0], axis=0).numpy()
      out = lut[out]
      cv2.imwrite('tc_out.png',out)
  retval,img_buffer = cv2.imencode('.jpg', out)
  return HttpResponse('data:false;base64,'+str(base64.b64encode(img_buffer))[2:-1])
