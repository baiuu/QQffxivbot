from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot
import pymysql
from os import path
import os
import requests


@on_command('ffxivitem', aliases=('道具', '查询道具', '查道具'), only_to_me=False)
async def ffxivitem(session: CommandSession):
    # 从 Session 对象中获取城市名称（city），如果当前不存在，则询问用户
    item = session.get_optional('item', default='NULL')
    if item == 'NULL':
        await session.send('请输入道具名')
    else:
        weather_report = await get_ffxivitem(item)
        await session.send(weather_report)


@ffxivitem.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['item'] = stripped_arg


async def get_ffxivitem(item: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    item_list = item.split()
    if len(item_list) > 1:
        if item_list[1] == "中文" or item_list[1] == "Cn":
            lang = "Name_cn"
        elif item_list[1] == "English" or item_list[0] == "En":
            lang = "Name_en"
            temp = ''
            if len(item_list) > 2:
                for i in range(len(item_list)):
                    if i > 0:
                        temp = f"{temp}{item_list[i]} "
                if " hq" in temp or " HQ" in temp:
                    item_list[1] = temp[:-4]
                    item_list[2] = "HQ"
                else:
                    item_list[1] = temp[:-1]
        elif item_list[0] == "日文" or item_list[0] == "Ja":
            lang = "Name_ja"
        else:
            lang = 'Null'
        db = pymysql.connect("localhost", "baiuu", "clml159", "ffxivdb_cn")
        cursor = db.cursor()
        sql = f"SELECT ItemID,{lang} FROM itemlist WHERE INSTR( {lang}, '{item_list[1]}' )"
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
        except:
            # 如果发生错误则回滚
            db.rollback()
        # 关闭数据库连接
        db.close()
        sid = 'null'
        item = ''
        for i in range(len(res)):
            if res[i][1] == item_list[1]:
                sid = i
                break
            else:
                if len(res) < 6:
                    if lang == "Name_cn":
                        temp = f"/道具 中文 {res[i][1]}\r\n"
                    elif lang == "Name_ja":
                        temp = f"/ffxivitem 日文 {res[i][1]}\r\n"
                    else:
                        temp = f"/ffxivitem English {res[i][1]}\r\n"
                    item += temp
                sid = 'null'
        if sid != 'null':
            name = res[sid][1]
            itemid = res[sid][0]
            if len(item_list) > 2:
                if item_list[2] == 'HQ' or item_list[2] == 'hq':
                    itemid = str(itemid)+'HQ'
            msg = await msgimg(itemid, name, lang, res[sid][0])
            return f'{msg}'
        elif len(res) == 0:
            return f'查询目标不存在'
        elif len(res) > 5:
            return f'查询结果过多请给予更精准的名字'
        else:
            mms = await msg1(item)
            return f'{mms}'
    else:
        return f'请输入 /道具 中文（English/日文）  道具名'


async def msg1(item):
    mmg = MessageSegment.text(item.strip('\r\n'))
    mmg1 = MessageSegment.text("查询到以下结果：\r\n")
    mms = mmg1 + mmg
    return mms


async def msgimg(itemid, name, lang, id):
    q = path.dirname(__file__).replace('\\', '/')
    d = f"file:///{q}"
    test = f"{q}/jpg/item/{itemid}.jpg"
    result = path.exists(test)
    if 'HQ' in name:
        if result == True:
            image = f"{d}/jpg/item/{itemid}.jpg"
        else:
            image = f"{d}/jpg/item/{itemid[:-2]}.jpg"
    else:
        image = f"{d}/jpg/item/{itemid}.jpg"
    mmg = MessageSegment.image(image)
    if lang == "Name_cn":
        urll = f'http://suo.im/api.php?url=https://ff14.huijiwiki.com/wiki/物品:{name}'
    elif lang == "Name_en":
        urll = f'http://suo.im/api.php?url=http://xivdb.com/item/{id}/'
    elif lang == "Name_ja":
        urll = f'http://suo.im/api.php?url=http://ja.xivdb.com/item/{id}/'
    response = requests.get(urll)
    mmg1 = MessageSegment.text(f"\r\n{response.text}")
    mms = mmg + mmg1
    return mms
