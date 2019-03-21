from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('ss', aliases=('技速', '技能速度'), only_to_me=False, permission=permission.GROUP)
async def ss(session: CommandSession):
    ss = session.get('ss')
    if ss == '':
        await session.send('请输入 /技速 技速数值')
    elif ss.isdigit():
        if int(ss) > 364:
            if int(ss) > 5000:
                await session.send('您技能速度要上天啊')
            else:
                text_report = await get_ss(ss)
                await session.send(text_report)
        else:
            await session.send('请输入 /技速 技速数值')
    else:
        await session.send('请输入 /技速 技速数值(数字)')


@ss.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['ss'] = stripped_arg


async def get_ss(ss: str) -> str:
    upss = int(ss)-364
    LevelMod = 2170
    ssl = 1 + ((130*upss/LevelMod)/10)
    sscd = ((1-(130*upss/LevelMod)/1000) * 2.5)*(1-0)
    ssl = round(ssl, 2)
    sscd = round(sscd, 2)
    res = f"{ss} 的技能速度收益是{ssl}% GCD是{sscd}。"
    return res
