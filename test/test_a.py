from coverageSpider.DataOutput import DataOutput
from coverageSpider.HtmlDownLoader import HtmlDownLoader
from coverageSpider.UrlManager import UrlManager
from coverageSpider.HtmlParser import HtmlParser
from bs4 import element
from bs4 import BeautifulSoup
import bs4


if __name__=="__main__":
   # param = sys.argv
   jenkins_num = ""
   # if len(param) ==1 :
   #     if isinstance(param[0],"number"):
   #         jenkins_num = param[0]
   # jenkins_address = ""
   # jacoco_url = jenkins_address + jenkins_num +"/jacoco/"
   # html_report = open('../test_html/jacoco1.html', 'r')
   # soup = BeautifulSoup(html_report, 'html.parser')
   # #print(soup)
   # result_table = soup.body.find_all("table", attrs={"class": "sortable pane"})[0]
   # html_parser = HtmlParser()
   #datas = html_parser.get_coverage_datas(jacoco_url,soup)
   #print(len(datas.keys()))

   # links = result_table.find_all("a")
   # # for link in links:
   # #    print(link.text)
   #
   # header = soup.body.find("h2").text
   # print(header)
   ue ="'https://jenkins2.foneshare.cn/job/k8s-jacoco/78/jacoco/'"
   l = ue
   print(len(ue.split("/")))
   print('appframework1' in ue)
   # if ue.index('appframework1')>0:
   #    print('11')

   present = int("50%".split('%')[0])
   print(present)