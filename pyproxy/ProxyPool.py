from helloworld.pytest.RedisModule import PyRedisUtil
from helloworld.pyproxy.ProxySpider import ProxySpider
import requests


class ProxyPool:
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Host": "blog.csdn.net"
    }

    proxy = ProxySpider()

    redisUtil = PyRedisUtil()

    def getValidProxy(self, redisUtil=redisUtil, proxy=proxy, headers=headers):
        length = redisUtil.llen(proxy.proxyKey)
        if length > 0:
            url = redisUtil.lpopList(proxy.proxyKey)
            proxies2 = {"https": str(url)}

            statusCode = requests.get("http://blog.csdn.net/pony_maggie/article/details/68062415", headers=headers,
                                      proxies=proxies2).status_code
            if statusCode == 200:
                redisUtil.rpush(proxy.proxyKey, url)
                return url
            else:
                self.getValidProxy()


#proxyPool = ProxyPool()
#url = proxyPool.getValidProxy()
#print("url = "+str(url))