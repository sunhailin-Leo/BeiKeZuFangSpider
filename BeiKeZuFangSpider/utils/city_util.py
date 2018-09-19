# -*- coding: UTF-8 -*-
"""
Created on 2018年9月17日
@author: Leo
"""
import os
import json
import logging
import requests
from lxml import etree

# 日志
logger = logging.getLogger(__name__)

# 所有城市的列表URL
CITY_URL = "https://www.ke.com/city/"

# Header
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 "
                  "UBrowser/6.2.4094.1 Safari/537.36 "
}

# CityJSON Path
# CITY_JSON_PATH = '.././static/city.json'
CITY_JSON_PATH = './BeiKeZuFangSpider/static/city.json'


class CityInfoSpider:
    def __init__(self, city: str):
        """
        城市
        :param city: 城市名称(目前只支持中文)
        """
        self._city = city.replace("市", "")
        # 判断json文件是否存在
        if not os.path.exists(CITY_JSON_PATH):
            self._parse_city_page()
        # 加载城市JSON
        city_json = json.load(open(CITY_JSON_PATH, 'r', encoding="UTF-8"))
        try:
            self._city_url = self._url_change(url=city_json[self._city])
            logger.info("当前获取到的URL: {}".format(self._city_url))
            # 获取城市的区域和地铁线路区域
            self._city_data = self._parse_city_area_and_metro()
        except KeyError:
            self._city_data = ("Error", "城市名称有误!请重新填写城市名称!")

    @staticmethod
    def _url_change(url: str) -> str:
        """
        城市URL转换成城市租房URL
        :param url: 城市URL
        :return: 城市租房URL
        """
        url = url.split(".")
        url.insert(1, "zu")
        return ".".join(url)

    @staticmethod
    def _get_page_html(url: str, timeout=10) -> str:
        """
        获取页面源代码
        :param url: URL
        :param timeout: 等待时间
        :return: 页面源代码
        """
        return requests.get(url=url, headers=HEADER, timeout=timeout).content.decode("UTF-8")

    def _is_er_shou_fang(self, url: str):
        """
        判断当前城市是否存在二手房板块
        :param url: 城市URL
        :return:
        """
        t_url = self._url_change(url=url)
        try:
            self._get_page_html(url=t_url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            return False

    def _parse_city_page(self):
        """
        解析城市编码
        """
        response_html = self._get_page_html(url=CITY_URL)
        selector = etree.HTML(text=response_html)
        # 国内城市编码
        city_list = selector.xpath('//li[contains(@data-action, "国内城市")]')
        # 写入城市URL到json中
        with open(CITY_JSON_PATH, "w", encoding="UTF-8") as f:
            # 字典推导式
            dict_data = {
                city.xpath('string(a)'): "https:{}".format(city.xpath('a/@href')[0])
                for city in city_list
                if "fang" not in city.xpath('a/@href')[0]
                   and self._is_er_shou_fang(url="https:{}".format(city.xpath('a/@href')[0]))
            }
            # 写入到json文件
            json.dump(dict_data, f, ensure_ascii=False, indent=4)

    def _parse_city_area_and_metro(self) -> (dict, dict):
        """
        解析城市的区域和地铁线路分布
        :return: 城市的URL, 区域数据和地铁沿线数据
        """
        response_html = self._get_page_html(url=self._city_url)
        selector = etree.HTML(text=response_html)
        # 区域
        area_list = selector.xpath('//ul[@data-target="area"]/li')[1:]
        area_dict = {
            area.xpath('string(a)'): self._city_url + area.xpath('a/@href')[0]
            for area in area_list
        }
        # 地铁沿线
        metro_list = selector.xpath('//ul[@data-target="station"]/li')[1:]
        metro_dict = {
            metro.xpath('string(a)'): self._city_url + metro.xpath('a/@href')[0]
            for metro in metro_list
        }
        return self._city_url, area_dict, metro_dict

    def get_city_data(self):
        """
        获取所需的城市数据
        :return: tuple(dict(区域), dict(地铁沿线))
        """
        return self._city_data


if __name__ == '__main__':
    c = CityInfoSpider(city="深圳市")
    print("#########################")
    print(c.get_city_data()[0])
    print(c.get_city_data()[1])
    print(c.get_city_data()[2])
