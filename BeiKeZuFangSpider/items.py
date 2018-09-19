# -*- coding: utf-8 -*-

import scrapy


class BeikezufangspiderItem(scrapy.Item):
    rent_house = {}

    def __setitem__(self, key, value):
        self.rent_house[key] = value
