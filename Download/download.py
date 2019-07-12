import os
import sys
import requests
import re
import subprocess
import threading
import json
import time
import random

class DownloadThread(threading.Thread):
    def __init__(self,download_url, fileFolder,fileName,callBack):
        threading.Thread.__init__(self)
        self.download_url = download_url
        self.fileFolder = fileFolder
        self.fileName = fileName
        self.callBack = callBack
    def hikvision_download_file(self, download_url, fileFolder, fileName):
        import execjs
        os.environ['EXECJS_RUNTIME'] = "Node"
        # print "File found: " + fileName
        import requests
        fileFolder = os.getcwd() + "/" + fileFolder
        if not os.path.exists(fileFolder):
            os.makedirs(fileFolder)
        if os.path.exists(fileFolder + fileName):
            return "finished"
        
        headers = {}
        headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
        headers['Accept-Encoding'] = "gzip, deflate"
        headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8" 
        headers["Connection"] = "keep-alive"
        headers['cookie'] = "_ga=GA1.2.1402998178.1562638478"
        headers["Host"] = "www.hikvisioneurope.com"
        headers["Upgrade-Insecure-Requests"] = "1"
        headers["Cache-Control"] = "max-age=0"
        refer_reg = ".+?(?=" + fileName + ")"
        headers["Referer"] = re.search(refer_reg, download_url).group()[:-1]
        try:
            r = requests.get(download_url,headers = headers)
            if(r.status_code!=200):
                print "status code: " + r.status_code
                print "while accessing " + download_url
                return
        except Exception,e:
            print "Exception : " + str(e)
            print "while downloading " + download_url
            return  
        except requests.exceptions.Timeout:
            print "Timeout while downloding " + download_url
            return
        except requests.exceptions.ConnectTimeout:
            print "Conect Timeout while downloding " + download_url
            return
        # else:
        #     print "Somethings wrong while downloading " + download_url
        #     return
            
        f = open(fileFolder + fileName,'wb')
        f.write(r.content)
        f.close()

        return 'finished'

    def run(self):
        self.hikvision_download_file(self.download_url, self.fileFolder, self.fileName)
        self.callBack(self.fileName)

class ThreadHandler:
    def __init__(self):
        self.thread_nums = 0
        self.MAX_THREAD_NUM = 3
        src = "test1.json"
        finish = "finished.json"
        self.src_file = open(src,"r")
        self.finish_file = open(finish,"r")
    def CreateThread(self):
        self.thread_nums += 1
        time.sleep(random.randint(2,4))
        from_file = self.src_file.readline()
        if not from_file:
            return
        # print from_file
        task = json.loads(from_file)
        download_url = task['downloadUrl']
        fileFolder = task['filePath']
        fileName = task['fileName']
        print "Downloading..." + fileName
        th = DownloadThread(download_url,fileFolder,fileName,self.ThreadCallback)
        th.start()
    def ThreadCallback(self,fileName):
        self.thread_nums -= 1
        self.CreateThread()
        print "Finished : " + fileName 
    def Run(self):
        for i in range(0, self.MAX_THREAD_NUM):
            self.CreateThread()


ThreadHandler = ThreadHandler()
ThreadHandler.Run()

        
    
        
        


    