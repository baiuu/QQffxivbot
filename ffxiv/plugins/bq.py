from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('bq', aliases=('不屈', '坚毅'), only_to_me=False, permission=permission.GROUP)
async def bq(session: CommandSession):
    bq = session.get('bq')
    if bq == '':
        await session.send('请输入 /不屈 不屈数值')
    elif bq.isdigit():
        if int(bq) > 364:
            if int(bq) > 5000:
                await session.send('您不屈要上天啊')
            else:
                text_report = await get_bq(bq)
                await session.send(text_report)
        else:
            await session.send('请输入 /不屈 不屈数值')
    else:
        await session.send('请输入 /不屈 不屈数值(数字)')


@bq.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['bq'] = stripped_arg


async def get_bq(bq: str) -> str:
    upbq = int(bq)-364
    LevelMod = 2170
    bql = (100*upbq/LevelMod)/10
    bql = round(bql, 2)
    res = f"{bq} 的不屈减伤收益是{bql}%。"
    return res
