#!/usr/bin/env python3
import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'FFXIV.settings'
from FFXIV import settings

django.setup()
from asgiref.sync import async_to_sync
from ffxivbot.models import *
import re
import json
import time
import requests
import string
import random
import codecs
import urllib
import base64
import logging
import traceback
from bs4 import BeautifulSoup
from channels.layers import get_channel_layer
from django.db import connection, connections

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename="log/crawl_wb.log")


def progress(percent, width=50):
    if percent >= 100:
        percent = 100
    show_str = ('[%%-%ds]' % width) % (int(width * percent / 100) * "#")
    print('\r%s %d%%' % (show_str, percent), end='')


def get_weibotile_share1(weibotile, mode="json"):
    content_json = json.loads(weibotile.content)
    mblog = content_json["mblog"]
    bs = BeautifulSoup(mblog["text"], "html.parser")
    tmp = {
        "url": content_json["scheme"],
        "title": bs.get_text().replace("\u200b", "")[:32],
        "content": "From {}\'s Weibo".format(weibotile.owner),
        "image": mblog["user"]["profile_image_url"],
    }
    res_data = tmp
    if mode == "text":
        res_data = "[[CQ:share,url={},title={},content={},image={}]]".format(tmp["url"], tmp["title"], tmp["content"],
                                                                             tmp["image"])
    logging.debug("weibo_share")
    logging.debug(json.dumps(res_data))
    return res_data


def crawl_wb(weibo_user, push=True):
    uid = weibo_user.uid
    containerid = weibo_user.containerid
    url = r'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid={}'.format(uid, containerid)
    s = requests.post(url=url, timeout=15)
    jdata = json.loads(s.text)
    if jdata["ok"] == 1:
        for tile in jdata["data"]["cards"]:
            if len(WeiboTile.objects.filter(itemid=tile.get("itemid", ""))) > 0:
                # print("crawled {} of {} before, pass".format(tile["itemid"], tile["itemid"]))
                continue
            t = WeiboTile(itemid=tile.get("itemid", ""))
            t.owner = weibo_user
            t.content = json.dumps(tile)
            t.crawled_time = int(time.time())
            if tile.get("itemid", "") == "":
                logging.info("pass a tile of {} cuz empty itemid".format(t.owner))
                continue
            channel_layer = get_channel_layer()

            groups = weibo_user.subscribed_by.all()
            bots = QQBot.objects.all()
            t.save()
            for group in groups:
                for bot in bots:
                    group_id_list = [item["group_id"] for item in json.loads(bot.group_list)]
                    if int(group.group_id) not in group_id_list:
                        continue
                    try:
                        if True:
                            content_json = json.loads(t.content)
                            mblog = content_json["mblog"]
                            bs = BeautifulSoup(mblog["text"], "html.parser")
                            if "original_pic" in mblog.keys():
                                text = "{}\n{}".format(
                                    "{}\'s Weibo:\n========".format(t.owner),
                                    bs.get_text().replace("\u200b", "").strip()
                                )
                                msg = [
                                    {"type": "text", "data": {"text": text}, },
                                    {"type": "image", "data": {"file": mblog["original_pic"]}, }
                                ]
                            else:
                                msg = "{}\n{}".format(
                                    "{}\'s Weibo:\n========".format(t.owner),
                                    bs.get_text().replace("\u200b", "").strip()
                                )
                        if push:
                            t.pushed_group.add(group)
                            jdata = {
                                "action": "send_group_msg",
                                "params": {"group_id": int(group.group_id), "message": msg},
                                "echo": "",
                            }
                            async_to_sync(channel_layer.send)(bot.api_channel_name,
                                                              {"type": "send.event", "text": json.dumps(jdata), })

                    except requests.ConnectionError as e:
                        logging.error("Pushing {} to group: {} ConnectionError".format(t, group))
                    except requests.ReadTimeout as e:
                        logging.error("Pushing {} to group: {} timeout".format(t, group))
                    except Exception as e:
                        traceback.print_exc()
                        logging.error("Error at pushing crawled weibo to {}: {}".format(group, e))

            logging.info("crawled {} of {}".format(t.itemid, t.owner))
    else:
        logging.error("Error at crawling weibo:{}".format(jdata.get("ok", "NULL")))
    return


def crawl():
    weibo_users = WeiboUser.objects.all()
    for user in weibo_users:
        logging.info("Begin crawling {}".format(user.name))
        try:
            crawl_wb(user, True)
        except requests.ReadTimeout as e:
            logging.error("crawling {} timeout".format(user.name))
        except Exception as e:
            traceback.print_exc()
            logging.error(e)
        time.sleep(1)
        logging.info("Crawl {} finish".format(user.name))


if __name__ == "__main__":
    print("Crawling Weibo Service Start, check log file log/crawl_wb.log")
    while True:
        try:
            crawl()
        except BaseException:
            logging.error("Error")
        time.sleep(60)
