# -*- coding: utf-8 -*-
"""
Created on 2020/4/21 10:37 PM
---------
@summary: 简单的爬虫示例（基于内存队列，因此不支持分布式）
---------
@author: Boris
@email: boris@bzkj.tech
"""

import spider
import json


class TestSingleSpider(spider.SingleSpider):
    def start_requests(self, *args, **kws):
        yield spider.Request("http://www.bj.chinanews.com/focus/1.html")

    def parser(self, request, response):
        for link in response.xpath('//ul[@class="branch_list_ul paging"]//a'):
            title = link.xpath("./text()").extract_first()
            url = link.xpath("./@href").extract_first()

            print("采集到列表 {} {}".format(title, url))

            yield spider.Request(url, title=title, callback=self.parser_detail)

    def parser_detail(self, request, response):
        if response.status_code != 200:
            raise Exception(response)  # 封堵重试

        response.code = "gbk"

        title = request.title
        url = request.url

        content = response.xpath(
            'string(//div[@class=" branch_con_text"])'
        ).extract_first()

        item = {"title": title, "url": url, "content": content}

        print("采集到正文 {}".format(json.dumps(item, indent=4, ensure_ascii=False)))


if __name__ == "__main__":
    test_single_spider = TestSingleSpider(parser_count=100)
    test_single_spider.start()
