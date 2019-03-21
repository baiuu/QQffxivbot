from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('det', aliases=('信念', '查信念'), only_to_me=False, permission=permission.GROUP)
async def det(session: CommandSession):
    det = session.get('det')
    if det == '':
        await session.send('请输入 /信念 信念数值')
    elif det.isdigit():
        if int(det) > 364:
            if int(det) > 5000:
                await session.send('您信念要上天啊')
            else:
                text_report = await get_det(det)
                await session.send(text_report)
        else:
            await session.send('请输入大于初始信念的数值')
    else:
        await session.send('请输入 /信念 信念数值(数字)')


@det.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['det'] = stripped_arg


async def get_det(det: str) -> str:
    updet = int(det)-364
    LevelMod = 2170
    detl = 1 + ((130*updet/LevelMod)/10)
    detl = round(detl, 2)
    res = f"{det} 信念收益是{detl}%。"
    return res
