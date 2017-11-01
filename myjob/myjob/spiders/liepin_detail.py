import scrapy
import configparser
import os
import time

class LiepinSpider(scrapy.spiders.Spider):
    name = "liepin"
    allowed_domains = ["www.liepin.com"]
    start_urls =[]
    data_source = "liepin"
    domain = "https://www.liepin.com"
    path = "/zhaopin/"

    def __init__(self):
        self.start_urls = self.__init_start_urls()



    def __init_start_urls(self):
        a = []

        params = {}
        # default value
        params["industries"] = ""
        params["dqs"] = "010"
        params["salary"] = "50$100"
        params["jobKind"] = ""
        params["pubTime"] = ""
        params["compkind"] = ""
        params["compscale"] = ""
        params["industryType"] = ""
        params["searchType"] = "1"
        params["clean_condition"] = ""
        params["isAnalysis"] = ""
        params["init"] = "1"
        params["sortFlag"] = "15"
        params["flushckid"] = "0"
        params["fromSearchBtn"] = "1"
        params["headckid"] = "0fe19ebe8682770e"
        params["d_headId"] = "53fff7f31621f3984070ff45e8f7eea1"
        params["d_ckId"] = "7bf47b5b504dbb8cb9d24165dc6baa3a"
        params["d_sfrom"] = "search_fp_nvbar"
        params["d_curPage"] = 0
        params["d_pageSize"] = "40"
        params["siTag"] = "1B2M2Y8AsgTpgAmY7PhCfg~F5FSJAXvyHmQyODXqGxdVw"
        params["key"] = "java+%E6%9E%B6%E6%9E%84%E5%B8%88"
        for i in range(0,3):

            url = self.domain+self.path+"?"
            for k in params.keys():
                url += "&"+k + "="+str(params[k])
            a.append(url)
        return a

###https://www.liepin.com/zhaopin/?pubTime=&ckid=f7257d56dc3e3ccf&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&flushckid=1&dqs=&industryType=&jobKind=&sortFlag=15&industries=dqs%3D010salary%3DjobKind%3DpubTime%3Dcompkind%3Dcompscale%3DindustryType%3DsearchType%3D1clean_condition%3DisAnalysis%3Dinit%3D1sortFlag%3D15flushckid%3D0fromSearchBtn%3D1headckid%3D0fe19ebe8682770ed_headId%3D53fff7f31621f3984070ff45e8f7eea1d_ckId%3D7bf47b5b504dbb8cb9d24165dc6baa3ad_sfrom%3Dsearch_fp_nvbard_curPage%3D0d_pageSize%3D40siTag%3D1B2M2Y8AsgTpgAmY7PhCfg~F5FSJAXvyHmQyODXqGxdVwkey%3Djava+%E6%9E%B6%E6%9E%84%E5%B8%88&salary=50$100&compscale=&key=java+%E6%9E%B6%E6%9E%84%E5%B8%88&clean_condition=&headckid=f7257d56dc3e3ccf&d_pageSize=40&siTag=8xn0k0zRebZDOrQMslcvBQ~SB9Rk-aix1mtHcCm-tdqGg&d_headId=876346d8f0a98afc194bb93502aa665f&d_ckId=876346d8f0a98afc194bb93502aa665f&d_sfrom=search_prime&d_curPage=0

#"https://www.liepin.com/zhaopin/?industries=&dqs=010&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&searchType=1" \
#"&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=0fe19ebe8682770e" \
#"&d_headId=53fff7f31621f3984070ff45e8f7eea1&d_ckId=7bf47b5b504dbb8cb9d24165dc6baa3a&d_sfrom=search_fp_nvbar" \
#"&d_curPage=0&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~F5FSJAXvyHmQyODXqGxdVw&key=java+%E6%9E%B6%E6%9E%84%E5%B8%88http"
    def parse(self, response):
        dp = response.xpath('//div[@class="job-info"]/h3/a/@href').extract()
        #print(dp)
        filename = response.url.split("/")[-2]
        data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        data_dir=data_dir+"/data/original/"+self.data_source+"/detail/"
        print(data_dir)
        with open(filename, 'wb') as f:
            f.write(response.body)
        for p in dp:
            if not p.startswith("http"):
                p = self.domain + p
            id = p.replace(self.domain,"").replace("/a/","").replace("/job/","").replace(".shtml","");
            #print(id)
            data_file_dir = data_dir+"/"+id
            if not os.path.exists(data_file_dir):
                os.makedirs(data_file_dir)
            data_file_path = data_file_dir+"/"+id+".ini";
            conf = configparser.ConfigParser()
            conf.add_section('config')  # 添加section
            conf.set('config', 'id', id)
            conf.set('config', "url", p)
            conf.set('config', 'domain', self.domain)
            conf.set('config', 'last_time', time.strftime('%Y-%m-%d %H:%M:%S'))
            with open(data_file_path, 'w') as f:
                conf.write(f)


