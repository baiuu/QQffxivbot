from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import pymysql
import re
import json
import os
import demjson
import none
from os import path

bot = none.get_bot()


@on_command('forget', only_to_me=False, permission=permission.GROUP)
async def forget(session: CommandSession):
    text = session.get('text')
    msg = session.ctx
    if text == '':
        await session.send('请输入 /forget 关键词')
    else:
        text_report = await fg_text(msg, text)
        await session.send(text_report)


@forget.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['text'] = stripped_arg


async def fg_text(msg, text: str) -> dict:
    if 'group_id' in msg:
        QG = msg['group_id']
    else:
        QG = 'NULL'
    db = pymysql.connect("localhost", "baiuu", "clml159", "teach")
    cursor = db.cursor()
    sql = "DELETE FROM teach WHERE teach='" + \
        text + "' AND QG='" + str(QG) + "'"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    db.close()
    return f'{text} 已忘记'
