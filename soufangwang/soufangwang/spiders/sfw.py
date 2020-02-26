# -*- coding: utf-8 -*-
import re

import scrapy
from soufangwang.items import NewHouseItem, EsfHouseItem


class SfwSpider(scrapy.Spider):
    name = 'sfw'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']/table[@class='table01']//tr")
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_td = tds[0]
            provience_text = re.sub(r'\s', '', province_td.xpath(".//text()").get())
            if provience_text:
                provience = provience_text
            if provience == '其它':
                continue
            city_td = tds[1]
            city_links = tds[1].xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath("./text()").get()
                city_url = city_link.xpath("./@href").get()
                link = city_url.split('.')
                new_house = link[0] + '.newhouse.fang.com' + '/house/s/'
                esf_house = link[0] + '.esf.fang.com'
                yield scrapy.Request(url=new_house, callback=self.parse_newhouse, meta={"info": (provience, city)})
                yield scrapy.Request(url=esf_house, callback=self.parse_esfhouse, meta={'info': (provience, city)})


    def parse_newhouse(self, response):
        provience, city = response.meta.get('info')
        lis = response.xpath("//div[@class='nl_con clearfix']//li")
        for li in lis:
            house_name = re.sub(r'[\n|\t]', '', ''.join(li.xpath(".//div[@class='nlcd_name']/a/text()").get()))
            price = re.sub(r'[\n|\t]', '', "".join(li.xpath(".//div[@class='nhouse_price']//text()").getall()))
            rooms = ",".join(li.xpath(".//div[@class='house_type clearfix']//a/text()").getall())
            area = re.sub(r'[\t|\n|－]', '', li.xpath(".//div[@class='house_type clearfix']/text()").getall()[-1])
            address = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            address = re.sub(r'[\n|\t]', '', address)
            district = re.match('\[(.*)\].*?', address).group(1)
            is_sale = li.xpath(".//div[@class='fangyuan']/span/text()").get()
            info = li.xpath(".//div[@class='fangyuan']//a/text()").get()
            origin_url = 'https://' + li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            item = NewHouseItem(
                provience=provience,
                city=city,
                house_name=house_name,
                price=price,
                rooms=rooms,
                area=area,
                address=address,
                district=district,
                is_sale=is_sale,
                info=info,
                origin_url=origin_url
            )
            yield item
            pages = response.xpath("//li[@class='fr']//a[last()-1]/text()").get()
            for page in range(2, len(pages)):
                next_url = response.urljoin('/house/s/b9{}/'.format(page))
                yield scrapy.Request(url=next_url, callback=self.parse_newhouse, meta={'info': (provience, city)})

    def parse_esfhouse(self, response):
        provience, city = response.meta.get('info')
        dls = response.xpath("//div[@class='shop_list shop_list_4']//dl")
        for dl in dls:
            house_name = dl.xpath(".//dd[not(@class)]//p[@class='add_shop']/a/@title").get()
            price = "".join(dl.xpath(".//dd[@class='price_right']//span[@class='red']//text()").getall())
            room_infos = "".join(dl.xpath(".//dd[not(@class)]//p[@class='tel_shop']//text()").getall()).split('|')
            rooms = re.sub(r'[\t|\n|\r|\s]', '', room_infos[0])
            try:
                area = re.sub(r'[\r|\t|\n|\s]', '', room_infos[1])
            except:
                area = re.sub(r'[\r|\t|\n|\s]', '', room_infos[0])
                pass
            address = "".join(dl.xpath(".//dd[not(@class)]//p[@class='add_shop']//span/text()").getall())
            infos = "-".join(room_infos[2:-1])
            info = re.sub(r'[\r|\t|\n|\s]', '', infos)
            origin_url = response.urljoin(dl.xpath(".//h4[@class='clearfix']/a/@href").get())
            item = EsfHouseItem(
                provience=provience,
                city=city,
                house_name=house_name,
                price=price,
                rooms=rooms,
                area=area,
                address=address,
                info=info,
                origin_url=origin_url,
            )
            yield item
        next_url = response.urljoin(response.xpath("//div[@class='page_al']//p[last()-1]/a/@href").get())
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse_esfhouse, meta={"info": (provience, city)})
