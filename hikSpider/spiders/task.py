import os
import sys
import requests
from re import search
import subprocess


def hikvision_download_file(download_url, fileFolder, fileName):
    import execjs
    os.environ['EXECJS_RUNTIME'] = "Node"
    print "File found: " + fileName
    import requests
    fileFolder = os.getcwd() + "/" + fileFolder
    if not os.path.exists(fileFolder):
        os.makedirs(fileFolder)
    if os.path.exists(fileFolder + fileName):
        return "finished"
    r = requests.get(download_url) 

    with open(fileFolder + fileName,'wb') as f:
        f.write(r.content)

    # node_function = execjs.compile("""
    #     async function getFile() {
    #         const puppeteer = require('puppeteer');
    #         const browser = await puppeteer.launch({headless: false});
    #         const page = await browser.newPage();
    #         await page.waitFor(1);
    #         await page._client.send('Page.setDownloadBehavior', {behavior: 'allow', downloadPath: '%s'});
    #         await page.goto('%s');
    #         await page.tap('img');
    #         await page.waitFor(240000);
    #         await browser.close();
    #     }
    # """ % (fileFolder, download_url))
    # node_function.call("getFile")

    return 'finished'
