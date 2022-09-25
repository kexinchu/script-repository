#-*- coding:utf-8 -*-
"""
Authors: chukexin
Date:    2022/09/25 
File:    update_kafka_add_del_sample.py
Desc:    推送kafka样例
"""

import sys
import json
import traceback
from send_product import KafkaSender
from conf.sender_config import PRODUCT_CONF

class updateKafkaAddDelSample(object):
    """
    更新 client
    """

    def __init__(self, env):
        self.kafka_sender = KafkaSender(PRODUCT_CONF['increase'])
        # 字段白名单 <最终需要send  kafka 的数据key列表>
        self.whitelist_fields = [
            'loc',
            'query',
            'title',
            'data',
        ]

    def process(self, loc, data, method):
        """发送更新包"""
        msg = ''
        display = self.format_data(data)
        display = self.filter_display(display)
        # append: 1 merge, 0 覆盖
        display['append'] = '0'
        display['new_key'] = '1'
        code, packet = self.kafka_sender.process(loc, display, method)
        if code == 0:
            msg = 'send kafka success: %s' % loc
            return 0, msg
        else:
            msg = 'send kafka failed: %s' % loc
            return code, msg

    def filter_display(self, display):
        """字段过滤 <按照白名单>"""
        ret = {}
        for k in display:
            if k in self.whitelist_fields:
                ret[k] = display[k]
        return ret

    def format_data(self, data):
        """格式化数据 - 业务相关 (从上游数据中解析所需数据)"""
        display = {}
        if 'data' in data:
            data_label = data['data']
            if '{' in data_label:
                data_label = json.loads(data_label)
            display['data'] = data_label
        
        if 'loc' in data:
            display['loc'] = data['loc']
        if 'query' in data:
            display['query'] = data['query']
        if 'title' in data:
            display['title'] = data['title']
        return display

if __name__ == "__main__":
    file_path = sys.argv[1]
    env = 'online'
    if len(sys.argv) > 2:
        env = sys.argv[2]
    # 初始化
    obj = updateKafkaAddDelSample(env=env)
    
    msg = ''
    for line in open(file_path, 'r'):
        line = line.strip()
        if line == '':
            continue
        try:
            # line : loc"\t"{"a":"1","b":2}
            loc, js_data = line.split("\t")
            loc = loc.strip()
            loc = loc.replace("https://", "http://")
            arr_data = json.loads(js_data)
            code, ret = obj.process(loc, arr_data, "ADD")
            if code != 0:
                print ("[ERROR]Request Failed: %s [%d] %s" % (loc, code, msg))
            else:
                print ("[NOTICE]Process Done: %s" % loc)
            # time.sleep(0.01)
        except:
            print ("EXCEPTION\t" + json.dumps(traceback.format_exc()))
            continue
