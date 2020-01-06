import requests
from bs4 import BeautifulSoup


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


if __name__ == '__main__':
    start_test()
