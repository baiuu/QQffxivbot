from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import random
import none
import time
import datetime


@on_command('ettime', aliases=('艾欧泽亚时间', 'ff14时间'), only_to_me=False, permission=permission.GROUP)
async def sleep(session: CommandSession):
    msgx = await get_ettime()
    await session.send(msgx)


async def get_ettime():
    locatime = time.time()
    ettime = round((locatime-1278950400)*144/7)
    year = int(ettime / 33177600)
    mon = int((ettime % 33177600 / 2764800)+1)
    day = int((ettime % 2764800 / 86400)+1)
    HH = int(ettime % 86400 / 3600)
    mm = int(ettime % 3600 / 60)
    ettime = time.localtime(ettime)
    ss = time.strftime("%S", ettime)
    return f"现在是艾欧泽亚时间：{year}-{mon}-{day} {HH}:{mm}:{ss}"
