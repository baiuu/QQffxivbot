from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import pymysql
import re
import json
import os
import demjson
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('teach', only_to_me=False, permission=permission.GROUP)
async def teach(session: CommandSession):
    text = session.get('text')
    msg = session.ctx
    if text == '':
        await session.send('请输入 /teach 关键词 说什么')
    else:
        text_report = await get_text(msg, text)
        await session.send(text_report)


@teach.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['text'] = stripped_arg


async def get_text(msg, text: str) -> dict:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    if 'group_id' in msg:
        QG = msg['group_id']
    else:
        QG = 'NULL'
    text_list = text.split()
    db = pymysql.connect("localhost", "baiuu", "clml159", "teach")
    cursor = db.cursor()
    sql = "SELECT * FROM teach WHERE teach='" + \
        text_list[0] + "' AND QG='" + str(QG) + "'"
    try:
        cursor.execute(sql)
        j = cursor.fetchone()
    except:
        # 如果发生错误则回滚
        db.rollback()
    if str(j) == "None":
        x = msg['message']
        res = str('(?<=teach).*')
        pattern = re.compile(res)
        temp = str(msg['message'][0]['data']['text'])
        rex = re.search(pattern, temp)
        if rex:
            temp = rex.group()
        msg['message'][0]['data']['text'] = temp
        relust = await mesg(bot, msg)
        d = path.dirname(__file__)
        jsonnew = d+"\\json"
        isExists = os.path.exists(jsonnew)
        if not isExists:
            os.makedirs(jsonnew)
        res = str('(?<='+text_list[0]+' ).*')
        pattern = re.compile(res)
        temp = str(x[0]['data']['text'])
        rex = re.search(pattern, temp)
        if rex:
            temp = rex.group()
        x[0]['data']['text'] = temp
        j = json.dumps(x)
        json_file = jsonnew+"\\"+str(QG)+"_"+text_list[0]+".json"
        f = open(json_file.replace('\\', '/'), 'w+')
        f.write(j)
        f.close()
        t = "('"+str(QG)+"_"+text_list[0]+".json','" + \
            str(QG) + "','" + text_list[0] + "')"
        sql = "INSERT INTO teach (filepath,QG,teach) VALUES " + t
        # sql = "SELECT * FROM teach WHERE teach='bat'"
        try:
            # 执行sql语句
            cursor.execute(sql)
            # j_o = cursor.fetchone()
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
        # 关闭数据库连接
        db.close()
        # o = demjson.decode_file(j_o[1])
        if len(x) > 1:
            return relust
        else:
            if len(text_list) > 1:
                return relust
            else:
                return f'请输入 /teach 关键词 说什么'
    else:
        return f'该关键词已存在'


async def mesg(bot, ctx):
    test = ctx['message']
    QQ = ctx['user_id']
    mmg = MessageSegment.at(QQ)
    mmg1 = MessageSegment.text('您教的我学会了是：')
    mmg = mmg + mmg1 + test
    return mmg


@bot.on_message
async def f(ctx):
    myqq = '[CQ:at,qq=1792174971] '
    msg = str(ctx['message'])
    if myqq in msg:
        db = pymysql.connect("localhost", "baiuu", "clml159", "teach")
        cursor = db.cursor()
        msg = msg.replace(myqq, '')
        QQ = str(ctx['user_id'])
        if 'group_id' in ctx:
            QG = str(ctx['group_id'])
        else:
            QG = 'NULL'
        sql = "SELECT * FROM teach WHERE teach='" + \
            msg+"' AND QG='" + str(QG) + "'"
        try:
            cursor.execute(sql)
            j_o = cursor.fetchone()
        except:
            # 如果发生错误则回滚
            db.rollback()
        # 关闭数据库连接
        db.close()
        if str(j_o) == "None":
            if QG == 'NULL':
                await bot.send_private_msg(user_id=QQ, message=msg+'该词条不存在')
            else:
                await bot.send_group_msg(group_id=QG, message=msg+'该词条不存在')
        else:
            d = path.dirname(__file__)
            jsonnew = d+"\\json"
            json_file = jsonnew+"\\"+j_o[1]
            o = demjson.decode_file(json_file.replace('\\', '/'))
            if QG == 'NULL':
                await bot.send_private_msg(user_id=QQ, message=o)
            else:
                await bot.send_group_msg(group_id=QG, message=o)
