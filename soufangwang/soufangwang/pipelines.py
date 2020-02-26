# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
from pymysql.cursors import DictCursor
import pymysql
from soufangwang.items import NewHouseItem, EsfHouseItem


class SoufangwangPipeline(object):
    def process_item(self, item, spider):
        return item


class TwistedMySQLPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '106.14.210.248',
            'port': 3306,
            'user': 'root',
            'password': '981016',
            'database': 'esf_fang',
            'charset': 'utf8',
            'cursorclass': DictCursor,

        }
        self.dbpool = adbapi.ConnectionPool(
            'pymysql', **dbparams
        )
        self._newhouse_sql = None
        self._esfhouse_sql = None

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            defer = self.dbpool.runInteraction(self.insert_newhouse, item)
            defer.addErrback(self.handle_error, item, spider)
            return item
        elif isinstance(item, EsfHouseItem):
            defer = self.dbpool.runInteraction(self.insert_esfhouse, item)
            defer.addErrback(self.handle_error, item, spider)
            return item

    @property
    def newhouse_sql(self):
        if not self._newhouse_sql:
            self._newhouse_sql = """
            insert into new_house(id, provience, city, house_name, price, rooms, area, address, district, is_sale, info, origin_url) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._newhouse_sql
        return self._newhouse_sql

    @property
    def esfhouse_sql(self):
        if not self._esfhouse_sql:
            self._esfhouse_sql = """
            insert into esf_house(id, provience, city, house_name, price, rooms, area, address, info, origin_url) values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._esfhouse_sql
        return self._esfhouse_sql

    def insert_newhouse(self, cursor, item):
        cursor.execute(self.newhouse_sql, (
            item['provience'], item['city'], item['house_name'], item['price'], item['rooms'], item['area'],
            item['address'], item['district'], item['is_sale'], item['info'], item['origin_url'],
        ))

    def insert_esfhouse(self, cursor, item):
        cursor.execute(self.esfhouse_sql, (
            item['provience'], item['city'], item['house_name'], item['price'], item['rooms'], item['area'],
            item['address'], item['info'], item['origin_url'],
        ))

    def handle_error(self, error, item, spider):
        print('*' * 10)
        print(error)
        print('*' * 10)
