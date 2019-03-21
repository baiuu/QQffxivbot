from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('ss1', aliases=('咏速', '咏唱速度','咏唱'), only_to_me=False, permission=permission.GROUP)
async def ss1(session: CommandSession):
    ss1 = session.get('ss1')
    if ss1 == '':
        await session.send('请输入 /咏速 咏速数值')
    elif ss1.isdigit():
        if int(ss1) > 364:
            text_report = await get_ss1(ss1)
            await session.send(text_report)
        else:
            await session.send('请输入 /咏速 咏速数值')
        if int(ss1) > 5000:
            await session.send('您咏唱速度要上天啊')
    else:
        await session.send('请输入 /咏速 咏速数值(数字)')


@ss1.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['ss1'] = stripped_arg


async def get_ss1(ss1: str) -> str:
    upss1 = int(ss1)-364
    LevelMod = 2170
    ss1l = 1 + ((130*upss1/LevelMod)/10)
    ss1cd = ((1-(130*upss1/LevelMod)/1000) * 2.5)*(1-0)
    ss1l = round(ss1l, 2)
    ss1cd = round(ss1cd, 2)
    res = f"{ss1} 的咏唱速度收益是{ss1l}% GCD是{ss1cd}。"
    return res
