# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HousePipeline:
    conn = None
    cursor = None

    def open_spider(self, spider):
        self.conn = pymysql.Connect(host='localhost', port=3306, user='root', password='123456', db='Spider',
                                    charset='utf8')

    def process_item(self, item, spider):
        sql = 'insert into house values ("%s", "%s", "%s", "%s", "%s", "%s")' % (
        item['name'], item['price'], item['type'], item['size'], item['addr'], item['tel'])
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
