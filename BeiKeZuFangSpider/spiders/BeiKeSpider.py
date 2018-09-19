# -*- coding: UTF-8 -*-
"""
Created on 2018年9月17日
@author: Leo
"""
import re
import uuid
from collections import OrderedDict

# Scrapy
import scrapy

# 项目内部库
from BeiKeZuFangSpider.utils.city_util import CityInfoSpider
from BeiKeZuFangSpider.utils.common_utils import DictMatching, flatten


class BeiKeScrapySpider(scrapy.Spider):
    name = "BeiKeErShouFang"

    def __init__(self, city: str, area: str, metro: str):
        """
        数据初始化
        :param city: 城市名称
        :param area: 区域名称
        :param metro: 地铁线路名称
        """
        self._area = area
        self._metro = metro

        # 启动的爬虫的URL
        self.start_urls = []

        # 城市
        if city != "":
            # 城市不能为空
            self._c = CityInfoSpider(city=city)
            self._city_info = self._c.get_city_data()
            if self._city_info[0] != "Error":
                # 存在当前城市的二手房数据
                if self._area == "" and self._metro == "":
                    # 爬取当前城市的全量数据
                    self.start_urls[0] = self._city_info[0]
                elif self._area != "" and self._metro == "":
                    dict_m = DictMatching(matching_dict=self._city_info[1], words=self._area, max_result=True)
                    self.start_urls.append(list(dict_m.dict_keys_matching()[0][1].values())[0])
                elif self._area == "" and self._metro != "":
                    dict_m = DictMatching(matching_dict=self._city_info[2], words=self._metro, max_result=True)
                    self.start_urls.append(list(dict_m.dict_keys_matching()[0][2].values())[0])
                else:
                    raise ValueError("城市名称和地铁线路名称不能同时存在!")
            else:
                raise ValueError(self._city_info[1])
        else:
            raise ValueError("城市名称不能为空!")

        super(BeiKeScrapySpider).__init__()

    def start_requests(self):
        self.logger.info("开始爬取!当前网址为: {}".format(self.start_urls[0]))
        yield scrapy.Request(url=self.start_urls[0],
                             callback=self.parse_page)

    def parse_page(self, response):
        self.logger.info("获取到当前页面源代码!正在解析获取总页数...")
        # 总页数
        total_page = response.xpath('//div[@class="content__pg"]/@data-totalpage').extract()[0]
        self.logger.info("当前爬取页面类型总页数为: {} 页".format(total_page))
        # 开始爬取第一页
        yield scrapy.Request(url="{}pg{}/#contentList".format(self.start_urls[0], 1),
                             callback=self.parse,
                             meta={'tp': int(total_page), 'cp': 1})

    def parse(self, response):
        self.logger.info("获取到当前页面源代码!正在解析...")
        # 房屋数据字典(为了兼容其他3.X版本使用了有序字典OrderDict)
        house_data = OrderedDict()
        # 房屋列表
        house_list = response.xpath('//div[@class="content__list"]/div')
        # 列表解析
        for house in house_list:
            # ID
            house_data['_id'] = str(uuid.uuid4()).replace("-", "")
            # 房屋所属区域
            house_data['area'] = self._area
            # 房屋详情页
            house_data['house_url'] = \
                "https://{}{}".format(response.meta['download_slot'], house.xpath('a[1]/@href').extract_first())
            # 房屋封面图
            house_data['cover_pic'] = house.xpath('a[2]/img/@data-src').extract_first()
            # 房屋标题
            house_data['title'] = house.xpath('string(div/p[1]/a)').extract_first().strip()
            # 房屋基本信息
            house_data['house_base_info'] = re.sub(r'\s+', '', house.xpath('string(div/p[2])').extract_first())
            # 房屋来源
            house_data['house_src'] = re.sub(r'\s+', '', house.xpath('string(div/p[3])').extract_first())
            # 房屋发布时间
            house_data['publish_date'] = house.xpath('string(div/p[4])').extract_first()
            # 房屋特点
            house_feature = house.xpath('string(div/p[5])').extract_first().split("\n")
            house_data['house_feature'] = [d for d in [d.strip() for d in house_feature] if d != ""]

            # 租房价格
            house_price = house.xpath('string(div/span)').extract_first().split(" ")
            house_price = ["{}-{}".format(d, d)
                           if len(d.split("-")) == 1 and i != 1
                           else d for i, d in enumerate(house_price)]
            house_price = [d.split("-") if i != 1 else d for i, d in enumerate(house_price)]
            house_price = flatten(nested_list=house_price)
            # 弹出单位字段
            house_unit = house_price.pop()
            house_data['price'] = ["{}{}".format(d, house_unit) for d in house_price]
            # 输出数据
            yield house_data
        self.logger.info("############################################################################################")
        if response.meta['cp'] < response.meta['tp']:
            next_page = response.meta['cp'] + 1
            self.logger.info("开始下一页! 下一页为第 {} 页, 总共 {} 页!".format(next_page, response.meta['tp']))
            yield scrapy.Request(url="{}pg{}/#contentList".format(self.start_urls[0], next_page),
                                 callback=self.parse,
                                 meta={'tp': response.meta['tp'], 'cp': next_page})
        else:
            self.logger.info("爬取结束!")
