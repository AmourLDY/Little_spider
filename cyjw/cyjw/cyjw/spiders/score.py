# -*- coding: utf-8 -*-
import time
import json
import scrapy
from urllib.request import urlretrieve
from urllib import parse
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from cyjw.items import CyjwItem


class ScoreSpider(scrapy.Spider):
    name = 'score'
    allowed_domains = ['cyjwgl.jmu.edu.cn']
    start_urls = ['http://cyjwgl.jmu.edu.cn']

    def start_requests(self):
        # 首次登录请去掉注释
        # # 登录之前Chrome的设置
        # # 实例化一个启动参数对象
        # chrome_options = Options()
        # # 添加启动参数
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # # 将参数对象传入Chrome
        # username = '输入用户名'
        # password = '输入密码'
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        # browser.get('http://cyjwgl.jmu.edu.cn/login.aspx')
        # text_username = browser.find_element_by_xpath("//input[@name='TxtUserName']").send_keys(username)
        # text_password = browser.find_element_by_xpath("//input[@name='TxtPassword']").send_keys(password)
        # time.sleep(9)
        # browser.find_element_by_xpath('//input[@name="BtnLoginImage"]').click()
        # cookies = browser.get_cookies()
        # self.write_cookies(cookies)
        cookies = self.read_cookies()
        return [
            scrapy.Request(url='http://cyjwgl.jmu.edu.cn/Student/ScoreCourse/ScoreAll.aspx', cookies=cookies,
                           callback=self.parse)]

    @staticmethod
    def write_cookies(cookies):
        with open('cookies.json', 'w') as fp:
            json.dump(cookies, fp)

    @staticmethod
    def read_cookies():
        with open('cookies.json', 'r') as fp:
            listcookies = json.load(fp)
            return listcookies

    def parse(self, response):
        # print(response.text)
        value = response.xpath("//input[@id='__VIEWSTATE']/@value").get()
        formdata = {
            'ctl00_ToolkitScriptManager1_HiddenField': '',
            '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$pageNumber',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': value,
            # 'ctl00$ContentPlaceHolder1$semesterList': '',
            'ctl00$ContentPlaceHolder1$pageNumber': '100'
        }
        yield scrapy.FormRequest(url='http://cyjwgl.jmu.edu.cn/Student/ScoreCourse/ScoreAll.aspx', method='POST',
                                 formdata=formdata,
                                 callback=self.parse_left, dont_filter=True)

    def parse_left(self, response):
        cyjw = CyjwItem()
        trs = response.xpath("//tr[@align='center']")[1:]
        for tr in trs:
            cyjw['term'] = tr.xpath("./td[1]/text()").get()
            cyjw['course_id'] = tr.xpath("./td[2]/text()").get()
            cyjw['course_name'] = tr.xpath("./td[3]/text()").get()
            cyjw['study_time'] = tr.xpath("./td[4]/text()").get()
            cyjw['study_score'] = tr.xpath("./td[5]/text()").get()
            cyjw['type'] = tr.xpath("./td[6]/text()").get()
            cyjw['exam_nature'] = tr.xpath("./td[7]/text()").get()
            cyjw['exam_status'] = tr.xpath("./td[8]/text()").get()
            cyjw['score'] = tr.xpath("./td[9]/text()").get()
            cyjw['GPA'] = tr.xpath("./td[10]/text()").get()
            yield cyjw
