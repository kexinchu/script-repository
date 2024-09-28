#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
from mongo.mongo_api import MongoAPI
from base.sample_data_push_pipe import SampleDataPushPipe
from conf.mongo_config import MONGO_SAMPLE_API_PATH as mongo_config

loc_json_dict = {}
def get_url_json_from_file(path_list):
    """
    @param path: 待读取json文件地址
    """
    for file_path in path_list:
        with open(file_path, 'r') as fr:
            while(True):
                line=fr.readline()
                if not line:
                    break
            
                line = line.strip()
                url_tag = line.split("\t")
                loc_json_dict[url_tag[0].strip("\n")] = url_tag[1]
# sample
# loc_json_dict = {"http://muzhi.baidu.com/content_production/W8FKt51YnD.html": ""}

def get_data_from_mongoDB_and_push_pipe():
    """
    医疗资源，通过读医疗沉淀库来获取存量数据
    """
    mongo_proxy = MongoAPI(mongo_config['sample_data_online'])
    for loc in loc_json_dict.keys():
        # 查mongo数据
        code, msg, data = mongo_proxy.get(where={'@id': loc})
        if code != 0 or not data:
            print('query mongo fail, msg %s' % msg)
            continue
        if isinstance(data, list) and len(data) == 0:
            print('query mongo fail, loc does not exist')
            continue
        json_line = data[0]         # 存量数据的json_line

        # merge json 数据
        merge(json_line, loc_json_dict[loc])
        push_bigpipe(json_line)


def merge(json_line, json_data):
    """
    merge 文件数据 和 mongoApi结果; 按key merge
    """
    whitelist_fields = [
        'loc',
        'query',
        'title',
        'data',
    ]
    add_json_data = json.loads(json_data)

    for key in add_json_data:
        if key in whitelist_fields:
            json_line[key] = add_json_data[key]
    

def push_bigpipe(json_line):
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
        "bp_env": "online",
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


if __name__ == "__main__":
    in_file = sys.argv[1]

    f_qp_loc = open(in_file, 'r')

    get_url_json_from_file(in_file)
    get_data_from_mongoDB_and_push_pipe()