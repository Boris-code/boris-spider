# -*- coding: utf-8 -*-
"""
Created on 2020/4/22 10:41 PM
---------
@summary:
---------
@author: Boris
@email: boris@bzkj.tech
"""

import spider


class DemoSpider(spider.SingleSpider):
    def start_requests(self, *args, **kws):
        yield spider.Request("https://www.baidu.com")

    def parser(self, request, response):
        print(response.text)


if __name__ == "__main__":
    DemoSpider().start()
