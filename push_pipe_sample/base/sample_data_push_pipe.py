#-*- coding:utf-8 -*-
"""
Authors: chukexin(chukexin)
Date:    2020/11/11 14:36
File:    sample_data_push_pipe.py
Desc:    向bigpipe推送数据
"""

import time
import hashlib
import json
import sys
import http_query
import bns
from  conf.bigpipe_config import SAMPLE_PUSH_BIGSEARCH_CONGIF  as bigpipe_config
reload(sys)
sys.setdefaultencoding('utf-8')

class SampleDataPushPipe(object):
    def __init__(self, env):
        self.bigpipe_conf = bigpipe_config[env["bp_env"]]
        self.bns = bns.BNS(self.bigpipe_conf["webservice"])

    def publish(self, data):
        """
        发布数据到bigpipe
        """
        path = self.bigpipe_conf["root_path"] + self.bigpipe_conf["pipe"]
        url = self.bns.get_url() + path
        token = self.bigpipe_conf['token']
        expires = str(int(round(time.time())) + 30)
        sign = hashlib.md5(expires + token).hexdigest()
        param = {
            'method': 'publish',
            "expires": expires,
            "username": self.bigpipe_conf["user"],
            "sign": sign,
            'assigntype': 1,
            "msg_guid": expires + "1",
            "message": json.dumps(data),
        }
        print(url)
        print(param)
        print("\n")
        ok, res = http_query.request_api_post_form(url, param)
        if ok and res.get("status", -1) == 0:
            return True, res
        else:
            return False, res

    def topic_fetch(self, start_pos, num=1, interval=300):
        """
        # queueFetch 从topic中receive一个数据包
        # start_pos: 消息起始位置
        # num: 获取消息数
        # interval: 签名有效时间，将当前时间戳加上该值，即是服务器可接受的处理截止时间。
        # return mix bool or dict
        # data样例: {'status':'','messages':[]}
        #"""
        path = '/rest/pipe/%s' % self.bigpipe_conf["pipe"]
        url = self.bns.get_url() + path
        token = self.bigpipe_conf['token']
        expires = str(int(round(time.time())) + 30)
        sign = hashlib.md5(expires + token).hexdigest()
        params = {
            'method': "fetch",
            "expires": expires,
            "username": self.bigpipe_conf["user"],
            "sign": sign,
            'pipelet': 1,
            "id": start_pos
        }
        params["batch"] = num
        ok, res = http_query.request_api_post_form(url, params)
        if ok:
            data = res.get("messages", [])
            return True, data
        return False, res

    def process(self, packet):
        """接收数据，打包，发送"""
        loc = packet.get("loc", packet.get("@id")) 
        method = packet.get("method", "ADD")
        tag = packet.get("tag", "Medical")      # 资源类型，是否医疗
        new_packet = {}
        
        # 预设值 需要传入参数 tag，eventType， verify_result
        new_packet["tag"] = tag
        new_packet["eventType"] = "published" # 执行类型 包含审核通过：published；审核拒绝：rejected；下线数据：deleted
        verify_result = "1"                   # 执行信息，需要跟eventType并行，1:新增 2:删除
        if method == "DEL":
            new_packet["eventType"] = "deleted"
            verify_result = "2"

        str_data = packet["data"].decode('gb18030').encode('utf8')
        data = json.loads(str_data)
        new_packet["logid"] = packet["Logid"]
        new_packet["timestamp"] = int(time.time())
        top1_data = {
            "verify_result": verify_result,
            "url": loc,
            "data": json.dumps(data.get("data", {}).get("display", {})),
            "submit_time": int(time.time()),    # 资源提交时间
            "verify_time": int(time.time()),    # 资源审核通过时间
            "verify_conclusion": "",            # 结论信息，为空即可
        }
        new_packet["top1_data"] = top1_data
        ok, msg = self.publish(new_packet)
        if ok == True:
            print("loc: %s, method: %s, resp:(ok:%s, msg:%s)" % (loc, method, ok, msg))
        else:
            print("loc: %s, method: %s, resp:(ok:%s, msg:%s)" % (loc, method, ok, msg))

