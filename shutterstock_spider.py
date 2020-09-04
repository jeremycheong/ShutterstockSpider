from bs4 import BeautifulSoup
import bs4
from base_spider import BaseSpider
from typing import Dict, List
import os
import config as cfg
from tqdm import tqdm
import time


class ShutterstockSpider(BaseSpider):
    def __init__(self, doman_url, save_dir=None) -> None:
        super(ShutterstockSpider, self).__init__()
        if save_dir is None:
            save_dir =  './downloads'
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

        self.save_dir = save_dir
        self.doman_url = doman_url


    def transform_url_to_name(self, image_url: str) -> str:
        return image_url.split('/')[-1].split('-')[-1]


    def get_image_info(self, image_soup_tag:bs4.element.Tag) -> Dict:
        image_info_tag = image_soup_tag.find('a').find('img')
        image_little_src = image_info_tag.get('src')
        if image_little_src is None:
            print('image_soup_tag info:\n', image_soup_tag)
            return None
        image_little_src_list = image_little_src.split('/')
        image_url_doman = '/'.join(image_little_src_list[:-1])

        image_complete_name_list = image_little_src_list[-1].split('-')
        image_name = image_complete_name_list[-1]
        image_pre_info = '-'.join(image_complete_name_list[:-2])
        image_mid_src = '{}/{}-{}-{}'.format(image_url_doman, image_pre_info, '600w', image_name)
        image_location_info = '-'.join(image_info_tag.get('alt').lower().replace(',', ' ').split()[:-2])
        preview_image_url = 'https://image.shutterstock.com/z/' + 'stock-photo-' + image_location_info + '-' + image_name
        return {'image_little_src': image_little_src,
                'image_mid_src': image_mid_src,
                'image_preview_src': preview_image_url}


    def catch_all_image_url_per_page(self, page_url: str) -> None:
        image_little_urls = open(os.path.join(self.save_dir, 'image_little_urls.txt'), 'w')
        image_mid_urls = open(os.path.join(self.save_dir, 'image_mid_urls.txt'), 'w')
        image_preview_urls = open(os.path.join(self.save_dir, 'image_preview_urls.txt'), 'w')
        error_soup_tag_info = open(os.path.join(self.save_dir, 'error_soup_info.txt'), 'w')
        time.sleep(2)
        image_soup_tags = self._html_parser(page_url).find_all('div', 'z_h_b900b')
        print('image_soup_tags len: ', len(image_soup_tags))
        for image_soup_tag in (image_soup_tags):
            image_info = self.get_image_info(image_soup_tag)
            if image_info is None:
                print('error soup tag...')
                error_soup_tag_info.write('{}\n\n'.format(image_soup_tag))
                continue

            image_little_urls.write('%s\n' % image_info['image_little_src'])
            image_mid_urls.write('%s\n' % image_info['image_mid_src'])
            image_preview_urls.write('%s\n' % image_info['image_preview_src'])

        image_little_urls.close()
        image_mid_urls.close()
        image_preview_urls.close()


    def analysis_page(self, key_words:List) -> None:
        page_url = '{}/{}?image_type=photo'.format(self.doman_url, '+'.join(key_words))
        # page_soup = self._html_parser(page_url)
        # page_cnt = page_soup.find('div', 'b_aE_c6506').get_text().split()[1]
        # print('共 %s 页' % page_cnt)
        self.catch_all_image_url_per_page(page_url)
        # for page_id in range(1, int(page_cnt) + 1):
        #     print('catch the page %d image url' % page_id)
        #     url_per_page = page_url + '&page=' + str(page_id)
        #     self.catch_all_image_url_per_page(url_per_page)


def test_analysis():
    # soup = BeautifulSoup(info_test, features='html.parser')
    # image_src = 'https://image.shutterstock.com/image-photo/mud-slide-on-coast-village-260nw-790332325.jpg'
    # image_src_list = image_src.split('/')
    # print('/'.join(image_src_list[:-1]))
    image_location = 'mud slide on coast village road montecito, california usa january, 9, 2017'
    print(image_location.lower().replace(',', ' ').split()[:-2])

if __name__ == '__main__':
    key_words = ['mudslide', 'mud']
    shutterstock_spider = ShutterstockSpider(cfg.domain)
    shutterstock_spider.analysis_page(key_words)
    # test_analysis()