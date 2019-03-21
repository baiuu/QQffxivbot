from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('logs', aliases=('logs查询', 'logs警察'), only_to_me=False, permission=permission.GROUP)
async def logs(session: CommandSession):
    text = session.get('text')
    msg = session.ctx
    if text == '':
        await session.send('请正确输入 /进度 游戏版本 服务器 玩家ID （只支持查询3.0以后的版本）')
    else:
        text_report = await get_logs(text)
        await session.send(text_report)


@logs.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['text'] = stripped_arg


async def get_logs(text: str) -> str:
    text_list = text.split()
    if len(text_list) == 3:
        url1 = f"https://cn.fflogs.com/v1/zones?api_key=8f28c7586ea5c07c5b4a9f9a49c57309"
        url2 = f"https://cn.fflogs.com/v1/classes?api_key=8f28c7586ea5c07c5b4a9f9a49c57309"
        url3 = f"https://cn.fflogs.com/v1/rankings/character/{name}/{server}/CN?zone=25&metric=dps&api_key=8f28c7586ea5c07c5b4a9f9a49c57309"
        url4 = f"https://cn.fflogs.com/v1/rankings/encounter/{boss}?metric=dps&class={job}&spec=1&region=CN&page=1&api_key=8f28c7586ea5c07c5b4a9f9a49c57309"
        if text_list[0] == "3.0" or text_list[0] == "苍穹" or text_list[0] == "3":
            response1 = requests.get(url1)
            re1 = json.loads(response1.text)
            response2 = requests.get(url2)
            re2 = json.loads(response2.text)
            response3 = requests.get(url3)
            re3 = json.loads(response3.text)
            le3 = await mesg3(text_list, re1, re2, re3)
            return le3
        elif text_list[0] == "4.0" or text_list[0] == "红莲" or text_list[0] == "4":
            response4 = requests.get(url4)
            re4 = json.loads(response4.text)
            response5 = requests.get(url5)
            re5 = json.loads(response5.text)
            response6 = requests.get(url6)
            re6 = json.loads(response6.text)
            le4 = await mesg4(text_list, re4, re5, re6)
            return le4
        else:
            return "请正确输入 版本号 例如：3.0 4.0 苍穹 红莲"
    else:
        return "请正确输入 /进度 游戏版本 服务器 玩家ID （只支持查询3.0以后的版本）"


async def mesg3(text_list, re1, re2, re3):
