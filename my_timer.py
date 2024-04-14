import time
from my_config import config

class MyTimer:
    def __init__(self, interval=config.Interval):
        self.interval = interval
        self.record = {} # 记录每个帧发送的时间，key=seq_num, value=发送时间

    def set(self, seq_num):
        # 开启seq_num计时器
        self.record[seq_num] = time.time()

    def timeout(self, seq_num)->bool:
        # 判断seq_num是否超时
        if seq_num not in self.record:
            return False
        return time.time() - self.record[seq_num] > self.interval