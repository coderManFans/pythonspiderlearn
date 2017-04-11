import requests,logging

from bs4 import BeautifulSoup

from pythonspiderlearn.pythonspiderlearn.data_tool.RedisModule import PyRedisUtil


class ProxySpider:

    # redis key 代理

    proxyKey = "proxyKey"


    '''
    爬取http://www.kuaidaili.com/中的可用代理数据信息，传入ProxyPool
    '''

    kuaiDaiLiCookie2 = '_ydclearance=c8bc038ce055d51d5b9b0e17-22f5-4151-878f-4f41030a6007-1490882885; channelid=0; sid=1490875433169593; _gat=1; _ga=GA1.2.1198673172.1489654873; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1490770898,1490774165,1490837633,1490875689; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1490875691'
    kuaiDaiLiHeader2 = {
        'Host': 'www.kuaidaili.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'http://www.kuaidaili.com',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': kuaiDaiLiCookie2
    }

    xiCiDaiLiheaders = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               "Referer": "http://www.kuaidaili.com",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
    }

    '''
    获取快代理网站代理IP
    '''
    def getKuaiDaiLi(self, myDaiLi=kuaiDaiLiHeader2,proxyKey=proxyKey):

        redisUtils = PyRedisUtil()

        try:
            html = requests.get("http://www.kuaidaili.com/proxylist/2/", headers=myDaiLi, timeout=30).text
            # print(html)
            soup = BeautifulSoup(html, 'html.parser').find_all("div", id="index_free_list")[0].table
            print(soup)

        except:

            logging.error("快代理请求头cookie失效，请重新获取cookie")
            return

        count = 0
        for i in range(1, 10):
            html = requests.get("http://www.kuaidaili.com/proxylist/" + str(i) + "/", headers=myDaiLi,
                                timeout=30).text
            # print(html)
            soup = BeautifulSoup(html, 'html.parser').find_all("div", id="index_free_list")[0].table
            # print(soup)
            for tr in enumerate(soup.find_all('tr')):
                tds = BeautifulSoup(str(tr), "html.parser")
                td = tds.findAll('td')
                if len(td) > 0:
                    if str(td[2].text) == '高匿名' or str(td[2].text) == '匿名':
                        valueUrl = "http://" + str(td[0].text) + ":" + str(td[1].text)
                        redisUtils.lpushList(proxyKey, valueUrl)
                        count += 1

        logging.info("count = " + str(count))

    def getXiCiDaiLi(self, myDaiLi=xiCiDaiLiheaders, proxyKey=proxyKey):

        redisUtils = PyRedisUtil()
        count = 0
        for i in range(1,5):

            r = requests.get("http://www.xicidaili.com/nn/"+str(i)+"/", headers=myDaiLi)
            #print(r.text)
            soupData = BeautifulSoup(r.text, 'html.parser')
            tables = soupData.findAll('table')
            tab = tables[0]

            for tr in enumerate(tab.find_all('tr')):
                tds = BeautifulSoup(str(tr), "html.parser")
                td = tds.findAll('td')

                if len(td) > 0:
                    if str(td[5].text) == 'HTTP' and (str(td[8].text).find("小时") > 0 or str(td[8].text).find("月") > 0 or str(td[8].text).find("天") > 0):
                        print("http://"+str(td[1].text) + ":" + str(td[2].text)+"-------"+td[8].text)
                        valueUrl = "http://"+str(td[1].text) + ":" + str(td[2].text)
                        redisUtils.lpushList(proxyKey,valueUrl)
                        count += 1

        print("count = "+str(count))

proxy = ProxySpider()
#proxy.getXiCiDaiLi()
#proxy.getKuaiDaiLi()


