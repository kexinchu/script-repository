#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: send_kafka.py
Author: chukexin
Date: 2022/09/25
Desc: 将指定数据推送kafka
"""
import sys
import json
import time
import logging
import traceback
from kafka import KafkaProducer
from ulpack import ULPacket

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(".")


class ProductSender(object):
    """
    将数据发送到 product
    """

    def __init__(self, env):
        """
        构造函数
        需要提供kafka的 IP:port list + topic name
        """
        self.topic_name = 'sample'
        self.brokers = '10.xx.xx.xx:8014,10.xx.xx.xx:2053'
        self.producer = KafkaProducer(bootstrap_servers=self.brokers.split(','))
        self.rep_count = 3
        self.env = env

    def __del__(self):
        """del"""
        self.producer.stop()

    def padding_struct(self, display):
        """把结构补上"""
        display['loc'] = self.loc
        packet = {
            'loc': self.loc,
            'data': {
                'loc': self.loc,
                'display': display
            }
        }
        return packet

    def process(self, loc, data, method):
        """处理方法"""
        code, result = 0, ""
        try:
            self.loc = loc
            # 补齐结构
            body = self.padding_struct(data)
            # 打包
            packet = self.pack(body, method)
            if not packet:
                return 1, 'pack failed'
            # 发送
            response = self.producer.send(self.topic_name, str(packet), loc.encode('utf8'))
            try:
                rst_str = response.get(timeout=10)
                result = "%s send to product success" % self.loc
                logging.info(result)
            except:
                logging.error('send loc fail, loc: %s' + self.loc)
        except:
            result = json.dumps(traceback.format_exc())
            code = 2
            logging.error("id: %s %s" % (loc, result))
        finally:
            logging.info("id: %s, code: %d, result: %s" % (loc, code, result))

        return code, packet

    def pack(self, data, method):
        """pack ULPacket"""
        if not self.env.get('product') or not self.env.get('siteid'):
            return None
        body = json.dumps(data).encode('gb18030')
        pack = ULPacket()
        
        # 下游kafka 依赖的信息 (仅代表我的样例业务)
        pack['product'] = self.env['product'].encode('utf8')
        pack['site_id'] = str(self.env['siteid'])
        pack['user'] = self.env.get('user', 'sample').encode('utf8')
        pack['pwd'] = self.env.get('pwd', 'sample_for_kafka_sender').encode('utf8')
        
        pack['method'] = method
        pack['Method'] = pack['method']
        pack['Url'] = self.loc.encode('utf8')
        pack['loc'] = self.loc.encode('utf8')
        pack['PageLength'] = str(len(body)).encode('gb18030')
        pack['Longsign1'] = pack['site_id']
        pack['Longsign2'] = str(int(time.time()))
        pack.body = body

        return str(pack)
