# -*- coding: utf-8 -*-
"""
文件说明：
File   : bns.py
Authors: chukexin
Date   : 2022/9/25
Comment:
"""
import os
import time
import random
import threading


class Balancer(object):
    """
    负载均衡器
    """
    def get(self, instances):
        """
        获取实例
        :param instances:
        :return:
        """
        raise NotImplementedError


class RandomBalancer(Balancer):
    """
    随机
    """
    def get(self, instances):
        """
        获取实例
        :param instances:
        :return:
        """
        index = int(random.random() * len(instances))
        return instances[index]


class RRBalancer(Balancer):
    """
    轮询
    """
    def __init__(self):
        self._index = 0
        self._lock = threading.Lock()

    def get(self, instances):
        """
        获取实例
        :param instances:
        :return:
        """
        if self._index >= len(instances):
            self._index = 0
        instance = instances[self._index]
        with self._lock:
            self._index += 1
        return instance


class BNS(object):
    """
    bns类，保存可用机器列表，当用户获取时返回其一，支持轮询，随机的负载均衡方式
    使用demo：
    bns = BNS('bns name', 'rr/random')
    bns.get_url()  # http://10.xx.xx.xx:8012
    bns.get_instance()  # {'host': '', 'ip': '', 'port': 8012, 'status': 0}
    """
    def __init__(self, name, balance="random", interval=10, auto_start=True):
        """
        :param name: BNS name，也支持提供列表，bns://{{bns name}} 或 list://host:port,host:port
        :param balance: 支持 random（随机） rr（轮询）
        :param interval: 列表更新间隔
        """
        self.name = name
        self.bns_name = self._parse_bns(name)
        self.balance = balance
        self.interval = interval
        if balance == 'random':
            self.balancer = RandomBalancer()
        elif balance == 'rr':
            self.balancer = RRBalancer()
        else:
            self.balancer = RandomBalancer()
            self.balance = 'random'
        self.stop_flag = False
        # 若是bns，则意味着需要动态更新实例列表
        if self.bns_name:
            self.instances = self.get_instances()
            if auto_start:
                self.start()
        else:
            self.instances = self._parse_list(name)

    def _parse_bns(self, name):
        if name.startswith('bns://'):
            return name[6:]
        return None

    def _parse_list(self, name):
        if name.startswith('list://'):
            name = name[7:]
        instances = name.split(',')
        instances = [instance.split(':') for instance in instances]

        def _parse(i):
            return {
                'host': i[0],
                'ip': i[0],
                'port': i[1],
                'status': '0'
            }
        instances = [_parse(instance) for instance in instances]
        return instances

    def __del__(self):
        self.stop()

    def start(self):
        """
        启动bns自动更新
        :return:
        """
        self.stop_flag = False
        t = threading.Thread(target=self._start_thread)
        t.daemon = True
        t.start()

    def stop(self):
        """
        停止更新
        :return:
        """
        self.stop_flag = True

    def _start_thread(self):
        while self.stop_flag is False:
            time.sleep(self.interval)
            self.instances = self.get_instances()

    def get_instances(self):
        """
        查询实例 (这里使用的是针对Baidu Name Service的命名服务查询指令, 其他命名服务做相应调整)
        :return:
        """
        lines = os.popen("${命令-获取Name service下的Ip + Port}")
        instances = [line.rstrip().split() for line in lines]
        instances = [i for i in instances if i[-1] == '0']
        ret = []
        for instance in instances:
            ret.append({
                'host': instance[0],
                'ip': instance[1],
                'port': instance[2],
                'status': instance[3],
            })
        return ret

    def get_instance(self):
        """
        获取单个实例
        :return:
        """
        return self.balancer.get(self.instances)

    def get_url(self):
        """
        获取一个http协议的url
        :return:
        """
        instance = self.get_instance()
        return 'http://%s:%s' % (instance['ip'], instance['port'])
