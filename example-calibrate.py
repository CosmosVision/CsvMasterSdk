#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Breif    : 标定采图例子
@Project  ：CsvMasterSdk
@File     ：example-calibrate.py
@Author   ：HORSETAIL
@Date     ：2022/2/9 15:49
@Company  : Shenzhen Cosmos Vision Tech Co., Ltd
@Copyright: Copyright@Cosmos Vision Tech.All Rights Reserved.
"""

from CsvCamController import CsvCamController
from CsvData import CsvPose
import logging

if __name__ == "__main__":

    '根据实际的视觉服务器IP/Port进行配置'
    ip = "127.0.0.1"
    port = 9001
    '初始化相机'
    cam = CsvCamController(ip, port)
    '连接相机'
    cam.connect()

    '执行操作：标定拍照'
    flange_pose = CsvPose(1000,0,2000,0,0,0)
    calib_res = cam.calShootSave(flange_pose)
    logging.warning("标定采图和保存的执行状态:{}".format(calib_res))

    '断开相机'
    cam.disconnect()

