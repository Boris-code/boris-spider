# boris-spider

![](https://img.shields.io/badge/python-3.6-brightgreen)

**boris-spide**r是一款使用Python语言编写的爬虫框架，于多年的爬虫业务中不断磨合而诞生，相比于scrapy，该框架更易上手，且又满足复杂的需求，支持分布式及批次采集。

官方文档：https://spider-doc.readthedocs.io

## 特性

1. 自动下载与重试异常请求，返回的response支持**xpath**、**css**、**re**等解析方式。自动处理中文乱码；
2. 支持 **单进程爬虫**， **分布式爬虫**，**批次爬虫**。批次爬虫封装了周期性采集数据的逻辑，批次开始时自动下发任务，抓取数据，统计任务处理速度，预估批次是否会超时，**超时报警**等；
3. 可**随时终止**、启动爬虫，**任务不丢失不漏采**；
4. **支持注册多模板**，即可将多个网站的解析模板注册到同一个爬虫内，由该爬虫统一管理;
5. 内置**DebugSpider**与**DebugBatchSpider**调试爬虫，调试代码更方便，且不会将调试过程中的数据入库，造成数据污染;
6. 支持以**模板的方式创建**爬虫项目、解析模板、数据item;
7. **数据自动入库**，不需要编写Pipeline;

## 框架流程图

![boris-spider -1-](http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/06/08/borisspider-1.png?x-oss-process=style/markdown-media)

### 模块说明：

* spider **框架调度核心**
* parser_control **模版控制器**，负责调度parser
* collector **任务收集器**，负责从任务队里中批量取任务到内存，以缓冲对任务队列数据库的访问频率及并发量
* parser **数据解析器**
* start_request 初始任务下发函数
* item_buffer **数据缓冲队列**，批量将数据存储到数据库中
* request_buffer **请求任务缓冲队列**，批量将请求任务存储到任务队列中
* request **数据下载器**，封装了requests，用于从互联网上下载数据
* response **数据返回体**，封装了response, 支持xpath、css、re等解析方式。自动处理中文乱码

### 流程说明

1. spider调度**start_request**生产任务
2. **start_request**下发任务到request_buffer中
3. spider调度**request_buffer**批量将任务存储到任务队列数据库中
4. spider调度**collector**从任务队列中批量获取任务到内存队列
5. spider调度**parser_control**从collector的内存队列中获取任务
6. **parser_control**调度**request**请求数据
7. **request**请求与下载数据
8. request将下载后的数据给**response**，进一步封装
9. 将封装好的**response**返回给**parser_control**（图示为多个parser_control，表示多线程）
10. parser_control调度对应的**parser**，解析返回的response（图示多组parser表示不同的网站解析器）
11. parser_control将parser解析到的数据item及新产生的request分发到**item_buffer**与**request_buffer**
12. spider调度**item_buffer**与**request_buffer**将数据批量入库



## 环境要求：

- Python 3.6.0+
- Works on Linux, Windows, macOS

## 安装

From PyPi:

    pip3 install boris-spider

From Git:

    pip3 install git+https://github.com/Boris-code/boris-spider.git

## 快速上手

创建爬虫

    spider create -p first_spider    

创建后的爬虫代码如下：


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
    

## 福利

框架内的utils/tools.py模块下积累了作者多年的工具类函数，种类达到100+，且之后还会不定期更新，具有搬砖价值! 
    
## 学习交流

想了解更多框架使用详情，可访问官方文档：https://spider-doc.readthedocs.io

如学习中遇到问题，可加下面的QQ群

群号:750614606

![WechatIMG188](http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/04/08/wechatimg188.jpeg)

知识星球：

![知识星球](http://markdown-media.oss-cn-beijing.aliyuncs.com/2020/02/16/zhi-shi-xing-qiu.jpeg)

星球会不定时分享爬虫技术干货，涉及的领域包括但不限于js逆向技巧、爬虫框架刨析、爬虫技术分享等