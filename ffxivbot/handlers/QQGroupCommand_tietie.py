from .QQEventHandler import QQEventHandler
from .QQUtils import *
from ffxivbot.models import *
import logging
import json
import random


def QQGroupCommand_tietie(*args, **kwargs):
    try:
        global_config = kwargs["global_config"]
        action_list = []
        receive = kwargs["receive"]
        group_id = receive["group_id"]

        # 更新成员信息
        action_list.append({
            "action": "get_group_member_list",
            "params": {"group_id": group_id},
            "echo": "get_group_member_list:%s" % group_id
        })

        msg = ""
        group = QQGroup.objects.get(group_id=group_id)
        member_list = json.loads(group.member_list)

        member_list1 = sorted(member_list, key=lambda i: i['last_sent_time'], reverse=True)
        member_list2 = member_list1[:5]
        two_member = random.sample(member_list2, 2)
        for member in two_member:
            msg = "[CQ:at,qq=%s] " % (member["user_id"]) + msg

        msg = msg + "贴贴~"

        reply_action = reply_message_action(receive, msg)
        action_list.append(reply_action)
        return action_list
    except Exception as e:
        msg = "Error: {}".format(type(e))
        action_list.append(reply_message_action(receive, msg))
        logging.error(e)
