from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import json
import random
import requests
import hashlib
from bs4 import BeautifulSoup
import traceback

import time
import hashlib
import random
import string
import requests
from urllib.parse import quote


def QQGroupChat(*args, **kwargs):
    try:
        group = kwargs.get("group", None)
        user_info = kwargs.get("user_info", None)
        action_list = []
        receive = kwargs["receive"]
        bot = kwargs["bot"]
        user_id = receive["user_id"]
        group_id = receive["group_id"]

        try:
            match_replys = CustomReply.objects.filter(group=group, key=receive["message"].strip().split(" ")[0])
            if match_replys.exists():
                item = random.choice(match_replys)
                action_list.append(reply_message_action(receive, item.value))
                return action_list
        except Exception as e:
            print("received message:{}".format(receive["message"]))
            traceback.print_exc()

        # repeat_ban & repeat
        message = receive["message"].strip()
        message_hash = hashlib.md5((message + "|{}".format(bot.user_id)).encode()).hexdigest()
        chats = ChatMessage.objects.filter(group=group, message_hash=message_hash).filter(
            timestamp__gt=int(time.time()) - 60)
        if chats.exists():
            chat = chats[0]
            chat.message = message
            chat.timestamp = int(time.time())
            chat.times = chat.times + 1
            chat.save(update_fields=["timestamp", "times", "message"])
            if (not message.startswith("/")) \
                    and group.repeat_length >= 1 \
                    and group.repeat_prob > 0 \
                    and chat.times >= group.repeat_length \
                    and (not chat.repeated):
                if random.randint(1, 100) <= group.repeat_prob:
                    action_list.append(reply_message_action(receive, chat.message))
                    chat.repeated = True
                    chat.save(update_fields=["repeated"])
        else:
            if group.repeat_ban > 0 or (group.repeat_length >= 1 and group.repeat_prob > 0):
                if receive["self_id"] != receive["user_id"]:
                    chat = ChatMessage(group=group, timestamp=time.time(), message_hash=message_hash)
                    chat.save()

        if "[CQ:at,qq=%s]" % (receive["self_id"]) in receive["message"]:
            question = receive["message"].replace("[CQ:at,qq=1738759322] ", "")
            msg = "[CQ:at,qq=%s] " % (receive["user_id"]) + get_content(question)

            action = reply_message_action(receive, msg)
            action_list.append(action)

        return action_list
    except Exception as e:
        msg = "Error: {}".format(type(e))
        traceback.print_exc()
        logging.error(e)
    return []


def curlmd5(src):
    m = hashlib.md5(src.encode('UTF-8'))
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()


def get_params(plus_item):
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp = str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
    # 应用标志，这里修改成自己的id和key
    app_id = '2125139771'
    app_key = 'wtFLIF1ilpZnBk21'
    params = {'app_id': app_id,
              'question': plus_item,
              'time_stamp': time_stamp,
              'nonce_str': nonce_str,
              'session': '10000'
              }
    sign_before = ''
    # 要对key排序再拼接  
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。  
        sign_before += '{}={}&'.format(key, quote(params[key], safe=''))
        # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾  

    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名  
    sign = curlmd5(sign_before)
    params['sign'] = sign
    return params


def get_content(plus_item):
    # 聊天的API地址
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat"
    # 获取请求参数  
    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item)
    # r = requests.get(url, params=payload)
    r = requests.post(url, data=payload)
    return r.json()["data"]["answer"]
