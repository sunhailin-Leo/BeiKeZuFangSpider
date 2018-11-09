# -*- coding: UTF-8 -*-
"""
Created on 2018年2月7日
@author: Leo
@file: kafka_consumer.py
"""

# Kafka Conusmer的example
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType

# client对象
client = KafkaClient(hosts="localhost:9092")

# 要用字节形式
topic = client.topics[b'BeiKeZuFang']

# 用的是get_simple_consumer做测试
consumer = topic.get_simple_consumer(
    consumer_group=b"BeiKeZuFang",
    auto_offset_reset=OffsetType.LATEST,
    reset_offset_on_start=True,
    auto_commit_enable=True,
    # auto_commit_enable=True,
    # 设置为False的时候不需要添加consumer_group，直接连接topic即可取到消息
    # 下面这个参数可以连接多个zk
    # 例如: IP地址:2181,IP地址:2182,IP地址:2183
    # zookeeper_connect=[zk的字符串]
)

for message in consumer:
    if message is not None:
        # 打印接收到的消息体的值
        data = message.value.decode("UTF-8")
        data = json.loads(data, encoding="GBK")
        print(data)
