# -*- coding:utf-8 -*-
"""
File: bigpipe_config.py
Author: chukexin
Date: 2022/09/24
Brief: bigpipe访问地址
"""

SAMPLE_PUSH_BIGSEARCH_CONGIF = {
    "online": {
        "webservice": "bns://group.sample.Bigpipe.all:http",   # baidu BNS
        "user": "sample-spider",
        "passwd": "sample-spider",
        "pipe": "sample-spider-pipe",
        "token": "$1$asdfghjkertyui",
        "root_path": "/bigpipe_sandbox_new/",
    },
    "se": {
        "webservice": "list://10.xx.xx.xx:2181,10.xx.xx.xx:2182,10.xx.xx.xx:2183",
        "user": "sample-spider",
        "passwd": "sample-spider",
        "pipe": "sample-spider-pipe",
        "token": "$1$asdfghjkertyui",
        "root_path": "/bigpipe_sandbox_new/",
    },
}
