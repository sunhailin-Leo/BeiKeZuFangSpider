# -*- coding: utf-8 -*-
import csv
import uuid
import logging

# 第三方库
# pymongo
import pymongo
from pymongo.errors import ConnectionFailure

# Scrapy
from scrapy.conf import settings

# 日志
logger = logging.getLogger(__name__)


class BeikezufangspiderPipeline(object):
    def __init__(self):
        """
        Pipeline的配置
        """
        # MongoDB配置
        self._host = settings.get("MONGODB_HOST")
        self._port = settings.get("MONGODB_PORT")
        self._user = settings.get("MONGODB_USER")
        self._pass = settings.get("MONGODB_PASS")
        self._db_name = settings.get("MONGODB_DB_NAME")
        self._col_name = settings.get("MONGODB_COL_NAME")

        # Kafka配置
        self._is_kafka = settings.get("KAFKA_PIPELINE")
        if self._is_kafka:
            self._kafka_hosts = settings.get("KAFKA_IP_PORT")
            self._kafka_topic = settings.get("KAFKA_TOPIC_NAME")

        # 初始化
        self.client = None
        self.db = None
        self.collection = None
        self.conn_flag = False

        # csv文件的位置,无需事先创建
        self._is_csv = settings.get("CSV_EXPORTER")
        if self._is_csv:
            self._csv_path = settings.get("CSV_DEFAULT_PATH")
            self.csv_file = None
            self._csv_header = [
                "区域",
                "租房链接",
                "房源名称",
                "房屋基本信息",
                "房屋来源",
                "发布时间",
                "房屋特点",
                "最低价(元/月)",
                "最高价(元/月)"
            ]
            self._store_file = \
                '{}export_{}.csv'.format(
                    self._csv_path,
                    str(uuid.uuid4()).replace("-", "")
                )

    def open_spider(self, spider):
        """
        启动爬虫之后的方法
        :param spider: 爬虫对象
        :return: 无返回值
        """
        if spider.name == "BeiKeErShouFang":
            if self._is_csv is not True:
                self.client = pymongo.MongoClient(
                    host=self._host,
                    port=self._port,
                    username=self._user,
                    password=self._pass,
                    socketTimeoutMS=3000
                )
                try:
                    # 判断是否能够连接上MongoDB
                    self.client.admin.command('ismaster')
                    self.db = self.client[self._db_name]
                    self.collection = self.db[self._col_name]
                except ConnectionFailure:
                    logger.error("MongoDB服务未启动, 使用CSV进行导出数据!")
                    self.conn_flag = False
                finally:
                    logger.debug("CSV文件存储位置: {}".format(self._store_file))
                    self.csv_file = csv.writer(open(self._store_file, 'w', newline=''))
                    self.csv_file.writerow(self._csv_header)
            else:
                # 使用CSV导出
                self.conn_flag = False
                logger.debug("CSV文件存储位置: {}".format(self._store_file))
                self.csv_file = csv.writer(open(self._store_file, 'w', newline=''))
                self.csv_file.writerow(self._csv_header)

    def close_spider(self, spider):
        """
        关闭爬虫之后的方法
        :param spider: 爬虫对象
        :return: 无返回值
        """
        if spider.name == "BeiKeErShouFang":
            if self._is_csv is not True:
                self.client.close()

    def process_item(self, item, spider):
        """
        写入数据库中
        :param item: 数据条目
        :param spider: 爬虫对象
        :return: 返回显示item
        """
        if spider.name == "BeiKeErShouFang":
            if self.conn_flag:
                try:
                    self.collection.insert(item)
                    return item
                except Exception as err:
                    logger.error(err)
                    # 结束爬虫
                    spider.crawler.engine.close_spider(spider, "MongoDB insert error! Reason: {}".format(str(err)))
            else:
                data = list(item.values())
                # 弹出ID列
                data.pop(0)
                # 弹出封面图
                data.pop(2)
                data[-2] = ",".join(data[-2])
                data_tail = data.pop()
                data_tail = [int(d.replace("元/月", "")) for d in data_tail]
                data.extend(data_tail)
                # 写入数据
                try:
                    self.csv_file.writerow(data)
                except UnicodeEncodeError:
                    logger.debug("解码错误!存在特殊符号无法解码!URL:{}".format(data[1]))
                return item
