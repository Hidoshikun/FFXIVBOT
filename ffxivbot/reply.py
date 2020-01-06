import random
import sys
import os

from FFXIV import settings
import django
import requests
from django.db import transaction
import logging

from channels.layers import get_channel_layer
from channels.exceptions import StopConsumer

from asgiref.sync import async_to_sync
import ffxivbot.handlers as handlers
from ffxivbot.models import *

django.setup()
channel_layer = get_channel_layer()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFXIVBOT_ROOT = os.environ.get("FFXIVBOT_ROOT", BASE_DIR)
sys.path.append(FFXIVBOT_ROOT)
os.environ["DJANGO_SETTINGS_MODULE"] = "FFXIV.settings"

CONFIG_PATH = os.environ.get(
    "FFXIVBOT_CONFIG", os.path.join(FFXIVBOT_ROOT, "ffxivbot/config.json")
)
config = json.load(open(CONFIG_PATH, encoding="utf-8"))

LOGGER = logging.getLogger(__name__)


def reply_heartbeat(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    LOGGER.debug(
        "bot:{} Event heartbeat at time:{}".format(
            receive["self_id"], int(time.time())
        )
    )
    call_api(bot, "get_status", {}, "get_status:{}".format(receive["self_id"]),
             post_type=receive.get("reply_api_type", "websocket"))


def get_help_msg(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    group_id = (receive["group_id"] if receive["message_type"] == "group" else None)
    user_id = (receive["user_id"] if receive["message_type"] != "group" else None)
    msg = "通用命令请见/normal_help，\n群命令见/group_help, \nFF14命令见/ff14_help\n"
    msg += "Based on: {}\n".format(
        "https://github.com/Bluefissure/FFXIVBOT/wiki/"
    )
    msg = msg.strip()
    send_message(bot, receive["message_type"], group_id or user_id, msg)


def get_normal_help_msg(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    group_id = (receive["group_id"] if receive["message_type"] == "group" else None)
    user_id = (receive["user_id"] if receive["message_type"] != "group" else None)
    msg = ""
    for (k, v) in handlers.commands.items():
        msg += "{}: {}\n".format(k, v)
    msg += "Based on: {}\n".format(
        "https://github.com/Bluefissure/FFXIVBOT/wiki/"
    )
    msg = msg.strip()
    send_message(bot, receive["message_type"], group_id or user_id, msg)


# 处理ff14_help
def get_ff14_help_msg(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    group_id = (receive["group_id"] if receive["message_type"] == "group" else None)
    user_id = (receive["user_id"] if receive["message_type"] != "group" else None)
    msg = ""
    for (k, v) in handlers.ff14_commands.items():
        msg += "{}: {}\n".format(k, v)
    msg += "Based on: {}\n".format(
        "https://github.com/Bluefissure/FFXIVBOT/wiki/"
    )
    msg = msg.strip()
    send_message(bot, receive["message_type"], group_id or user_id, msg)


# 处理group_help
def get_group_help_msg(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    (group, group_created) = QQGroup.objects.get_or_create(group_id=receive["group_id"])
    member_list = json.loads(group.member_list)
    msg = ("" if member_list else "本群成员信息获取失败，请尝试重启酷Q并使用/update_group刷新群成员信息\n")
    for (k, v) in handlers.group_commands.items():
        msg += "{}: {}\n".format(k, v)
    msg = msg.strip()
    send_message(bot, receive["message_type"], receive["group_id"], msg)


# 处理ping
def get_ping_msg(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    discuss_id = receive["discuss_id"]
    group_id = receive["group_id"]
    user_id = receive["user_id"]
    msg = ""
    if "detail" in receive["message"]:
        msg += "[CQ:at,qq={}]\ncoolq->server: {:.2f}s\nserver->rabbitmq: {:.2f}s\nhandle init: {:.2f}s".format(
            receive["user_id"],
            receive["consumer_time"] - receive["time"],
            receive["pika_time"] - receive["consumer_time"],
            time.time() - receive["pika_time"],
        )
    else:
        msg += "[CQ:at,qq={}] {:.2f}s".format(
            receive["user_id"], time.time() - receive["time"]
        )
    msg = msg.strip()
    send_message(bot, receive["message_type"], discuss_id or group_id or user_id, msg,
                 post_type=receive.get("reply_api_type", "websocket"))


def handle_normal_command(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    # 合并ff14命令
    handlers.commands.update(handlers.ff14_commands)
    command_keys = sorted(handlers.commands.keys(), key=lambda x: -len(x))
    already_reply = False
    for command_key in command_keys:
        if receive["message"].find(command_key) == 0:
            handle_method = getattr(handlers, "QQCommand_{}".format(command_key.replace("/", "", 1)), )
            action_list = handle_method(receive=receive, global_config=config, bot=bot)
            already_reply = True
            for action in action_list:
                call_api(
                    bot,
                    action["action"],
                    action["params"],
                    echo=action["echo"],
                    post_type=receive.get("reply_api_type", "websocket")
                )
            break

    return already_reply


def handle_group_command(receive, bot):
    group_id = receive["group_id"]

    (group, group_created) = QQGroup.objects.get_or_create(group_id=group_id)
    member_list = json.loads(group.member_list)

    # get sender's user_info
    user_info = (receive["sender"] if "sender" in receive.keys() else None)
    user_info = (user_info if (user_info and ("role" in user_info.keys())) else None)

    group_command_keys = sorted(
        handlers.group_commands.keys(), key=lambda x: -len(x)
    )
    already_reply = False
    for command_key in group_command_keys:
        if receive["message"].find(command_key) == 0:
            if not group.registered and command_key != "/group":
                msg = "本群%s未在数据库注册，请群主使用/register_group命令注册" % (
                    group_id
                )
                send_message(bot, "group", group_id, msg)
                break
            else:
                handle_method = getattr(
                    handlers,
                    "QQGroupCommand_{}".format(
                        command_key.replace("/", "", 1)
                    ),
                )
                action_list = handle_method(
                    receive=receive,
                    global_config=config,
                    bot=bot,
                    user_info=user_info,
                    member_list=member_list,
                    group=group,
                    commands=handlers.commands,
                    group_commands=handlers.group_commands,
                    alter_commands=handlers.alter_commands,
                )
                for action in action_list:
                    call_api(
                        bot,
                        action["action"],
                        action["params"],
                        echo=action["echo"],
                        post_type=receive.get("reply_api_type", "websocket")
                    )
                    already_reply = True
                if already_reply:
                    break


def handle_chat(receive):
    bot = QQBot.objects.get(user_id=receive["self_id"])
    (group, group_created) = QQGroup.objects.get_or_create(group_id=receive["group_id"])

    # get sender's user_info
    user_info = (receive["sender"] if "sender" in receive.keys() else None)
    user_info = (user_info if (user_info and ("role" in user_info.keys())) else None)

    action_list = handlers.QQGroupChat(
        receive=receive,
        bot=bot,
        user_info=user_info,
        group=group,
        commands=handlers.commands,
        alter_commands=handlers.alter_commands,
    )
    for action in action_list:
        call_api(
            bot,
            action["action"],
            action["params"],
            echo=action["echo"],
            post_type=receive.get("reply_api_type", "websocket")
        )


def handle_qq_request(receive, bot):
    pass
    # CONFIG_GROUP_ID = config["CONFIG_GROUP_ID"]
    # if receive["request_type"] == "friend":  # Add Friend
    #     flag = receive["flag"]
    #     if bot.auto_accept_friend:
    #         reply_data = {"flag": flag, "approve": True}
    #         call_api(bot, "set_friend_add_request", reply_data,
    #                  post_type=receive.get("reply_api_type", "websocket"))
    # if (
    #         receive["request_type"] == "group"
    #         and receive["sub_type"] == "invite"
    # ):  # Invite Group
    #     flag = receive["flag"]
    #     if bot.auto_accept_invite:
    #         reply_data = {
    #             "flag": flag,
    #             "sub_type": "invite",
    #             "approve": True,
    #         }
    #         call_api(bot, "set_group_add_request", reply_data,
    #                  post_type=receive.get("reply_api_type", "websocket"))
    # if (
    #         receive["request_type"] == "group"
    #         and receive["sub_type"] == "add"
    #         and str(receive["group_id"]) == CONFIG_GROUP_ID
    # ):  # Add Group
    #     flag = receive["flag"]
    #     user_id = receive["user_id"]
    #     qs = QQBot.objects.filter(owner_id=user_id)
    #     if qs.count() > 0:
    #         reply_data = {"flag": flag, "sub_type": "add", "approve": True}
    #         call_api(bot, "set_group_add_request", reply_data,
    #                  post_type=receive.get("reply_api_type", "websocket"))
    #         reply_data = {
    #             "group_id": CONFIG_GROUP_ID,
    #             "user_id": user_id,
    #             "special_title": "饲养员",
    #         }
    #         call_api(bot, "set_group_special_title", reply_data,
    #                  post_type=receive.get("reply_api_type", "websocket"))


def handle_qq_event(receive, bot):
    pass
    # if receive["event"] == "group_increase":
    #     group_id = receive["group_id"]
    #     user_id = receive["user_id"]
    #     try:
    #         group = QQGroup.objects.get(group_id=group_id)
    #         msg = group.welcome_msg.strip()
    #         if msg != "":
    #             msg = "[CQ:at,qq=%s]" % user_id + msg
    #             send_message(bot, "group", group_id, msg,
    #                          post_type=receive.get("reply_api_type", "websocket"))
    #     except Exception as e:
    #         traceback.print_exc()


def call_api(bot, action, params, echo=None, **kwargs):
    # print("calling api:{} {}\n============================".format(json.dumps(action), json.dumps(params)))
    if "async" not in action and not echo:
        action = action + "_async"
    if "send_" in action and "_msg" in action:
        params["message"] = handle_message(bot, params["message"])
    jdata = {"action": action, "params": params}
    if echo:
        jdata["echo"] = echo
    post_type = kwargs.get("post_type", "websocket")
    if post_type == "websocket":
        async_to_sync(channel_layer.send)(
            bot.api_channel_name, {"type": "send.event", "text": json.dumps(jdata)}
        )
    elif post_type == "http":
        url = os.path.join(bot.api_post_url, "{}?access_token={}".format(action, bot.access_token))
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url=url, headers=headers, data=json.dumps(params))
        if r.status_code != 200:
            print("HTTP Callback failed:")
            print(r.text)


def send_message(bot, private_group, uid, message, **kwargs):
    if private_group == "group":
        call_api(bot, "send_group_msg", {"group_id": uid, "message": message}, **kwargs)
    if private_group == "discuss":
        call_api(bot, "send_discuss_msg", {"discuss_id": uid, "message": message}, **kwargs)
    if private_group == "private":
        call_api(bot, "send_private_msg", {"user_id": uid, "message": message}, **kwargs)


def update_group_member_list(bot, group_id, **kwargs):
    call_api(
        bot,
        "get_group_member_list",
        {"group_id": group_id},
        "get_group_member_list:%s" % group_id,
        **kwargs,
    )


def handle_message(bot, message):
    new_message = message
    if isinstance(message, list):
        new_message = []
        for idx, msg in enumerate(message):
            if msg["type"] == "share" and bot.share_banned:
                share_data = msg["data"]
                new_message.append(
                    {
                        "type": "image",
                        "data": {
                            "file": share_data["image"],
                            "url": share_data["image"],
                        },
                    }
                )
                new_message.append(
                    {
                        "type": "text",
                        "data": {
                            "text": "{}\n{}\n{}".format(
                                share_data["title"],
                                share_data["content"],
                                share_data["url"],
                            )
                        },
                    }
                )
            else:
                new_message.append(msg)
    return new_message
