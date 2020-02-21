# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CyjwItem(scrapy.Item):
    term = scrapy.Field()
    course_id = scrapy.Field()
    course_name = scrapy.Field()
    study_time = scrapy.Field()
    study_score = scrapy.Field()
    type = scrapy.Field()
    exam_nature = scrapy.Field()
    exam_status = scrapy.Field()
    score = scrapy.Field()
    GPA = scrapy.Field()
    pass
