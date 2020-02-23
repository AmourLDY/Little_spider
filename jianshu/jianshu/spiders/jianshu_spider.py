# -*- coding: utf-8 -*-
import scrapy
from jianshu.items import JianshuItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime
import re


class JianshuSpiderSpider(CrawlSpider):
    name = 'jianshu_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/\d+.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        author = response.xpath("//span[@class='_22gUMi']/text()").get()
        time_stmp = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        time_stmp = datetime.datetime.strptime(time_stmp, "%Y.%m.%d %H:%M:%S")
        char_counts = response.xpath("//div[@class='s-dsoj']//span[2]/text()").get()
        char_counts = re.sub(r'[字数|\s|,]', '', char_counts)
        views_counts = response.xpath("//div[@class='s-dsoj']//span[3]/text()").get()
        views_counts = re.sub(r'[阅读|\s|,]', '', views_counts)
        text = response.xpath("//article[@class='_2rhmJa']").get()
        label = ",".join(response.xpath("//div[@class='_2Nttfz']//a//span/text()").getall())
        article_id = response.url.split('?')[0].split('/')[-1]
        item = JianshuItem(
            title=title,
            author=author,
            time=time_stmp,
            char_counts=char_counts,
            views_counts=views_counts,
            text=text,
            label=label,
            article_id=article_id,
        )
        yield item
