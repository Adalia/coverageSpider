# coding:utf-8

import requests

class HtmlDownLoader(object):
    def download(self,url):
        if url is None:
            return None

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        if response.status_code ==200:
            response.encoding='utf-8'
            return response.text
        return None