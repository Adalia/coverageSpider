# coding:utf-8

import codecs
import csv
import os
from urllib.parse import urljoin
class DataOutput(object):

    def __init__(self):
        self.datas = []

    def store_data(self,data):
        if data is None:
            return

       # headers =['主属性',"上级","业务类型","指令","指令覆盖率","分支","分支覆盖率","圈复杂度","圈覆盖率","行","行覆盖率","方法","方法覆盖率","类","类覆盖率","业务类型"]
        headers =self._get_headers()
        rows = self._datas_to_csv(data)
        #Todo:判断输出数据的业务类型
        #Todo:增加自定义文件名
        if rows:
            if os.path.exists("JsonOutput/result.csv"):
                with open("JsonOutput/"+"result"+".csv",'a') as f:  #增量更新
                    f_csv = csv.DictWriter(f,headers)
                    f_csv.writerows(rows)

            else:
                with open("JsonOutput/result.csv",'w') as f:  #清空文件并写入
                    f_csv = csv.DictWriter(f,headers)
                    f_csv.writeheader()
                    f_csv.writerows(rows)


    def _datas_to_csv(self,datas):
        rows = []
        print(datas["url"])
        parent_name = datas["parent_name"]
        parent_url = datas["url"]
        record_type = "预设业务类型"
        coverage_datas = datas["child_coverage"]
        if coverage_datas:
            for name,coverage in coverage_datas.items():
                if("$Result" in name or "$Arg" in name ):
                    print(name)
                else:
                    row = {}
                    row["主属性（必填）"] = self._formatting_name(name, parent_name)
                    row["业务类型（必填）"] = record_type
                    row["链接"] = self._formatting_url(parent_url, name)
                    row["上级"] = self._formatting_parent_name(parent_name, parent_url)
                    row["branch覆盖数量"] = coverage["branch"]["MC"]
                    row["branch覆盖率"] = self._formatting_coverage_percent(coverage["branch"]["percent"])
                    row["line覆盖数量"] =coverage["line"]["MC"]
                    row["line覆盖率"] = self._formatting_coverage_percent(coverage["line"]["percent"])
                    row["类型"]=self._formatting_type(parent_name)
                    row["负责人（必填）"]="李海荟"
                    rows.append(row)
                
            return rows
        return None

    def _get_headers(self):
        return ['主属性（必填）', "业务类型（必填）", "链接", "上级", "branch覆盖数量", "branch覆盖率", "line覆盖数量", "line覆盖率", "类型", "负责人（必填）"]

    #Todo主属性避免重名，需要定义下输入内容，增加上级的最后一级,如[service]ButtonService
    def _formatting_name(self,name,parent):
        if "com.facishare.paas." in name:
            name = name.split('com.facishare.paas.')
            if len(name)==2:
                return name[1]

        elif parent is not None and "appframework" in parent: #类
            name_list = parent.split(".")
            return "["+name_list[len(name_list)-1]+"]"+name

        else:
           parent = parent.split('Package:')[1]
           return "[" + parent.strip() + "]"+name


    def _formatting_parent_name(self, parent,url):
        if parent is not None and "." not in parent: #方法的父级要添加[action]命名,从上级的URL中获取
            flag_list = url.split("/")   #https://jenkins2.foneshare.cn/job/k8s-jacoco/109/jacoco/com.facishare.paas.appframework.core.predef.service/TagService
            flag_url_p = flag_list[len(flag_list)-2].split(".") #com.facishare.paas.appframework.core.predef.service
            flag = flag_url_p[len(flag_url_p)-1]  #得到service
            parent = "[" + flag + "]" + parent.split('Package:')[1].strip()
            return parent
        return parent

    def _formatting_url(self, parent_url,name):
        #如果是方法，返回父的url
        if "(" in name or "{" in name:   #如果是方法级别的，URL直接返回父级的，不进入方法层
            return parent_url

        elif "$" not in name:  # 自定义对象中的URL不可以包含$
            return urljoin(parent_url + '/', name)   #如果不是方法级别的，URL增加一层，直接访问到包或类

        return ''

    def _formatting_type(self, parent_name):
        if parent_name is None or len(parent_name)==0:
            return '包'
        elif "appframework" in parent_name:
            return '类'
        else:
            return '方法'
        return ""

    def _formatting_coverage_percent(self, percent):
        #Todo: 百分数转换成数字，这样导入进入就是正常的百分数
        if (percent is None) or ('%' not in percent):
            return ''
        return int(percent.split('%')[0])

    def _get_headers(self):
        return ['主属性（必填）',"业务类型（必填）","链接","上级","branch覆盖数量","branch覆盖率","line覆盖数量","line覆盖率","类型","负责人（必填）"]