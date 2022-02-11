#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Brief    : 相机控制类
@Project  ：CsvMasterSdk
@File     ：CsvCamController.py
@Author   ：HORSETAIL
@Date     ：2022/2/9 15:49
@Company  : Shenzhen Cosmos Vision Tech Co., Ltd
@Copyright: Copyright@Cosmos Vision Tech.All Rights Reserved.
"""

import logging
from CsvData import CsvPose, CsvRecgInfo
from CsvTcpSocket import CsvTcpClient


class CsvCamController:
    def __init__(self, ip="127.0.0.1", port=549002):
        """
        构造函数
        :param ip:相机ip地址
        :param port:相机端口
        """
        # 对应的视觉客户端
        self.tcp_client = CsvTcpClient(ip, port)
        # self.cam_tcp_client.start()

    def __del__(self):
        """
        析构函数
        """
        self.tcp_client.stop()

    def connect(self):
        """
        启动相机连接
        @rtype: object
        """
        return self.tcp_client.start()

    def disconnect(self):
        """
        断开相机连接
        :return:
        """
        return self.tcp_client.stop()

    def openVideo(self):
        """
        打开视频
        :return: 成功返回：True，失败返回：False
        """
        command = "OpenVideo"
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_OpenVideo") >= 0:
            return False
        return True

    def closeVideo(self):
        """
        关闭视频
        :return: True 成功，False 失败
        """
        command = "CloseVideo"
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_CloseVideo") >= 0:
            return False
        return True

    def calShootSave(self, pose):
        """
        采集标定图像
        :param pose: 机器人法兰姿态，如果标定无机械臂，则可置为CsvPose()
        :return: 成功返回：YES_CalShootSave, 失败返回：NO_CalShootSave
        """
        command = "CalShootSave,X{},Y{},Z{},RX{},RY{},RZ{}".format(pose.x, pose.y, pose.z, pose.rx, pose.ry, pose.rz)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_CalShootSave") >= 0:
            return "NO_CalShootSave"
        return "YES_CalShootSave"

    def setParam(self, id, val1, val2):
        """
        设置视觉和相机参数
        :param id: 参数ID号
        :param val1: 设置值1
        :param val2: 设置值2
        :return: 成功返回：YES_SetParam, 失败返回：NO_SetParam
        """
        command = "SetParam,{},{},{}".format(id, val1, val2)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_SetParam") >= 0:
            return "NO_SetParam"
        return "YES_SetParam"

    def getParam(self, id):
        """
        设置视觉和相机参数
        :param id: 参数ID号
        :return: 成功返回：[val1 val2], 失败返回:NO_SetParam
        """
        command = "GetParam,{}".format(id)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_GetParam") >= 0:
            return "NO_GetParam"

        recv_data_array = recv_data.split(',')

        count = len(recv_data_array)
        val1 = -1000000
        val2 = -1000000
        if count == 1:
            val1 = float(recv_data_array[0])
        if count == 2:
            val1 = float(recv_data_array[0])
            val2 = float(recv_data_array[1])
        return [val1, val2]

    def switchModel(self, model_name):
        """
        切换模型
        :param model_name: 模型名称
        :return: 成功返回：YES_SwitchModel, 失败返回：NO_SwitchModel,失败原因
        """
        command = "SwitchModel,{}".format(model_name)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_SwitchModel") >= 0:
            return recv_data
        return "YES_SwitchModel"

    def recgGrasp(self, pose, model_type="ALL"):
        """
        识别抓取
        :param pose: 当前法兰姿态
        :param model_type: 模型类型
        :return: 成功返回：识别结果信息，失败返回：NO_RecgGrasp
        """
        recg_info = CsvRecgInfo()
        command = "RecgGrasp,{},{},{},{},{},{},{}".format(pose.x, pose.y, pose.z, pose.rx, pose.ry, pose.rz, model_type)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_RecgGrasp") >= 0:
            return recg_info
        recv_data = recv_data.split(',')
        recg_info.pose.x = float(recv_data[0].replace("X", ""))
        recg_info.pose.y = float(recv_data[1].replace("Y", ""))
        recg_info.pose.z = float(recv_data[2].replace("Z", ""))
        recg_info.pose.rx = float(recv_data[3].replace("RX", ""))
        recg_info.pose.ry = float(recv_data[4].replace("RY", ""))
        recg_info.pose.rz = float(recv_data[5].replace("RZ", ""))
        recg_info.pick_id = -1
        recg_info.modelid = recv_data[6]
        recg_info.isvalid = True

        return recg_info

    def recg(self, pose, model_type="ALL"):
        """
        仅识别
        :param pose: 当前法兰姿态,如果没有机器人法兰值，那么可以置为CsvPose()
        :param model_type: 模型类型
        :return:
        """
        recg_info = CsvRecgInfo()
        command = "Recg,{},{},{},{},{},{},{}".format(pose.x, pose.y, pose.z, pose.rx, pose.ry, pose.rz, model_type)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().strip().decode()

        if recv_data.find("NO_Recg") >= 0:
            return recg_info

        recv_data = recv_data.split(',')

        recg_info.pose.x = float(recv_data[0].replace("X", ""))
        recg_info.pose.y = float(recv_data[1].replace("Y", ""))
        recg_info.pose.z = float(recv_data[2].replace("Z", ""))
        recg_info.pose.rx = float(recv_data[3].replace("RX", ""))
        recg_info.pose.ry = float(recv_data[4].replace("RY", ""))
        recg_info.pose.rz = float(recv_data[5].replace("RZ", ""))
        recg_info.pick_id = -1
        recg_info.modelid = recv_data[6]
        recg_info.isvalid = True

        return recg_info

    def addGrasp(self, teach_recg_grasp):
        """
        添加示教抓取点
        :param teach_recg_grasp: 示教抓取信息
        :return: 成功返回：YES_AddGrasp, 失败返回：NO_AddGrasp
        """
        command = "AddGrasp,{},{},{},{},{},{},{}\n".format(teach_recg_grasp.flange_pose.x,
                                                           teach_recg_grasp.flange_pose.y,
                                                           teach_recg_grasp.flange_pose.z,
                                                           teach_recg_grasp.flange_pose.rx,
                                                           teach_recg_grasp.flange_pose.ry,
                                                           teach_recg_grasp.flange_pose.rz,
                                                           teach_recg_grasp.tool)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().decode()

        if recv_data.find("YES_AddGrasp") >= 0:
            logging.warning("添加示教点成功")
        else:
            logging.error("添加示教点失败")

        return recv_data

    def removeGrasp(self, id):
        """
        删除示教抓取点
        :param id: 示教ID号
        :return: 成功返回：YES_RemoveGrasp, 失败返回：NO_RemoveGrasp
        """
        command = "RemoveGrasp,{}".format(id)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().decode()

        if recv_data.find("YES_RemoveGrasp") >= 0:
            logging.warning("删除示教点成功")
        else:
            logging.error("删除示教点失败")

        return recv_data

    def eulerTest(self, x, y, z):
        """
        欧拉系统测试函数1
        :param x: 法兰x
        :param y: 法兰y
        :param z: 法兰z
        :return: 成功返回：相关数值，失败返回：NO_EulerTest
        """
        command = "EulerTest,{},{},{}".format(x, y, z)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().decode()

        if recv_data.find("NO_EulerTest") >= 0:
            logging.warning("欧拉系统测试失败")
        else:
            logging.error("欧拉系统测试成功")

        return recv_data

    def eulerTest(self, x, y, z, rx, ry, rz):
        """
        欧拉系统测试函数2
        :param x: 法兰x
        :param y: 法兰y
        :param z: 法兰z
        :param rx: 法兰rx
        :param ry: 法兰ry
        :param rz: 法兰rz
        :return: 成功返回：输出指定机器人坐标的旋转矩阵与位置值，失败返回：NO_EulerTest
        """
        command = "EulerTest,{},{},{},{},{},{}".format(x, y, z, rx, ry, rz)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().decode()

        if recv_data.find("NO_EulerTest") >= 0:
            logging.warning("欧拉系统测试失败")
        else:
            logging.error("欧拉系统测试成功")

        return recv_data

    def eulerTest(self, x, y, z, rx, ry, rz, r00, r10, r20, r01, r11, r21, r02, r12, r22):
        """
        欧拉系统测试函数3
        :param x: 法兰x
        :param y: 法兰y
        :param z: 法兰z
        :param rx: 法兰rx
        :param ry: 法兰ry
        :param rz: 法兰rz
        :param r00:矩阵元素
        :param r10:矩阵元素
        :param r20:矩阵元素
        :param r01:矩阵元素
        :param r11:矩阵元素
        :param r21:矩阵元素
        :param r02:矩阵元素
        :param r12:矩阵元素
        :param r22:矩阵元素
        :return: 成功返回：输出指定位置与旋转矩阵的机器人坐标（与前一个命令刚好相反），失败返回：NO_EulerTest
        """
        command = "EulerTest,{},{},{},{},{},{}".format(x, y, z, rx, ry, rz,
                                                       r00, r10, r20,
                                                       r01, r11, r21,
                                                       r02, r12, r22)
        self.tcp_client.send(command)
        recv_data = self.tcp_client.recv().decode()

        if recv_data.find("NO_EulerTest") >= 0:
            logging.warning("欧拉系统测试失败")
        else:
            logging.error("欧拉系统测试成功")

        return recv_data
