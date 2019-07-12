# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from ..items import fileItem
import re

class HikvisionSpider(scrapy.Spider):
    name = 'hikvision'
    allowed_domains = ['hikvisioneurope.com']
    start_urls = ['http://www.hikvisioneurope.com/uk/portal/?dir=portal']
    # start_urls = ['http://www.hikvisioneurope.com/uk/portal/?dir=portal/Software/Software%20Tools/SADP/SADP_V3.0.1.7']

    def jsonParse(self,dict_a):
        res = "{"
        for key in dict_a:
            res += "\"" + key + "\"" + " "
            res += ": "
            res += "\"" + dict_a[key] + "\","
        res = res[:-1]
        res += "}"
        return res
        
    def parse(self, response):
        base_url = 'http://www.hikvisioneurope.com/uk/portal/'
        # number = 0
        # item_list = {}
        result = ""
        for i in range(2,100):
            path = '//*[@id="datatable-checkbox"]/tbody/tr['
            path += str(i)
            path += ']/td[1]/a[2]/@href'
            flags = "--------------------------------\n"  
            # print flags + "Searching Path : "+ path
            next_context = response.xpath(path).get(default="Nothing") #find nexturl
            # print next_context
            if (cmp('Nothing',next_context) == 0): # no more next page url
                download_url_path = '//*[@id="datatable-checkbox"]/tbody/tr['+str(i)+ ']/td[4]/a/@href'
                download_context = response.xpath(download_url_path).get(default="Nothing")
                if (cmp('Nothing',download_context)==0):   #not download_url
                    # print "Not download url: ",download_context
                    break
                else:                             #downlaod_url
                    item = fileItem()
                    download_url = download_context
                    item['downloadUrl'] = base_url + download_url

                    file_name = re.search(r'(/)(?!.*\1).*',download_url).group()[1:]
                    item['fileName'] = file_name

                    path_reg = ".+?(?=" + file_name + ")"
                    filepath = re.search(path_reg,download_url).group()
                    item['filePath'] = filepath

                    yield item
                    
                    line = self.jsonParse(item) + "\n"
                    result += line
                    # print "file found " + download_url
            else:
                next_url = next_context
                yield scrapy.Request((base_url + next_url).strip(),self.parse)
        
        
        # file = open('test.json', 'a')
        # file.write(result.encode('utf-8'))
        

