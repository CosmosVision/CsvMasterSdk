#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Brief    : 常用数据类型
@Project  ：CsvMasterSdk
@File     ：CsvData.py
@Author   ：HORSETAIL
@Date     ：2022/2/9 15:49
@Company  : Shenzhen Cosmos Vision Tech Co., Ltd
@Copyright: Copyright@Cosmos Vision Tech.All Rights Reserved.
"""


class CsvPosition:
    def __init__(self, x=0, y=0, z=0, name=""):
        """
        位置点
        """
        self.x = x
        self.y = y
        self.z = z
        self.name = name

    def isZero(self):
        if abs(self.x) < 1e-6 and abs(self.y) < 1e-6 and abs(self.z) < 1e-6:
            return True


class CsvPose:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0, name=""):
        """
        位姿
        """
        self.x = x
        self.y = y
        self.z = z
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.name = name

    def isZero(self):
        if abs(self.x) < 1e-6 and abs(self.y) < 1e-6 and abs(self.z) < 1e-6 and \
                abs(self.rx) < 1e-6 and abs(self.ry) < 1e-6 or abs(self.rz) < 1e-6:
            return True


class CsvRecgInfo:
    def __init__(self):
        """
        识别信息
        """
        self.pose = CsvPose()
        self.pick_id = 0
        self.modelid = 0
        self.isvalid = False


class CsvTeachGraspInfo:
    def __init__(self):
        """
        示教抓取信息
        """
        self.flang_pose = CsvPose()
        self.recg_pose = CsvPose()
        self.tool = "T0"
        self.model_id = "M0"


class CsvPartType:
    def __init__(self):
        """
        零件类型
        """
        self.IronSeat33 = 1000
        self.IronSeat38 = 1001
        self.IronSeat42 = 1002
        self.Platen201 = 2001
        self.Platen202 = 2002


class CsvPartInfo:
    def __init__(self, part_array):
        """
        初始化
        @param part_array: 零件数组，从数据库中导出
        """
        self.ID = part_array[0]
        self.ProductSN = part_array[1]
        self.PartSN = part_array[2]
        self.AssembleOrder = part_array[3]
        self.AssembleX = part_array[4]
        self.AssembleY = part_array[5]
        self.AssembleZ = part_array[6]
        self.AssembleRX = part_array[7]
        self.AssembleRY = part_array[8]
        self.AssembleRZ = part_array[9]
        self.SpotWeldingID = part_array[10]
        self.FullWeldingID = part_array[11]
        self.PartModel = part_array[12]
        self.Note = part_array[13]
        self.WeldingNO = part_array[14]
        self.TeachWorkPose = part_array[15]
        self.TeachGraspPose = part_array[16]
