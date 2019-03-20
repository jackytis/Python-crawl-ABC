# -*- coding: utf-8 -*-


# Function: 下载汽车之家·图片·产品库中各车型高清大图（def函数方法实现）
# Python version: 3.6.6
# Author: jackytis
# 微信公众号：「萤享生活」（fireflysharelife）
# Created on: 2019-03-22


import requests
import time
import os
from bs4 import BeautifulSoup


# 写入文件，即:将获取的html内容下载到本地，img是二进制，所以用'wb'
def write_to_file(file_path, content):
    with open(file_path, 'wb') as f:
        f.write(content)


# 获取指定url的html响应，复用度高
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    return response


# 通过BeautifulSoup + CSS选择器获取指定节点内容列表
def get_select_list(content, select_path):
    soup = BeautifulSoup(content, 'lxml')
    return soup.select(select_path)


# 下载单页图库的全部图片
def download_img_for_onepage(car_type, page, category=1):

    # Step1 获取图片库列表
    url = 'https://car.autohome.com.cn/pic/series/{}-{}-{}.html'.format(str(car_type), str(category), str(page))
    content = get_html(url).text
    a_list = get_select_list(content, 'body > div.content > div > div.column.grid-16.contentright.fn-visible > div:nth-of-type(7) > div > div.uibox > div.uibox-con.carpic-list03.border-b-solid > ul > li > a')
    dir_name = get_select_list(content, 'head > title')[0].get_text()  # 保存的目录名称
    dir_name = './img/' + dir_name
    if not os.path.exists(dir_name):  # 如果目录不存在，则自动创建
        os.makedirs(dir_name)
    
    # Step2 循环图片库列表，获取每张图片的外链href等信息
    for a in a_list:
        href = 'https://car.autohome.com.cn' + a.attrs['href']
        content = get_html(href).text
        img = get_select_list(content, '#img')[0]
        file_name = get_select_list(content, 'head > title')[0].get_text().split('_')[0] + '.jpg'  # 保存的图片名称
        
        # Step3 获取单张图片的src，并将原图下载到本地路径
        src = 'https:' + img.attrs['src']
        content = get_html(src).content
        file_path = '/'.join((dir_name, file_name))
        write_to_file(file_path, content)
        print('<%s> 下载成功!' % file_name)
        time.sleep(0.5)


# 主函数，即先从该函数开始读取执行
def main():
    start_page = 1
    end_page = 4
    car_type = 4175
    # category = 1  # 1:车身外观; 3:车厢座椅; 10:中控方向盘
    for x in range(start_page, end_page + 1):
        print('\n正在准备下载第%d页...' % x)
        download_img_for_onepage(car_type, 'p%d' % x, 1)
    print('\n' + '='*20 + 'Done!' + '='*20)
 

# .py文件的入口，即整个.py程序首先会从此开始读取执行。
# 同时这里也表示：如果单独运行该.py文件时，main()函数才会执行；否则被其他.py文件import引入时，不会执行main()函数
if __name__ == '__main__':
    main()

