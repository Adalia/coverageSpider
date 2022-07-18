# coding:utf-8

from DataOutput import DataOutput
from HtmlDownLoader import HtmlDownLoader
from UrlManager import UrlManager
from HtmlParser import HtmlParser
import sys
class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownLoader()
        self.output = DataOutput()
        self.parser = HtmlParser()

    def crawl(self,root_url,expect,deep,project):
        # 添加入口 URL
        self.manager.add_new_url(root_url)
        # 判断 url 管理器中是否有新的 url()，同时判断抓去了多少个 url
        while(self.manager.has_new_url()):
          #  try:
                # 从 URL 管理器获取新的 URL
                new_url = self.manager.get_new_url()
                # 下载网页
                html = self.downloader.download(new_url)
                # 解析网页，提取数据和 url
                new_urls,data = self.parser.parser(new_url,html,expect,deep)
                # 将抽取的 URL 添加到 URL 管理器中
                if new_urls:
                    self.manager.add_new_urls(new_urls)
                # 存储数据
                if data:
                    self.output.store_data(data,project)

            # except Exception as e:
            #     print("crawl failed")
            #     print(e)

if __name__=="__main__":
    param = sys.argv
    jenkins_address = "https://jenkins2.foneshare.cn/job/k8s-jacoco/"

    jenkins_num = "238"
    jacoco_url = jenkins_address + jenkins_num + "/jacoco"

    project="com.facishare.paas.appframework"
    expect = ["com.facishare.paas.appframework.core.predef.service",  "com.facishare.paas.appframework.core.predef.action", "com.facishare.paas.appframework.core.predef.controller"]
    need_method =  ["com.facishare.paas.appframework.core.predef.service"]

    spider_man = SpiderMan()
    spider_man.crawl(jacoco_url, expect, need_method, project)

    ##社交组测试
    # jenkins_num = "308"
    # jacoco_url = jenkins_address + jenkins_num + "/jacoco"
    # # jacoco_url_1 = "https://jenkins2.foneshare.cn/job/k8s-jacoco/98/jacoco/com.facishare.paas.appframework.core.predef.service/"
    # expect = ["com.facishare.social.device.predefine.action", "com.facishare.social.device.predefine.controller",
    #           "com.facishare.social.device.predefine.service"]
    # need_method = "com.facishare.social.device.predefine.service"
    # project = "com.facishare.social"
    # spider_man = SpiderMan()
    # spider_man.crawl(jacoco_url, expect, need_method, project)
