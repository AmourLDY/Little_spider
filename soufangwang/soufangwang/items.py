# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    provience = scrapy.Field()
    city = scrapy.Field()
    house_name = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    is_sale = scrapy.Field()
    info = scrapy.Field()
    origin_url = scrapy.Field()


class EsfHouseItem(scrapy.Item):
    provience = scrapy.Field()
    city = scrapy.Field()
    house_name = scrapy.Field()
    price = scrapy.Field()
    rooms = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    info = scrapy.Field()
    origin_url = scrapy.Field()
