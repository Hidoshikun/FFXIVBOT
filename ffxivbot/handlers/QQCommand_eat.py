from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import json
import random


def QQCommand_eat(*args, **kwargs):
    try:
        action_list = []
        receive = kwargs["receive"]
        max_cnt = 2400000
        min_cnt = 1000000
        receive_msg = receive["message"].replace("/eat", "", 1).strip()
        msg = ""
        if receive_msg == "":
            flag = False
            while not flag:
                article_id = random.randrange(min_cnt, max_cnt)
                url = "https://www.douguo.com/cookbook/%s.html" % article_id
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
                content = requests.get(url, timeout=5, headers=headers)
                soup = BeautifulSoup(content.text, "html.parser")
                if "404" in soup.text:
                    pass
                else:
                    title = soup.select("#left > div.rinfo.relative > h1")[0].get_text()
                    pic_url = soup.select("#banner > a > img")[0].get("src")
                    msg = title + "[CQ:image,file=%s]" % pic_url
                    flag = True
        else:
            search_url = "https://www.douguo.com/caipu/"
            args = receive_msg.split(" ")
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
            content0 = requests.get(search_url + args[0], timeout=5, headers=headers)
            soup0 = BeautifulSoup(content0.text, "html.parser")
            cooklist = soup0.select("#left > div.mt25 > ul > li > div > a")
            if not cooklist:
                msg = "没有找到相应的搜索结果"
            else:
                url = "https://www.douguo.com" + random.sample(cooklist, 1)[0].get("href")
                content = requests.get(url, timeout=5, headers=headers)
                soup = BeautifulSoup(content.text, "html.parser")
                title = soup.select("#left > div.rinfo.relative > h1")[0].get_text()
                pic_url = soup.select("#banner > a > img")[0].get("src")
                msg = title + "[CQ:image,file=%s]" % pic_url

        reply_action = reply_message_action(receive, msg)
        action_list.append(reply_action)
        return action_list
    except Exception as e:
        msg = "Error: {}".format(type(e))
        action_list.append(reply_message_action(receive, msg))
        logging.error(e)
