from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('fy', aliases=('防御', '防御力'), only_to_me=False, permission=permission.GROUP)
async def fy(session: CommandSession):
    fy = session.get('fy')
    if fy == '':
        await sefyion.send('请输入 /防御 防御数值')
    elif fy.isdigit():
        if int(fy) > 364:
            if int(fy) > 20000:
                await session.send('您防御要上天啊')
            else:
                text_report = await get_fy(fy)
                await session.send(text_report)
        else:
            await session.send('请输入 /防御 防御数值')
    else:
        await session.send('请输入 /防御 防御数值(数字)')


@fy.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['fy'] = stripped_arg


async def get_fy(fy: str) -> str:
    LevelMod = 2170
    fyl = (15004*int(fy)/LevelMod)/1000
    fyl = round(fyl, 2)
    res = f"{fy} 的防御力减伤是{fyl}%。"
    return res
