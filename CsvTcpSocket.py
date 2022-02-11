#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Breif    : Socket相机连接类
@Project  ：CsvMasterSdk
@File     ：CsvTcpSocket.py
@Author   ：HORSETAIL
@Date     ：2022/2/9 15:49
@Company  : Shenzhen Cosmos Vision Tech Co., Ltd
@Copyright: Copyright@Cosmos Vision Tech.All Rights Reserved.
"""
import datetime
import logging
import socket
import sys
import threading

class CsvTcpClient:
    """
    客户端
    """

    def __init__(self, ip="127.0.0.1", port=549001):
        """
        初始化参数
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.addr = (ip, port)
        self.event = threading.Event()
        self.recv_data = ""

    def __del__(self):
        """
        析构函数
        """
        self.stop()

    def start(self):
        """
        连接socket
        :return:
        """
        try:
            self.sock.connect(self.addr)
        except (socket.timeout, socket.error) as e:
            logging.warning("新TCP客户端连接失败： ip 和 port:{}".format(self.addr))
            #self.sock.close()
            return False
        # 准备接收数据，recv是阻塞的，启动新的线程
        logging.warning("新TCP客户端连接成功： ip 和 port:{}".format(self.addr))
        return True

    def recv(self):
        """
        接收数据
        :return:
        """
        try:
            self.recv_data = self.sock.recv(1024)  # 阻塞
        except Exception as e:
            logging.warning(e)  # 有任何异常保证退出
            return
        logging.warning("接收命令（相机->SDK）：{}".format(self.recv_data.decode()))
        return self.recv_data

    def send(self, msg: str):
        """
        发送数据
        :param msg: 消息字符串
        :return:
        """
        data = "{}\n".format(msg.strip()).encode()
        self.sock.send(data)
        logging.warning("发送命令（SDK->相机）：{}".format(msg.strip()))

    def stop(self):
        """
        关闭socket
        :return:
        """
        isclose = getattr(self.sock, '_closed', False)
        #print("socket status:{}".format(isclose))
        if isclose == True:
            return
        logging.warning("{} 断开".format(self.addr))
        self.sock.send("quit".encode())
        self.sock.close()

class CsvTcpServer:
    """
    CsvTcpServer服务器
    """

    def __init__(self, ip="127.0.0.1", port=59001):  # 启动服务
        """
        初始化参数
        """
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event = threading.Event()

        self.clients = {}  # 客户端
        self.conns = {}  # 客户端Socket
        self.conn = socket.socket()

        self.recv_data_str = ""

    def start(self):
        """
        连接socket
        :return:
        """
        try:
            print(self.addr)
            self.sock.bind(self.addr)
            self.sock.listen(1)
            # accept会阻塞主线程，所以开一个新线程
            threading.Thread(target=self._accept, name='accept', daemon=True).start()

        except self.sock.error as msg:
            logging.warning("新TCP服务器准备失败： ip 和 port:{}".format(self.addr))
            return False
        # 准备接收数据，recv是阻塞的，启动新的线程
        logging.warning("新TCP服务器就绪,ip 和 port:{}".format(self.addr))
        return True

    def stop(self):
        """
        关闭soket
        :return:
        """
        for c in self.clients.values():
            c.close()
        self.sock.close()
        self.event.wait(3)
        self.event.set()

    def _accept(self):
        """
        监听客户端接入
        :return:
        """
        while not self.event.is_set():  # 多人连接

            self.conn, client = self.sock.accept()  # 阻塞

            f = self.conn.makefile(mode='rw')
            self.clients[client] = f
            self.conns[client] = self.conn

            data = "{}".format("New Connection").encode()
            self.conn.send(data)
            
            logging.warning("新客户端连接到服务器，IP和端口：{}-{}".format(self.conn, client))
            
            
            # recv 默认阻塞,每一个连接单独起一个recv线程准备接收数据
            threading.Thread(target=self._recv, args=(f, client), name='recv', daemon=True).start()
            # threading.Thread(target=self._recv, args=(f, client), name='recv',daemon=True).start()

    def _recv(self, f, client):  # 接收客户端数据
        """
        接收数据
        :param f: 数据流
        :param client: 客户端
        :return:
        """
        while not self.event.is_set():
            try:
                # data = f.readline()
                data = self.conns[client].recv(8192)
                if len(data) == 0:
                    data = 'quit'
            except Exception:
                data = 'quit'
            finally:
                msg = data.strip()
                # Client通知退出机制
                if msg == 'quit':
                    f.close()
                    self.clients.pop(client)
                    self.conns.pop(client)
                    logging.warning('{} quit'.format(client))
                    break

            msg = "{:%Y/%m/%d %H:%M:%S} {}:{}\n{}\n".format(datetime.datetime.now(), *client, data)
            logging.warning(msg)

            command_str = data.strip()

            self.recv_data_str = command_str

    def recv(self):
        """
        接收数据
        :return:
        """
        try:
            self.recv_data = self.conn.recv(1024).decode().strip()  # 阻塞
        except Exception as e:
            logging.warning(e)  # 有任何异常保证退出
            return

        # print(type(msg),msg)
        logging.warning("{}".format(self.recv_data))
        return self.recv_data

    def send(self, msg: str):
        """
        发送消息
        :param msg: 消息
        :return:
        """
        data = "{}".format(msg.strip()).encode()
        logging.warning(data)
        self.conn.send(data)

        self.recv_data_str = "WartingData";
