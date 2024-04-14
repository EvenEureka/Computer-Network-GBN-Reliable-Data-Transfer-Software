'''
server端应该实现的功能:
    解析PDU数据帧,提取出头部,分析发送方和接收方的地址和端口。
    维护用户的ip地址表,根据表格转发PDU数据帧。
'''

import socket
import my_PDU
from my_config import config

# server类的实现，起到转发作用
class MyServer:
    def __init__(self, ip, port):
        self.server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ip=ip
        self.port=port
        self.PDUSize=config.PDUSize
        self.IP_PORT=(ip, port)
        self.server_socket.bind(self.IP_PORT)
        # 读取用户ip
        self.client_ips=[]
        self.client_ips_path='./data/127.0.0.1/clients.txt'
        with open(self.client_ips_path, 'r') as f:
            for line in f:
                self.client_ips.append(line.strip())

    def start(self):
        print('-------server has been successfully started!-------')
        while True:
            data, addr=self.server_socket.recvfrom(self.PDUSize)
            # 解码数据
            header, raw_data = my_PDU.decode_PDU(data)
            # 若源ip不在自己的用户ip表里 (表示一个未注册的用户上线)：更新用户表
            source_ip = header.source_addr[0]
            if source_ip not in self.client_ips:
                self.client_ips.append(source_ip)
                with open(self.client_ips_path, 'a') as f:
                    f.write(source_ip+'\n')
            # 若源ip在自己的用户ip表里(用户已注册):
            if source_ip in self.client_ips:
                # 转发数据
                dest_ip = header.dest_addr[0]
                if dest_ip in self.client_ips:
                    self.client_ips.append(dest_ip)
                    with open(self.client_ips_path, 'a+') as f:
                        f.write(dest_ip+'\n')   
                    
                print(f'收到 {source_ip} 给 {dest_ip} 的信息')
                # 转发数据
                # self.server_socket.sendto(data,header.dest_addr)
                self.server_socket.sendto(data, (dest_ip, header.dest_addr[1]))
            
            # 若源ip不在自己的用户ip表里：
            elif source_ip not in self.client_ips:
                print(f'未注册用户 {source_ip} 尝试发送信息')
                # 丢弃数据
                pass
        print('-------server has been successfully shut down!-------')
        self.server_socket.close()