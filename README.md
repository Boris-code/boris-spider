# boris-spider

![](https://img.shields.io/badge/python-3.6-brightgreen)

一款高可用的python爬虫框架，支持分布式及批次采集

## 安装

From PyPi:

    pip3 install boris-spider

From Git:

    pip3 install git+https://github.com/Boris-code/boris-spider.git

## 快速上手

    import spider
    
    
    class DemoSpider(spider.SingleSpider):
        def start_requests(self, *args, **kws):
            yield spider.Request("https://www.baidu.com")
    
        def parser(self, request, response):
            print(response.text)
    
    
    if __name__ == "__main__":
        DemoSpider().start()