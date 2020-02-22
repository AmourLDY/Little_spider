# -*- coding: utf-8 -*-
import json

import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    # start_urls = ['http://httpbin.org/user-agent', 'http://httpbin.org/ip']
    start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        text = json.loads(response.text)
        print(text)
        yield scrapy.Request(url=HttpbinSpider.start_urls[0], dont_filter=True)
