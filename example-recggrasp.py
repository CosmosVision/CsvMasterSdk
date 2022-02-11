#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Breif    : 识别抓取例子
@Project  ：CsvMasterSdk
@File     ：example-recggrasp.py
@Author   ：HORSETAIL
@Date     ：2022/2/9 15:49
@Company  : Shenzhen Cosmos Vision Tech Co., Ltd
@Copyright: Copyright@Cosmos Vision Tech.All Rights Reserved.
"""

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

    '执行操作：仅识别'
    flange_pose = CsvPose(1000,0,2000,0,0,0)
    recg_res = cam.recgGrasp(flange_pose, "ALL")
    logging.warning("Recgnize and Grasp Result:pick id:{},modelid:{},isvalid:{}"
          ",pose.x:{},pose.y:{},pose.z:{},pose.rx:{},pose.ry:{},pose.rz:{}".format(
        recg_res.pick_id, recg_res.modelid, recg_res.isvalid,
        recg_res.pose.x,recg_res.pose.y,recg_res.pose.z,
        recg_res.pose.rx, recg_res.pose.ry, recg_res.pose.rz,
    ))

    '断开相机'
    cam.disconnect()

