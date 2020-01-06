from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import json
import random


def QQCommand_erciyuan(*args, **kwargs):
    try:
        action_list = []
        receive = kwargs["receive"]
        if random.randint(1, 100) <= 15:
            msg = "别骂了别骂了"
        else:
            msg = [
                {
                    "type": "image",
                    "data": {
                        "file": "erciyuan/erciyuan (%s).jpg" % (random.randint(1, 254))
                    },
                }
            ]
        reply_action = reply_message_action(receive, msg)
        action_list.append(reply_action)
        return action_list
    except Exception as e:
        msg = "Error: {}".format(type(e))
        action_list.append(reply_message_action(receive, msg))
        logging.error(e)
