# -*- coding: utf-8 -*- 
# @Time : 2021/7/13 下午7:45 
# @Author : Jianglin Zhang 
# @File : publish.py

# coding:utf-8
import datetime
import time
import redis

number_list = ['300033', '300032', '300031', '300030']
signal = ['1', '-1', '1', '-1']

#rc = redis.StrictRedis(host='192.168.108.103', port='6379', db=3, password='')
rc = redis.StrictRedis(host='192.168.108.103', port='6379', db=3)
for i in range(len(number_list)):
    value_new = str(number_list[i]) + ' ' + str(signal[i])+str(datetime.datetime.now())
    rc.publish("liao", value_new)
    time.sleep(3)