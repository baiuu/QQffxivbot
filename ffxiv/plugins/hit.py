from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('hit', aliases=('暴击', '查暴击'), only_to_me=False, permission=permission.GROUP)
async def hit(session: CommandSession):
    hit = session.get('hit')
    if hit == '':
        await session.send('请输入 /暴击 暴击数值')
    elif hit.isdigit():
        if int(hit) > 364:
            if int(hit) > 5000:
                await session.send('您暴击要上天啊')
            else:
                text_report = await get_hit(hit)
                await session.send(text_report)
        else:
            await session.send('请输入大于初始暴击的数值')
    else:
        await session.send('请输入 /暴击 暴击数值(数字)')


@hit.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['hit'] = stripped_arg


async def get_hit(hit: str) -> str:
    uphit = int(hit)-364
    LevelMod = 2170
    hitd = ((200*uphit/LevelMod)+1400)/10
    hitl = ((200*uphit/LevelMod)+50)/10
    hitd = round(hitd, 2)
    hitl = round(hitl, 2)
    res = f"{hit} 暴击的暴击伤害是 {hitd}% 暴击率是{hitl}%。"
    return res
