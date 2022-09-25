# -*- coding: utf-8 -*-
"""
# http请求
"""
import requests
import urllib
import traceback
import json
import time
import logging 

def request_api_post_form(url, params, timeout=3):
    """
    # 基础请求服务: post 方法
    # url：请求api
    # params： 请求参数，{}（字典格式）
    # """
    result = ""
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    for i in range(3):
        try:
            begin_time = int(time.time() * 1000)
            r = requests.post(url, data=params, timeout=timeout, headers=headers)
            res = r.json()
        except:
            end_time = int(time.time() * 1000)
            result = json.dumps(traceback.format_exc())
            logging.error("request error，use time: %sms, times %s, url: %s, msg: %s" % \
                (end_time - begin_time, i, url, result))
            time.sleep(1)
            continue
        end_time = int(time.time() * 1000)
        logging.info("request use time: %sms" % (end_time - begin_time))
        if r.status_code != 200:
            result = r.text
            time.sleep(1)
            continue
        return True, res
    return False, result