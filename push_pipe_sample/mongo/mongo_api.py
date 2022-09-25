#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
########################################################

"""
File: mongo_api.py
Desc: Mongo HTTP API
Author: chukexin
"""

import sys
import json
import urllib
import urllib2
import logging
import traceback


class MongoAPI(object):
    """Mongo HTTP API"""

    def __init__(self, conf, **kwargs):
        """init"""
        self.conf = conf
        self.port = self.conf.get('port')
        self.host = self.conf.get('hostname')
        self.table = self.conf.get('table')

        if self.port:
            self.host += ':' + str(self.port)

        self.user = self.conf.get('user')
        self.passwd = self.conf.get('passwd')
        self.logger = kwargs.get('logger', logging)

    def request(self, action, params, data=None):
        """request"""
        code, msg, result = -1, '', []
        params_kv = {}
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Basic ' + ("%s:%s" % (self.user, self.passwd)).encode(
                "base64").strip()
        }

        try:
            url = "http://%s/%s/%s" % (self.host, action, self.table)

            for key, value in params.items():
                if isinstance(value, dict):
                    # params_kv[key] = json.dumps(value)
                    params_kv[key] = json.dumps(value, separators=(',', ':'))
                else:
                    params_kv[key] = value

            if len(params_kv) > 0:
                url += '?' + urllib.urlencode(params_kv)

            if data and len(data) > 0:
                request = urllib2.Request(url=url, data=json.dumps(data), headers=headers)

            else:
                request = urllib2.Request(url=url, headers=headers)

            for x in range(5):
                try:
                    response = urllib2.urlopen(request, None, 500)
                    if response.code == 200:
                        response_text = response.read()
                        response_json = json.loads(response_text)
                        code = response_json.get('errno', -1)
                        msg = response_json.get('errmsg', '')

                        if action == 'count':
                            result = response_json.get('count', 0)
                        else:
                            result = json.loads(response_json.get('data', '[]'))
                        break

                except Exception as e:
                    msg = str(e)
                    print >> sys.stderr, e

        except Exception as e:
            msg = str(e)
            print >> sys.stderr, e

        if code != 0:
            log_msg = 'Mongo API host:%s action:%s table:%s params:%s code:%s msg:%s' % (
                self.host, action, self.table, json.dumps(params_kv), str(code), msg)
            self.logger.info(log_msg)

        return code, msg, result

    def get(self, **params):
        """get"""
        return self.request('get', params)

    def put(self, data):
        """put"""
        return self.request('put', {}, data)

    def delete(self, where):
        """put"""
        if len(where) == 0:
            return -1, '', []
        return self.request('delete_where', {}, where)

    def mod(self, data):
        """put"""
        return self.request('mod', {}, data)

    def count(self, where):
        """count"""
        return self.request('count', {'where': where})


# if __name__ == "__main__":
#     mongo = MongoAPI({
#         'hostname': 'mongo-restapi-sample.www.exe.serv',
#         'port': 8080,
#         'user': 'chukexin',
#         'passwd': 'sample',
#         'table': 'mongo_data_test'
#     })

#     try:
#         loc = "http://mip.qiuyi.cn/audio/detail?id=1423"
#         code, msg, res = mongo.get(where={'@id': loc})
#         print(code, msg, res)
#     except:
#         print("loc:%s\n%s" % (loc, traceback.format_exc()))
    
