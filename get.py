# import requests
# #
# # response = requests.get("http://jenkins2.foneshare.cn/job/k8s-jacoco/44/jacoco/com.facishare.paas.appframework.core.predef.controller/")
# #
# # print(response.text)

import requests
from bs4 import element
from bs4 import BeautifulSoup
import bs4
import codecs    #codecs可以很方便地对文本文件进行编码和解码
import re
from urllib.parse import urljoin
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
headers = {'User-Agent':user_agent}
#由于我的终端不支持汉语，下面链接中的汉字在复制的过程中已经被转码，不要紧
#url = "http://jenkins2.foneshare.cn/job/k8s-jacoco/44/jacoco/com.facishare.paas.appframework.core.predef.controller/"
#response = requests.get(url, headers = headers)
#response.encoding = 'utf-8'    #使用utf-8对内容编码
# f = codecs.open('/home/***/test.txt', 'w', encoding='utf-8')
# f.write(r.text)
# f.close()
#print(response.text)
'''报错：MarkupResemblesLocatorWarning: "/Users/lihaihui/test_html/jacoco1.html" looks like a filename, not markup. You should probably open this file and pass the filehandle into Beautiful Soup.
soup = BeautifulSoup('../test_html/jacoco1.html', 'html.parser')
'''

#修改为
html_report = open('test_html/jacoco1.html','r')
soup = BeautifulSoup(html_report, 'html.parser')
#soup = BeautifulSoup(html_report, 'lxml')
#print(soup.prettify())
#解析包的覆盖率


#解析包->类的覆盖率
#<h2>可以获取归属包、类
# header = soup.body.find("h2").text
# b=header.split("paas.")[1]
# print(b)
# print(header)
result_table = soup.body.find_all("table",attrs={"class": "sortable pane"})[0]
# #
# new_urls = set()
# #抽取url
# links = result_table.find_all("a")
# base_url = "http://jenkins2.foneshare.cn/job/k8s-jacoco/47/jacoco/"
# for link in links:
#     new_url = link['href']
#     if "$" not in new_url and "Arg" not in new_url:
#         new_full_url = urljoin(base_url,new_url)
#         new_urls.add(new_full_url)
#


# print(len(new_urls))
#
# ptn = r"$"
# print(re.search(ptn, "Ab$stractStanda$rdAsyncBulkAction$Result"))

#tag的.contents属性可以将tag子节点已列表的方式输出
result_trs = result_table.contents  #两个list中间有个元素是 '//print(result_table.prettify())
#print(len(result_trs))
element_list = []
for child in result_table.children:
    #if(isinstance(child,bs4.element.Tag)):
    if type(child) is not bs4.element.NavigableString:#因为有空行，为NavigableString类型，所以得去掉
        element_list.append(child)


   # print(type(child))

data = {}
print(element_list[1])
print("**************************")
name = element_list[1].find("a").text
print(name)
coverage_bodys = element_list[1].find_all("table")
print(len(coverage_bodys))
print("*************77*************")
type_list = []
for body in coverage_bodys:
    for type_c in body:
        if type(type_c) is not element.NavigableString:  # 因为有空行，为NavigableString类型，所以得去掉
           # print(child.prettify())
            type_list.append(type_c)

print(len(type_list))
print(type_list[0].find("span").text)
print(type_list[1].find("td").text)

#if type(sec) is not bs4.element.NavigableString