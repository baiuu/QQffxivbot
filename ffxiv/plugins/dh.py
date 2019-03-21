from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('dh', aliases=('直击', '查直击'), only_to_me=False, permission=permission.GROUP)
async def dh(session: CommandSession):
    dh = session.get('dh')
    if dh == '':
        await session.send('请输入 /直击 直击数值')
    elif dh.isdigit():
        if int(dh) > 364:
            if int(dh) > 5000:
                await session.send('您直击要上天啊')
            else:
                text_report = await get_dh(dh)
                await session.send(text_report)
        else:
            await session.send('请输入大于初始直击的数值')
    else:
        await session.send('请输入 /直击 直击数值(数字)')


@dh.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['dh'] = stripped_arg


async def get_dh(dh: str) -> str:
    updh = int(dh)-364
    LevelMod = 2170
    dhl = (550*updh/LevelMod)/10
    dhl = round(dhl, 2)
    res = f"{dh} 直击率是{dhl}%。"
    return res
