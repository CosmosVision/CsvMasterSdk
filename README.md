# CsvMasterSdk
三维视觉引导系统SDK

## 运行环境
Python 3.9 <br>
PyCharm community 2021.1.3 / VS 2017+ <br>

## 运行库安装
pip install logging mkdocs <br>

## SDK使用流程
1.连接服务器 <br>
2.执行相关视觉操作 <br>
3.关闭服务器 <br>


## 例子

### 打开视频例子
```python
from CsvCamController import CsvCamController
from CsvData import CsvPose
import logging

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 9001
    '初始化相机'
    cam = CsvCamController(ip, port)
    '连接相机'
    cam.connect()

    '执行操作：视频打开,视觉服务器将会打开视频流'
    status = cam.openVideo()
    logging.warning("Open Video status:".format(status))
    '执行操作：视频关闭,视觉服务器将会关闭视频流'
    status = cam.closeVideo()
    logging.warning("Close Video status:".format(status))

    '断开相机'
    cam.disconnect()
```


### 识别例子
```python
    #!/usr/bin/env python3
    print("Hello, World!");
```
### 标定采图例子
```python
    #!/usr/bin/env python3
    print("Hello, World!");
```
