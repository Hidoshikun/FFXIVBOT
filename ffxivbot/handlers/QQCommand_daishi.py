from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import json
import random


def QQCommand_daishi(*args, **kwargs):
    try:
        action_list = []
        receive = kwargs["receive"]
        msg = [
            {
                "type": "image",
                "data": {
                    "file": "daishi/daishi (%s).jpg" % (random.randint(1, 123))
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
