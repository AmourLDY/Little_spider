# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter


class CyjwPipeline(object):
    def __init__(self):
        self.fp = open("cyjw.csv", 'wb')
        self.exporter = CsvItemExporter(self.fp, encoding='gbk')

    def open_spider(self, spider):
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
        self.exporter.finish_exporting()
