# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spiders.task import hikvision_download_file


class HikspiderPipeline(object):
    def jsonParse(self,dict_a):
        res = "{"
        for key in dict_a:
            res += "\"" + key + "\"" + " "
            res += ": "
            res += "\"" + dict_a[key] + "\","
        res = res[:-1]
        res += "}"
        return res

    def __init__(self):
        self.file = open('test.json', 'a')

    def process_item(self, item, spider):
        # data = {
        #     'downloadUrl': item['downloadUrl'],
        #     'path' : item['path'],
        #     'fileName:':item['fileName']
        # }
        # line = self.jsonParse(item) + "\n"
        # self.file.write(line.encode('utf-8'))
        hikvision_download_file(item['downloadUrl'], item['filePath'], item['fileName'])
        return item
