# -*- coding: utf-8 -*-
import scrapy
import copy
from qczj.items import QczjItem


class BmwSpider(scrapy.Spider):
    name = 'bmw'
    allowed_domains = ['https://car.autohome.com.cn/']
    start_urls = ['https://car.autohome.com.cn/pic/series/65.html#pvareaid=2042214']

    def parse(self, response):
        item = QczjItem()
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            urls = uibox.xpath(".//div[2]/ul//li//a[1]/@href").getall()
            image_urls = list(map(lambda x: response.urljoin(x), urls))
            item['category'] = uibox.xpath(".//div[@class='uibox-title']/a[1]/text()").get()
            for url in image_urls:
                yield scrapy.Request(url, callback=self.parse_image, meta={'item': copy.deepcopy(item)}, dont_filter=True)

    def parse_image(self, response):
        item = response.meta.get('item')
        image_urls = response.xpath("//img[@id='img']/@src").get()
        item['image_urls'] = [response.urljoin(image_urls)]
        yield item

