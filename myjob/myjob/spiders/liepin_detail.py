import scrapy
import configparser
import os

class LiepinDetailSpider(scrapy.spiders.Spider):
    name = "liepin_detail"
    allowed_domains = ["www.liepin.com"]
    start_urls =[]
    data_source = "liepin"
    domain = "https://www.liepin.com"
    data_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    data_dir = data_dir + "/data/original/" + data_source + "/detail/"

    def __init__(self):
        self.start_urls = self.__init_start_urls()



    def __init_start_urls(self):
        a = []
        conf = configparser.ConfigParser()
        if os.path.exists(self.data_dir):
            files = os.listdir(self.data_dir)
            for file_name in files:
                conf_path = self.data_dir+file_name+"/"+file_name+".ini"
                if os.path.exists(conf_path):
                    conf.read(conf_path);
                    url = conf.get("config","url")
                    a.append(url)

        return a

###https://www.liepin.com/zhaopin/?pubTime=&ckid=f7257d56dc3e3ccf&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&flushckid=1&dqs=&industryType=&jobKind=&sortFlag=15&industries=dqs%3D010salary%3DjobKind%3DpubTime%3Dcompkind%3Dcompscale%3DindustryType%3DsearchType%3D1clean_condition%3DisAnalysis%3Dinit%3D1sortFlag%3D15flushckid%3D0fromSearchBtn%3D1headckid%3D0fe19ebe8682770ed_headId%3D53fff7f31621f3984070ff45e8f7eea1d_ckId%3D7bf47b5b504dbb8cb9d24165dc6baa3ad_sfrom%3Dsearch_fp_nvbard_curPage%3D0d_pageSize%3D40siTag%3D1B2M2Y8AsgTpgAmY7PhCfg~F5FSJAXvyHmQyODXqGxdVwkey%3Djava+%E6%9E%B6%E6%9E%84%E5%B8%88&salary=50$100&compscale=&key=java+%E6%9E%B6%E6%9E%84%E5%B8%88&clean_condition=&headckid=f7257d56dc3e3ccf&d_pageSize=40&siTag=8xn0k0zRebZDOrQMslcvBQ~SB9Rk-aix1mtHcCm-tdqGg&d_headId=876346d8f0a98afc194bb93502aa665f&d_ckId=876346d8f0a98afc194bb93502aa665f&d_sfrom=search_prime&d_curPage=0

#"https://www.liepin.com/zhaopin/?industries=&dqs=010&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&searchType=1" \
#"&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=0&fromSearchBtn=1&headckid=0fe19ebe8682770e" \
#"&d_headId=53fff7f31621f3984070ff45e8f7eea1&d_ckId=7bf47b5b504dbb8cb9d24165dc6baa3a&d_sfrom=search_fp_nvbar" \
#"&d_curPage=0&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~F5FSJAXvyHmQyODXqGxdVw&key=java+%E6%9E%B6%E6%9E%84%E5%B8%88http"
    def parse(self, response):
        content = response.xpath('//div[@class="content content-word"]/text()').extract()

        title = response.xpath('//div[@class="job-note"]/h5/text()').extract()
        #if len(title)==0:
        #    title = response.xpath('//div[@class="title-info"]//h1/text()').extract()


        #company = response.xpath('//div[@class="title-info"]//h3/text()').extract()
        company = response.xpath('//div[@class="job-note"]//a/text()').extract()
        if len(company) == 0:
            company = response.xpath('//div[@class="job-note"]//span/text()').extract()
        salary = response.xpath('//div[@class="job-note"]//p/text()').extract()
        id = response.url.split("/")[-1].replace(".shtml","")
        file_dir = self.data_dir+id
        file_name = file_dir+"/"+id+".html"
        if os.path.exists(file_name):
            os.remove(file_name);
        with open(file_name, 'wb') as f:
            f.write(response.body)


        file_name_content = file_dir+"/"+id+"_content.txt"
        if os.path.exists(file_name_content):
            os.remove(file_name_content)
        with open(file_name_content, 'w') as f:
            for t in content:
                t = t.strip()
                t = t.replace("\n","").replace("\r","")
                if t!='':
                    f.write(t+"\n")

        file_name_data = file_dir + "/" + id + "_data.ini"
        if os.path.exists(file_name_data):
            os.remove(file_name_data)
        conf = configparser.ConfigParser()
        conf.add_section("data");
        if len(title) > 0:
            conf.set("data", "title", title[0].strip().replace("\r","").replace("\n",""))
        else:
            print("title empty id:"+id)

        if len(company) > 0:
            conf.set("data", "company", company[0].strip().replace("\r","").replace("\n",""))
        else:
            print("company empty id:" + id)
        if len(salary) > 0:
            conf.set("data", "salary", salary[0].strip().replace("\r","").replace("\n",""))
        else:
            print("salary empty id:" + id)
        with open(file_name_data, 'w') as f:
            conf.write(f)


