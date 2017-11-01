import scrapy

class LiepinSpider(scrapy.spiders.Spider):
    name = "liepin"
    allowed_domains = ["www.liepin.com"]
    start_urls = [
        "https://www.liepin.com/zhaopin/?industries=&dqs=010&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&searchType=1&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=0fe19ebe8682770e&d_headId=53fff7f31621f3984070ff45e8f7eea1&d_ckId=7bf47b5b504dbb8cb9d24165dc6baa3a&d_sfrom=search_fp_nvbar&d_curPage=0&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~F5FSJAXvyHmQyODXqGxdVw&key=java+%E6%9E%B6%E6%9E%84%E5%B8%88",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)