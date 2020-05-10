# boris-spider

![](https://img.shields.io/badge/python-3.6-brightgreen)

一款高可用易上手的python爬虫框架，支持分布式及批次采集

## 特性

1. 自动下载与重试异常请求，返回的response支持**xpath**、**css**、**re**等解析方式。自动处理中文乱码；
2. 支持**分布式爬虫**，**批次爬虫**。批次爬虫封装了周期性采集数据的逻辑，批次开始时自动下发任务，抓取数据，统计任务处理速度，预估批次是否会超时，**超时报警**等；
3. 可**随时终止**、启动爬虫，任务不丢失不漏采；
4. **支持注册多模板**，即可将多个网站的解析模板注册到同一个爬虫内，由该爬虫统一管理（适用场景：如抓取100家新闻网站，只需启动一个爬虫即可）
5. **上手简单**，且又支持复杂的爬虫需求

## 安装

From PyPi:

    pip3 install boris-spider

From Git:

    pip3 install git+https://github.com/Boris-code/boris-spider.git

## 快速上手

支持的命令行：

    > spider                                                     
    Spider 0.0.4
    
    Usage:
      spider <command> [options] [args]
    
    Available commands:
      create        create spider、parser、item and so on
      shell         debug response
    
    Use "spider <command> -h" to see more info about a command

生产爬虫模板

    spider create -p first_spider    

模板如下：


    import spider


    class FirstSpider(spider.SingleSpider):
        def start_requests(self, *args, **kws):
            yield spider.Request("https://www.baidu.com")
    
        def parser(self, request, response):
            # print(response.text)
            print(response.xpath('//input[@type="submit"]/@value').extract_first())
    
    
    if __name__ == "__main__":
        FirstSpider().start()
        
直接运行，打印如下：

    Thread-2|2020-05-19 18:23:41,128|request.py|get_response|line:283|DEBUG| 
                    -------------- FirstSpider.parser request for ----------------
                    url  = https://www.baidu.com
                    method = GET
                    body = {'timeout': 22, 'stream': True, 'verify': False, 'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}}
                    
    百度一下
    Thread-2|2020-05-19 18:23:41,727|parser_control.py|run|line:415|INFO| parser 等待任务 ...
    FirstSpider|2020-05-19 18:23:44,735|single_spider.py|run|line:83|DEBUG| 无任务，爬虫结束
    
## 了解更多

未完待续...