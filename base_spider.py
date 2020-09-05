import requests
import os
from bs4 import BeautifulSoup
import time
from typing import Dict

from abc import abstractmethod, ABCMeta


HEADERS = {
    "Accept-Encoding":"gzip",
    "Cache-Control": "max-age=0",
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0b6pre) Gecko/20100903 Firefox/4.0b6pre Firefox/4.0b6pre',
    "Accept-Language":  "zh-CN,zh;q=0.8,en;q=0.6,en-US;q=0.4,zh-TW;q=0.2",
    "Connection" :  "keep-alive",
    "Accept-Encoding" :  "gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

class BaseSpider(metaclass=ABCMeta):
    def __init__(self):
        self.headers = HEADERS

    @abstractmethod
    def transform_url_to_name(self, image_url) -> str:
        raise NotImplementedError

    def set_headers(self, headers:Dict):
        self.headers = headers

    def _html_parser(self, url):  #解析网页的函数
        request_ok = False
        soup = None
        while(not request_ok):
            try:
                r = requests.get(url, headers=self.headers)  #get请求
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                content = r.text
                soup = BeautifulSoup(content, "html.parser")
                request_ok = True
            except:
                print('Request {} failed! wait and try againe...'.format(url))
                time.sleep(1.5)
        time.sleep(0.5)
        return soup

    def _download_image(self, image_url, save_dir):
        image_name = self.transform_url_to_name(image_url)
        image_path = os.path.join(save_dir, image_name)
        request_ok = False
        img_req = None
        while(not request_ok):
            try:
                img_req = requests.get(image_url, stream=True)
                request_ok = True
            except:
                print('get image url: {} failed! wait and try againe...'.format(image_url))
                time.sleep(1.5)
        
        assert img_req is not None, 'img_req is None'
        with open(image_path, 'wb') as f:
            for chunk in img_req.iter_content(chunk_size=32):
                f.write(chunk)
        print('save image: ' +  image_path + " done!")
        time.sleep(0.1)


