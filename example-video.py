#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Breif    : 视频控制例子
@Project  ：CsvMasterSdk
@File     ：example-video.py
@Author   ：HORSETAIL
@Date     ：2022/2/9 15:49
@Company  : Shenzhen Cosmos Vision Tech Co., Ltd
@Copyright: Copyright@Cosmos Vision Tech.All Rights Reserved.
'''

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

