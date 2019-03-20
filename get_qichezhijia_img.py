# -*- coding: utf-8 -*-


# Function: 下载汽车之家·图片·产品库中「保时捷718」高清大图
# Python version: 3.6.6
# Author: jackytis
# 微信公众号：「萤享生活」（fireflysharelife）
# Created on: 2019-03-16


import requests
from bs4 import BeautifulSoup
import time


# Step1：从【图1】缩略图页面获取【图2】大图页面的URL

url = 'https://car.autohome.com.cn/pic/series/4175-1-p1.html'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

response = requests.get(url=url, headers=headers)
content = response.text

soup = BeautifulSoup(content, 'lxml')  # 'html.parser'
a_list = soup.select('body > div.content > div > div.column.grid-16.contentright.fn-visible > div:nth-of-type(7) > div > div.uibox > div.uibox-con.carpic-list03.border-b-solid > ul > li > a')

for a in a_list:
    href = a.attrs['href']
    href = 'https://car.autohome.com.cn' + href
    print(href)  

    # Step2：从【图2】大图页面获取图片文件的URL
    
    response = requests.get(url=href, headers=headers)
    content = response.text
    
    soup = BeautifulSoup(content, 'lxml')
    img_list = soup.select('#img')
    
    src = img_list[0].attrs['src']
    src = 'https:' + src
    print(src)
    
    # Step3：下载图片到本地
    
    response = requests.get(url=src, headers=headers)
    content = response.content
    
    file_path = './img/保时捷718/' + src.split('__')[1]
    with open(file_path, 'wb') as f:
        f.write(content)
    
    time.sleep(1)    # 休眠保护

print('='*20 + 'Done!' + '='*20)


