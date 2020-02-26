# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
from lianjia.items import LianjiaItem
from scrapy import Request


class XmlianjiaSpider(scrapy.Spider):
    name = 'xmlianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://xm.lianjia.com/xiaoqu/huli/']

    def parse(self, response):
        for i in range(1, 20):
            next_url = "https://xm.lianjia.com/xiaoqu/huli/pg{}/".format(i)
            yield Request(url=next_url, callback=self.url_parse)

    def url_parse(self, response):
        item = LianjiaItem()
        nodes = response.xpath('//ul[@class="listContent"]//li')
        for node in nodes:
            item['url'] = node.xpath('.//div[@class="title"]/a/@href').get()
            yield Request(url=item['url'], callback=self.parse_node, meta={"item": item})

    def parse_node(self, response):
        item = response.meta.get("item", "")
        item['name'] = response.xpath("//h1[@class='detailTitle']/text()").get()
        item['address'] = response.xpath("//div[@class='detailDesc']/text()").get()
        item['year'] = response.xpath("//div[@class='xiaoquInfoItem'][1]/span[@class='xiaoquInfoContent']/text()").get()
        item['type'] = response.xpath("//div[@class='xiaoquInfoItem'][2]/span[@class='xiaoquInfoContent']/text()").get()
        item['company'] = response.xpath(
            "//div[@class='xiaoquInfoItem'][5]/span[@class='xiaoquInfoContent']/text()").get()
        item['building_count'] = response.xpath(
            "//div[@class='xiaoquInfoItem'][6]/span[@class='xiaoquInfoContent']/text()").get()
        item['house_count'] = response.xpath(
            "//div[@class='xiaoquInfoItem'][7]/span[@class='xiaoquInfoContent']/text()").get()
        yield item
