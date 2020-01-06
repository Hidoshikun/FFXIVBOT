from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import requests
import random


def QQCommand_mingyan(*args, **kwargs):
    action_list = []
    QQ_BASE_URL = kwargs["global_config"]["QQ_BASE_URL"]
    receive = kwargs["receive"]
    try:
        random_type = ''.join(random.sample(["a", "b", "c"], 1))
        url = "https://v1.hitokoto.cn/?c=" + random_type
        r = requests.get(url=url, timeout=5)
        jdata = json.loads(r.text)
        msg = jdata["hitokoto"] + "\n" + "--From " + jdata["from"]
    except Exception as e:
        msg = "Error: {}".format(type(e))
    reply_action = reply_message_action(receive, msg)
    action_list.append(reply_action)
    return action_list