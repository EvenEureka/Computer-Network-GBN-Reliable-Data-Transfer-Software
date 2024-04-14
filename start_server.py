from my_server import MyServer
from my_config import config

# 由此文件开启服务器端
def main_server():
    server=MyServer(config.ServerIP, config.UDPPort)
    server.start()

        
if __name__=='__main__':
    main_server()