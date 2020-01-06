# !/usr/bin/python
# -*- coding: UTF-8 -*-
import base64
from bs4 import BeautifulSoup
import requests
import random


def base64test():
    with open('D:/python/luck_img/luck_1.jpg', 'rb') as f:  # 以二进制读取图片
        data = f.read()
        encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
        print(str(encodestr, 'utf-8'))  # 重新编码数据


def urltest():
    count = 1
    while count < 10:
        article_id = random.randrange(1000000, 2400000)
        url = "https://www.douguo.com/cookbook/%s.html" % article_id
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
        content = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(content.text, "html.parser")
        if "404" in soup.text:
            print("fetch error")
        else:
            print(str(article_id), soup.select("#left > div.rinfo.relative > h1")[0].get_text())
            print(soup.select("#banner > a > img")[0].get("src"))
        count += 1


def cooklist_test():
    search_url = "https://www.douguo.com/caipu/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    content0 = requests.get(search_url + "土豆", timeout=5, headers=headers)
    soup0 = BeautifulSoup(content0.text, "html.parser")
    cooklist = soup0.select("#left > div.mt25 > ul > li > div > a")
    url = "https://www.douguo.com" + random.sample(cooklist, 1)[0].get("href")
    print(url)
    content = requests.get(url, timeout=5, headers=headers)
    soup = BeautifulSoup(content.text, "html.parser")
    title = soup.select("#left > div.rinfo.relative > h1")[0].get_text()
    pic_url = soup.select("#banner > a > img")[0].get("src")
    print(title, pic_url)


if __name__ == "__main__":
    cooklist_test()
