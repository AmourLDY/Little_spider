# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': '',
            'password': '',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (
            item['title'], item['author'], item['time'], item['char_counts'], item['views_counts'],
            item['text'],
            item['label'], item['article_id']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into jianshu(id, title, author, time_create, char_counts, view_counts, article, label, article_id) values (null,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


class TwistedMySQLPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '106.14.210.248',
            'port': 3306,
            'user': 'root',
            'password': '981016',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor,
        }
        self.dbpool = adbapi.ConnectionPool(
            'pymysql', **dbparams
        )
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into jianshu(id, title, author, time_create, char_counts, view_counts, article, label, article_id) values (null,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)
        return item

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (
            item['title'], item['author'], item['time'], item['char_counts'], item['views_counts'],
            item['text'],
            item['label'], item['article_id']))

    def handle_error(self, error, item, spider):
        print('*' * 10)
        print(error)
        print('*' * 10)
