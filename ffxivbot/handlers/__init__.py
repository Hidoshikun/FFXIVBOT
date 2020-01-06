from .QQEventHandler import QQEventHandler
from .QQGroupEventHandler import QQGroupEventHandler

from .QQCommand_cat import QQCommand_cat
from .QQCommand_gakki import QQCommand_gakki
from .QQCommand_10 import QQCommand_10
from .QQCommand_bird import QQCommand_bird
from .QQCommand_comment import QQCommand_comment
from .QQCommand_search import QQCommand_search
from .QQCommand_about import QQCommand_about
from .QQCommand_donate import QQCommand_donate
from .QQCommand_anime import QQCommand_anime
from .QQCommand_gate import QQCommand_gate
from .QQCommand_chp import QQCommand_chp
from .QQCommand_random import QQCommand_random
from .QQCommand_weather import QQCommand_weather
from .QQCommand_gif import QQCommand_gif
from .QQCommand_dps import QQCommand_dps
from .QQCommand_dice import QQCommand_dice
from .QQCommand_hso import QQCommand_hso
from .QQCommand_raid import QQCommand_raid
from .QQCommand_bot import QQCommand_bot
from .QQCommand_pixiv import QQCommand_pixiv
from .QQCommand_duilian import QQCommand_duilian
from .QQCommand_image import QQCommand_image
from .QQCommand_nuannuan import QQCommand_nuannuan
from .QQCommand_tex import QQCommand_tex
from .QQCommand_waifu import QQCommand_waifu
from .QQCommand_quest import QQCommand_quest
from .QQCommand_share import QQCommand_share
from .QQCommand_trash import QQCommand_trash
from .QQCommand_shorten import QQCommand_shorten
from .QQCommand_ifttt import QQCommand_ifttt
from .QQCommand_daishi import QQCommand_daishi
from .QQCommand_erciyuan import QQCommand_erciyuan
from .QQCommand_joke import QQCommand_joke
from .QQCommand_mingyan import QQCommand_mingyan
from .QQCommand_fsx import QQCommand_fsx
from .QQCommand_mxh import QQCommand_mxh
from .QQCommand_nmsl import QQCommand_nmsl
from .QQCommand_lyl import QQCommand_lyl
from .QQCommand_luck import QQCommand_luck
from .QQCommand_treasure import QQCommand_treasure
from .QQCommand_hh import QQCommand_hh
from .QQCommand_eat import QQCommand_eat

from .arknights.QQCommand_akhr import QQCommand_akhr

from .QQGroupCommand_group import QQGroupCommand_group
from .QQGroupCommand_welcome import QQGroupCommand_welcome
from .QQGroupCommand_custom_reply import QQGroupCommand_custom_reply
from .QQGroupCommand_repeat_ban import QQGroupCommand_repeat_ban
from .QQGroupCommand_repeat import QQGroupCommand_repeat
from .QQGroupCommand_left_reply import QQGroupCommand_left_reply
from .QQGroupCommand_ban import QQGroupCommand_ban
from .QQGroupCommand_revenge import QQGroupCommand_revenge
from .QQGroupCommand_vote import QQGroupCommand_vote
from .QQGroupCommand_weibo import QQGroupCommand_weibo
from .QQGroupCommand_live import QQGroupCommand_live
from .QQGroupCommand_lottery import QQGroupCommand_lottery
from .QQGroupCommand_command import QQGroupCommand_command
from .QQGroupCommand_hunt import QQGroupCommand_hunt

from .QQGroupChat import QQGroupChat

commands = {
    "/cat": "云吸猫",
    "/gakki": "云吸gakki",
    "/10": "云吸十元",
    "/bird": "云吸飞鸟",
    "/lyl": "云吸李依李",
    "/waifu": "云吸二次元老婆",
    "/about": "关于此项目",
    "/random": "掷骰子",
    "/anime": "以图搜番（\"/anime 图片\"）",
    "/gif": "生成沙雕图（\"/gif help\"）",
    "/pixiv": "Pixiv相关功能（\"/pixiv help\"）",
    "/duilian": "对联（\"/duilian 稻花香里说丰年\"）",
    "/gate": "挖宝选门（\"/gate 3\"）",
    "/chp": "彩虹屁",
    "/akhr": "罗德岛公开招募",
    "/hso": "好色哦",
    "/daishi": "查看带湿发言",
    "/erciyuan": "别骂了别骂了",
    "/trash": "你是什么垃圾？",
    "/joke": "讽刺笑话（\"/joke 996|强东|建设一流公司|程序员|公司\"）",
    "/mingyan": "随机返回二次元名言",
    "/mxh": "梅溪湖CP短打生成器（\"/mxh 海德林 佐迪亚克\"）",
    "/fsx": "副属性收益计算",
    "/nmsl": "嘴臭生成器",
    "/luck": "浅草寺求签",
    "/eat": "吃啥",
}

ff14_commands = {
    "/gate": "挖宝选门（\"/gate 3\"）",
    "/search": "查询物品(\"/search 神龙\")",
    "/treasure": "宝图搜寻",
    "/weather": "天气信息（快捷命令\"/fog\",\"/heat_wave\",\"/thunder\",\"/kx\"）",
    "/dps": "DPS排名（\"/dps 8s 骑士\"）",
    "/raid": "零式英雄榜（\"/raid 蓝色裂痕 萌芽池\"）",
    "/quest": "任务查询(/quest 狂乱前奏)",
    "/nuannuan": "本周金蝶暖暖作业",
    "/fsx": "副属性收益计算",
    "/hh": "光之收藏家幻化查询",
}

group_commands = {
    "/group": "群相关功能控制",
    "/welcome": "设置欢迎语",
    "/custom_reply": "添加自定义命令",
    # "/repeat_ban": "复读姬口球系统",
    "/repeat": "开启复读姬系统",
    # "/left_reply": "聊天限额剩余情况",
    # "/ban": "投票禁言",
    # "/revenge": "复仇",
    "/vote": "投票系统",
    "/weibo": "微博订阅系统",
    "/live": "直播订阅系统",
    "/command": "群功能停用/启用",
    "/lottery": "抽奖",
    # "/hunt": "狩猎",
}

alter_commands = {
    "/pzz": "/weather 优雷卡常风之地 强风",
    "/blizzard": "/weather 优雷卡恒冰之地 暴雪",
    "/kx": "/weather 优雷卡恒冰之地 暴雪",
    "/fog": "/weather 优雷卡恒冰之地 薄雾",
    "/thunder": "/weather 优雷卡恒冰之地 打雷",
    "/heat_wave": "/weather 优雷卡恒冰之地 热风",
    "/register_group": "/group register",
    "/welcome_demo": "/welcome demo",
    "/set_welcome_msg": "/welcome set",
    "/add_custom_reply list": "/custom_reply list",
    "/add_custom_reply": "/custom_reply add",
    "/del_custom_reply": "/custom_reply del",
    "/set_repeat_ban": "/repeat_ban set",
    "/disable_repeat_ban": "/repeat_ban disable",
    "/set_left_reply_cnt": "/left_reply set",
    "/set_ban": "/ban set",
    "/revenge_confirm": "/revenge confirm",
    "/laji": "/trash",
    "/吃啥": "/eat",
}
