from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import random
import none
import time
import datetime

bot = none.get_bot()


@on_command('luck', only_to_me=False, permission=permission.GROUP)
async def luck(session: CommandSession):
    msg = session.ctx
    msgx = await go_luck(msg)
    await session.send(msgx)


async def go_luck(msg) -> dict:
    QQ = msg['user_id']
    t = time.time()
    ltime = time.localtime(int(t))
    yy = time.strftime("%Y", ltime)
    mm = time.strftime("%m", ltime)
    dd = time.strftime("%d", ltime)
    dateT = datetime.datetime(int(yy), int(mm), int(dd), 0, 0, 0)
    timestamp = time.mktime(dateT.timetuple())
    x = str(int(timestamp)+int(QQ*int(dd))+int(QQ/int(mm)))
    x = x[:-2]
    x = int(x[-2:])
    c = ""
    for i in range(x):
        c += "|"
    mmg = MessageSegment.at(QQ)
    mmg1 = MessageSegment.text(f"今日运势：{str(x)}% {c}")
    mmg = mmg+mmg1
    return mmg
