# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class fileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    downloadUrl = scrapy.Field() # 下载链接
    fileName = scrapy.Field()    # 文件名
    filePath = scrapy.Field()        # 保存路径
    pass
