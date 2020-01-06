from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import requests


def QQCommand_nmsl(*args, **kwargs):
    action_list = []
    receive = kwargs["receive"]
    try:
        url = u'https://www.nmsl8.club/nmsl'
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        msg = soup.select('#content')[0].get_text().strip()
        # msg = msg.replace('妈', '[CQ:emoji,id=128052]').replace('狗', '[CQ:emoji,id=128054]')
        # result = requests.get('https://nmsl.shadiao.app/api.php?lang=zh_cn')
        # msg = result.text

    except Exception as e:
        msg = "Error: {}".format(type(e))
    reply_action = reply_message_action(receive, msg)
    action_list.append(reply_action)
    return action_list
