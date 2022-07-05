from django.shortcuts import HttpResponse
from django.http import JsonResponse
import base64
import cv2
import numpy as np
import os
import os.path as osp
from copy import deepcopy
from functools import partial

import numpy as np
import paddle
import paddleseg
from paddleseg import transforms
from paddleseg.models.ocrnet import OCRNet
from paddleseg.models.backbones.hrnet import HRNet_W18
# paddle.device.set_device('cpu')


# 定义全局变量
# 可在此处调整实验所用超参数

# 实验目录，保存输出的模型权重和结果
EXP_DIR =  '../data/tc_exp/'
# 保存最佳模型的路径
BEST_CKP_PATH = osp.join(EXP_DIR, 'best_model2/model.pdparams')

model = OCRNet(5,HRNet_W18(), backbone_indices=[0])
model_static = paddle.load(BEST_CKP_PATH)
model.set_dict(model_static)

model.eval()

infer_transforms = transforms.Compose([
    transforms.Normalize()
])

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

  with paddle.no_grad():
    input = data['img'][0].strip('data:false;base64,')
    input = base64.b64decode(input)
    input = cv2.imdecode(np.frombuffer(input, np.uint8), cv2.IMREAD_COLOR)
    input = infer_transforms(input)
    input = paddle.to_tensor(input[0],dtype="float32").unsqueeze(0)
    out = model(input)[0]
    out = paddle.argmax(out[0], axis=0).numpy()
    class1 = (out==0).sum().sum()/(out.shape[0]*out.shape[1])*100
    class2 = (out==1).sum().sum()/(out.shape[0]*out.shape[1])*100
    class3 = (out==2).sum().sum()/(out.shape[0]*out.shape[1])*100
    class4 = (out==3).sum().sum()/(out.shape[0]*out.shape[1])*100
    out = lut[out]
    cv2.imwrite('tc_out.png',out)
  #out = cv2.cvtColor(out,cv2.COLOR_BGR2RGB)
  retval,img_buffer = cv2.imencode('.jpg', out)
  return JsonResponse({'img':'data:false;base64,'+str(base64.b64encode(img_buffer))[2:-1],
                      'list':[{'class':'建筑','percent':'{:.2f}%'.format(class1),'color':'#0000FF'},
                              {'class':'耕地','percent':'{:.2f}%'.format(class2),'color':'#8EFF1E'},
                              {'class':'林地','percent':'{:.2f}%'.format(class3),'color':'#FF003C'},
                              {'class':'其他','percent':'{:.2f}%'.format(class4),'color':'#00DEFF'}
                              ]
                      })
