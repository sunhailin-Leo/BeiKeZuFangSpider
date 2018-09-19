# -*- coding: utf-8 -*- #
"""
Created on 2018年9月19日
@author: Leo
"""
# Python内置库
import os
import sys

# Python第三方库
# 通过调用命令行进行调试
# 调用execute这个函数可调用scrapy脚本
from scrapy.cmdline import execute


def main():
    """
    启动方法
    """
    print("启动爬虫...")
    city_name = input("请输入城市名称:")
    print("您输入的城市名称为: {}".format(city_name))
    if city_name == "":
        raise ValueError("城市名称不能为空!")
    else:
        area_name = input("请输入区域名称(可以忽略):")
        if area_name != "":
            print("您输入的区域名称为: {}".format(area_name))
            metro_name = ""
        else:
            metro_name = input("请输入地铁线名称:")
            print("您输入的地铁线为: {}".format(metro_name))
            area_name = ""
        print("城市: {}, 区域: {}, 地铁线: {}".format(city_name, area_name, metro_name))
        start_spider(city_name=city_name, area_name=area_name, metro_name=metro_name)


def start_spider(
        city_name: str,
        area_name: str,
        metro_name: str):
    """
    用scrapy.cmdline命令启动Scrapy
    :param city_name: 城市名称
    :param area_name: 区域名称
    :param metro_name: 地铁线名称
    """
    # 设置工程路径，在cmd 命令更改路径而执行scrapy命令调试
    # 获取main文件的父目录，os.path.abspath(__file__) 为__file__文件目录
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # 运行
    execute(["scrapy", "crawl", "BeiKeErShouFang",
             "-a", "city={}".format(city_name),
             "-a", "area={}".format(area_name),
             "-a", "metro={}".format(metro_name)])


if __name__ == '__main__':
    main()
    # start_spider(city_name="深圳市", area_name="南山区", metro_name="")
