# coding:utf-8

import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4 import element

class HtmlParser(object):

    def parser(self,page_url,html_cont,expect,deep):
        '''
        用于解析网页内容，抽取URL和数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return: 返回URL和数据
        '''
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'html.parser')
        new_urls = self._get_new_urls(page_url,soup,expect,deep)
        new_data = self._get_new_data(page_url,soup)
        return new_urls,new_data

    def _get_new_urls(self,page_url,soup,expect,deep):
        '''
        抽取新的URL集合
        :param page_url: 下载页面的URL
        :param soup: 页面soup
        :return: 返回新的URL集合
        '''
        result_table = self._get_coverage_table(soup)
        new_urls = set()
        #抽取url
        if result_table:
            links = result_table.find_all("a")
            for link in links:
                #TODO：细化一下判断，抓取到哪个层级：包、类、方法
                new_url = link.text
                # Todo 在expect入参中指定抓取层级
                # 由于service层是一个类多个方法，所有抓取到方法层
                if deep is not None:
                    for item in deep:
                         if item in page_url:
                            new_full_url = urljoin(page_url + "/", new_url)
                            new_urls.add(new_full_url)
                # 只需要new_url在expect中加入到URL 并且 不能是方法（即不包含括号）
                if new_url in expect:
                    # 非service包忽略方法
                    if "(" not in new_url and ")" not in new_url:
                        new_full_url = urljoin(page_url + "/", new_url)
                        new_urls.add(new_full_url)

            return new_urls
        return None

    def _get_new_data(self, page_url, soup):
        '''
        抽取数据
        :param page_url:
        :param soup:
        :return:
        '''
        data = {}
        data['url'] = page_url
        title = soup.find()
        data['parent_name'] = self._get_reference_name(page_url,soup)
        data['child_coverage']=self._get_coverage_datas(page_url,soup)
        return data


    def _get_reference_name(self,page_url,soup):
        '''
        解析该页覆盖率属于哪个 package 或者哪个 class
        :param page_url:
        :param soup: 完整得html
        :return: 如："appframework.core.predef.controller"
        '''
        header = soup.body.find("h2").text
        if len(header.split("paas."))==2:
            return header.split("paas.")[1]     #com.facishare.paas.appframework.core.predef.controller -> appframework.core.predef.controller
        elif header.split(":") ==2:
            return header.split(":")[1]
        elif header !="JaCoCo Coverage Report":
            return header
        else:
            return None


    def _get_coverage_datas(self,page_url,soup):
        '''
        解析 HTML 中覆盖率表格，找到覆盖率数据的所有行
        :param page_url:
        :param soup: 完整的 HTML 数据
        :return: 返回覆盖率数据
        '''
        result_table=self._get_coverage_table(soup)
        if result_table:
            element_list = []
            for child in result_table.children:
                if (type(child) is not element.NavigableString):  # 因为有空行，为NavigableString类型，所以得去掉
                    element_list.append(child)
            datas = {}
            for line in element_list:
                if line.find("a"):
                    data = self._get_data_from_tr(line)
                    datas[data[0]]=data[1]   #如：{"addAction":{"instruction":{"M&C":"","percent":""},...,"class":{"M&C":"","percent":""}}
            return datas
        return None

    def _get_data_from_tr(self,tr):
        name = tr.find("a").text
        coverage_bodys = tr.find_all("table")
        coverage ={}
        type_list = []
        for body in coverage_bodys:
            for type_c in body:
                if (type(type_c) is not element.NavigableString):  # 因为有空行，为NavigableString类型，所以得去掉
                    type_list.append(type_c)
        if (len(type_list) >= 10):
            coverage = {
                "instruction":{"MC":type_list[0].find("span").text,"percent":type_list[1].find("td").text},
                "branch":{"MC":type_list[2].find("span").text,"percent":type_list[3].find("td").text},
                "complexity": {"MC":type_list[4].find("span").text,"percent":type_list[5].find("td").text},
                "line": {"MC":type_list[6].find("span").text,"percent":type_list[7].find("td").text},
                "method": {"MC":type_list[8].find("span").text,"percent":type_list[9].find("td").text},
               # "class": {"MC":type_list[10].find("span").text,"percent":type_list[11].find("td").text},
            }
        if(len(type_list)==12):
            coverage["class"]={"MC":type_list[10].find("span").text,"percent":type_list[11].find("td").text}
        return name,coverage

    def _get_coverage_table(self, soup):
        '''
        解析页面上的覆盖率统计的大表格数据，用于解析子级页面的url和数据
        :param soup:
        :return:
        '''
        result_table=None
        result_table_list = soup.body.find_all("table", attrs={"class": "sortable pane"})
        if(len(result_table_list)>0):
            result_table = result_table_list[0]
        return result_table
