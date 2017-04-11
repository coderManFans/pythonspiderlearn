#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017-3-31 15:19
# @Author  : coderManFans
# @Site    : redis操作工具类
# @File    : PythonMysqlTest.py
# @Software: PyCharm

import redis,logging

msg_Error = "error"

class PyRedisUtil(object):

    __pool = redis.ConnectionPool(host='127.0.0.1', port='6379')
    __conn = redis.Redis(connection_pool=__pool)


    '''
    带有过期时间的设置值
    '''
    def setex(self,key,value,expireTime):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        if str(value).strip() == "":
            logging.error("value is null ")
            return
        try:
            PyRedisUtil.conn.set(key,value,ex=expireTime)
        except:
            logging.error("redis set key="+str(key)+" error.....")

    def lpushList(self,key, *value):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        if len(value) == 0:
            logging.error("value is null ")
            return
        try:
            PyRedisUtil.__conn.lpush(key, value)
        except:
            logging.error("redis lpush error,key = " + str(key) + ",value = " + str(
                value) + " or key has exited,the operation against the key-value data structure")

    def lpopList(self,key):
        if str(key).strip() == "":
            logging.error("key is null ")
            return msg_Error
        try:
            return PyRedisUtil.__conn.lpop(key)

        except:
            logging.error("redis lpop error, key = " + key)
            return msg_Error

    def rpush(self,key,*value):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        if len(value) == 0:
            logging.error("value is null ")
            return
        try:
            PyRedisUtil.__conn.rpush(key,value)
        except:
            logging.error("redis rpush error, key = " + key+", value = "+value)

    def rpop(self,key):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        try:
            PyRedisUtil.__conn.rpop(key)
        except:
            logging.error("redis rpush error, key = " + key)

    def llen(self,key):
        if str(key).strip() == "":
            logging.error("key is null ")
            return msg_Error
        return PyRedisUtil.__conn.llen(key)

    #set 插入一个元素
    def sadd(self,key,value):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        if len(value) == 0:
            logging.error("value is null ")
            return
        PyRedisUtil.__conn.sadd(key,value)

    def get(self,key):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        return PyRedisUtil.__conn.get(key)

    # set 集合
    def smembers(self,key):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        return PyRedisUtil.__conn.smembers(key)

    # set 删除一个元素
    def srem(self,key,value):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        if str(value).strip() == "":
            logging.error("value is null ")
            return
        return PyRedisUtil.__conn.srem(key,value)

    #set 集合数量
    def scard(self,key):
        if str(key).strip() == "":
            logging.error("key is null ")
            return
        return PyRedisUtil.__conn.scard(key)


redisUtil = PyRedisUtil()

def testSet():
    for url in redisUtil.smembers("jiangbo_phd"):
        print(url)
testSet()
