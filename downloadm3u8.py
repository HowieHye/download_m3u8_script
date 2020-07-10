import random
import re
import time
import urllib.request
import urllib
import win32api
import logging

uapools = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 Edg/80.0.361.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)"
]

timenow = time.strftime("%Y_%m_%d_%H_%M_%S")
logfilename = ".\\log\\"+timenow+".log"
logging.basicConfig(filename=logfilename,format='%(levelname)s:%(asctime)s:%(message)s',level=logging.INFO)


def searchByUrl(url):
    if("html" in url):
        pass
    else:
        url = url + ".html"
    patOfUrl = '/vodplay/(.*?)-1.html'
    urlOut = re.compile(patOfUrl, re.S).findall(url)[0]
    logging.info("urlOut:"+urlOut)
    return urlOut


def randomUA():
    opener = urllib.request.build_opener()
    this_ua = random.choice(uapools)
    ua = ("User-Agent", this_ua)
    uaForN = "User-Agent:" + this_ua
    opener.addheaders = [ua]
    urllib.request.install_opener(opener)
    logging.info("当前使用的ua:" + str(this_ua))
    return uaForN


def searchAllUrl(url0, url):
    randomUA()
    dataOfFirstPage = urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "ignore")
    patOfEveryPage = '<a href="/vodplay/' + url0 + '(.*?)">.*?</a></li>'
    patOfName = '<a href="/vodplay/' + url0 + '.*?>(.*?)</a></li>'

    resultOfPage = re.compile(patOfEveryPage, re.S).findall(dataOfFirstPage)
    resultOfName = re.compile(patOfName, re.S).findall(dataOfFirstPage)
    return resultOfName, resultOfPage

def findName(url):
    randomUA()
    dataOfFirstPage = urllib.request.urlopen(url, timeout=60).read().decode("utf-8", "ignore")
    pat = "vod_name='(.*?)',"
    resultName = re.compile(pat,re.S).findall(dataOfFirstPage)[0]
    return resultName


def findM3U8(page):
    patOfM3U8 = 'url":"https?:(.*?)","url_next'
    randomUA()
    dataOfCurPage = urllib.request.urlopen(page).read().decode("utf-8", "ignore")
    resultOfCurPage = re.compile(patOfM3U8, re.S).findall(dataOfCurPage)[0]
    resultOfCurPageUrl = "http:"+resultOfCurPage.replace('\/', '/')
    return resultOfCurPageUrl



def downloadM3U8(index):
    print("共有"+str(index)+"集/期")
    startindex = input("请输入从第几集开始下载:")
    endindex = input("请输入下载到第几集:")
    return startindex,endindex


def downloadVideo(url, name):
    ua = randomUA()
    parameter = url + " --saveName " + name + " --enableDelAfterDone --headers headers=" + ua
    win32api.ShellExecute(0, 'open', 'N_m3u8DL-CLI.exe', parameter, '', 0)
    logging.info(parameter)
    return


def main():
    url = input("please input url:")
    url0 = searchByUrl(url)
    result = searchAllUrl(url0, url)
    logging.info(result)

    startindex,endindex = downloadM3U8(len(result[1]))
    logging.info("startindex:"+startindex)
    logging.info("endindex:"+endindex)
    print("请等待下载完成!")
    for i in range(int(startindex)-1, int(endindex)):
        curPageUrl = "http://lab.liumingye.cn/vodplay/" + url0 + result[1][i]
        logging.info("curPageUrl:"+curPageUrl)
        m3u8url = findM3U8(curPageUrl)
        NamePre = findName(url)
        Name = NamePre + result[0][i]
        downloadVideo(m3u8url, Name)
        logging.info("正在从" + m3u8url + "下载" + Name)
        time.sleep(30)



if __name__ == '__main__':
    main()
