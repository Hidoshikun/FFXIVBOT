import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'FFXIV.settings'
from FFXIV import settings

django.setup()
import requests
from bs4 import BeautifulSoup
from ffxivbot.models import *
import base64


def start_test():
    count = 1
    while count <= 100:
        url = r'https://www.zgjm.net/chouqian/guanyinlingqian/%s.html' % count
        s = requests.post(url=url, timeout=5)
        soup = BeautifulSoup(s.text, "html.parser")
        total = soup.select(".article-content > p")
        text = ""
        for elem in total:
            line = elem.get_text().strip()
            if len(line) != 0:
                text = text + elem.get_text().strip() + "\n"

        text = text.replace('❃ ', '') + "\n私聊獭獭也可以抽，抽到凶签也不要气馁！每天只能抽一次哦~"
        print(count)
        filename = 'luck/luck_%s.txt' % count
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        count += 1


def dump_data():
    for i in range(1, 101):
        pic = open('luck_img/luck_%s.jpg' % i, 'rb')
        file = open('luck/luck_%s.txt' % i, mode='r', encoding='utf8')
        pic_data = pic.read()
        data = file.read()
        encodestr = base64.b64encode(pic_data)  # 得到 byte 编码的数据
        base64_string = encodestr.decode('utf-8')
        t = LuckData(number=i)
        t.text = data
        t.pic_base64 = base64_string
        t.save()
        print(str(i) + "success")


def decode_base64():
    t = LuckData.objects.filter(number=1)
    str = t[0].pic_base64
    data = base64.b64decode(str)
    pic = open("test.jpg", "wb")
    pic.write(data)
    pic.close()


if __name__ == '__main__':
    decode_base64()
