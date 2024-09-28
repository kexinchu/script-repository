#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: sample_read_file_and_push_pipe.py
Author: chukexin
Desc: 读取本地文件，推送pipe
"""

import sys
import json
from base.sample_data_push_pipe import SampleDataPushPipe

def push_bigpipe(json_line, pipe_type):
    """
    将处理之后的数据写文件
    """
    packet = {
        "loc": json_line['loc'],
        "site_id": 201873979,
        "method": "ADD",
        "Logid": "1689422193427010",
        "tag": "ZyptRealtimeBuild",
    }
    env = {
        "bp_env": pipe_type,
    }

    data = {
        "loc": json_line["loc"],
        "data": {
            "display": json_line,
        }
    }
    packet['data'] = json.dumps(data)
    packet["data"] = packet["data"].encode('gb18030')
    task = SampleDataPushPipe(env)
    task.process(packet)


def main_process(json_line, is_test):
    """
    主函数
    """
    # 处理其他逻辑
    
    # 推送bigpipe
    if is_test:
        push_bigpipe(json_line, "se")   # 沙盒pipe
    else:
        push_bigpipe(json_line, "online")

if __name__ == "__main__":
    data_file = sys.argv[1]  # B端产出的数据
    is_test = sys.argv[2]            # 是否测试行为

    # 读 B 端产出的siteplatform.data数据
    fr = open(data_file, "r")

    while True:
        line = fr.readline()
        if not line:
            # 读到文件结尾，跳出
            break

        line = line.strip()
        line_split = line.split("\t")
        if len(line_split) != 6:
            continue
        line = line_split[3]    # 有效数据
        # 资源提交时间，B端给出
        verify_time = line_split[1]
        json_line = json.loads(line)
        
        if is_test == "test":
            main_process(json_line, True)
        else:
            main_process(json_line, False)