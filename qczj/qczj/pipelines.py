# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os
import re
from pathlib import Path
from urllib import request
from urllib.parse import urlparse

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes

from qczj.settings import IMAGES_STORE


class QczjPipeline(object):
    def __init__(self):
        self.path = Path(__file__).parent.joinpath('images')
        if not self.path.exists():
            self.path.mkdir()

    def process_item(self, item, spider):
        category = item['category']
        urls = item['urls']

        category_path = self.path.joinpath(category)
        if not category_path.exists():
            category_path.mkdir()
        for url in urls:
            for i in range(len(urls)):
                image_name = '{}.png'.format(i)
                request.urlretrieve(url, category_path.joinpath(image_name))
        return item


class BMWImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(BMWImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(BMWImagesPipeline, self).file_path(request, response, info)
        category = request.item.get('category')
        category_path = Path(IMAGES_STORE).joinpath(category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace('full/', '')
        return '{}/{}'.format(category, image_name)

