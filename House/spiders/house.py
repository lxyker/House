# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from House.items import HouseItem


class HouseSpider(CrawlSpider):
    name = 'house'
    # allowed_domains = ['www.qq.com']
    start_urls = ['https://wuhan.newhouse.fang.com/house/s/']

    rules = (
        Rule(LinkExtractor(allow=r'/house/s/b\d+/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        li_list = response.xpath('//*[@id="newhouse_loupai_list"]/ul/li')
        for li in li_list:
            item = HouseItem()
            item['name'] = li.xpath('.//div[@class="nlcd_name"]/a/text()').extract_first()
            item['price'] = li.xpath('.//div[@class="nhouse_price"]/span/text()').extract_first()
            item['addr'] = li.xpath('//div[@id="sjina_C31_06"]/a/@title').extract_first()
            item['tel'] = li.xpath('.//div[@class="tel"]/p/text()').extract_first()

            item['type'] = li.xpath('.//div[@class="house_type clearfix"]/a/text()').extract()

            item['size'] = li.xpath('.//div[@class="house_type clearfix"]/text()').extract()

            if item['name']:
                item['name'] = re.sub(r'\n|\t|', '', item['name'])
            if item['size']:
                item['size'] = re.sub(r'\n|－|\t', '', item['size'][-1])

            yield item