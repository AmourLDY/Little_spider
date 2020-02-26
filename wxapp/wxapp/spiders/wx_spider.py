# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxapp.items import WxappItem

import re


class WxSpiderSpider(CrawlSpider):
    name = 'wx_spider'
    allowed_domains = ['www.wxapp-union.com']
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2/']

    rules = (
        Rule(LinkExtractor(allow=r'http://www.wxapp-union.com/portal.php?mod=list&catid=\d/'), follow=True),
        Rule(LinkExtractor(allow=r'http://www.wxapp-union.com/article-.+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = WxappItem()
        item['title'] = response.xpath("//h1[@class='ph']/text()").get()

        author = response.xpath("//p[@class='authors']//text()").getall()
        author = "".join(author)
        item['author'] = author.replace('\n', '')

        text = response.xpath("//div[@class='content_middle cl']//text()").getall()
        text = "".join(text)
        item['text'] = re.sub(r'[\n\r\，]', '', text)
        yield item
