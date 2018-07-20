# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import time
import json
import os

class OitYitikuscrapyDataPipeline(object):
    def open_spider(self, spider):
        path ='D:\\xiti10001\\data\\{}\\'.format(time.strftime("%Y%m%d",time.localtime()))
        # path = 'd:\\OITData\\zujuan\\{0}\\{1}\\'.format(time.strftime("%Y%m%d", time.localtime()), spider.name)
        isExists = os.path.exists(path)
        if isExists:
            pass
        else:
            os.makedirs(path)
        self.file = codecs.open(path + spider.name+'.json', 'a', encoding='utf-8')
    def process_item(self, item, spider):
        print('进程打印信息：',spider.name)
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.close()