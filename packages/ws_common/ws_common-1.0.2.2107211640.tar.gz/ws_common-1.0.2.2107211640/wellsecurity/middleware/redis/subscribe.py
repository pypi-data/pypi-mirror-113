# -*- coding: utf-8 -*- 
# @Time : 2021/7/13 下午7:51 
# @Author : Jianglin Zhang 
# @File : subscribe.py
# coding:utf-8
import time
import datetime
import redis

#rc = redis.StrictRedis(host='****', port='6379', db=3, password='******')
rc = redis.StrictRedis(host='192.168.108.103', port='6379', db=3)
ps = rc.pubsub()
ps.subscribe('wellsecuritymessage')  # 从liao订阅消息
for item in ps.listen():  # 监听状态：有消息发布了就拿过来
    if item['type'] == 'message':
        print(item['channel'])
        print(item['data'])
