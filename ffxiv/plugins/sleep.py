from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import random
import none
import time
import datetime

bot = none.get_bot()


@on_command('sleep', only_to_me=False, permission=permission.GROUP)
async def sleep(session: CommandSession):
    msg = session.ctx
    msgx = await go_sleeo(msg)
    await session.send(msgx)


async def go_sleeo(msg) -> dict:
    rd = random.randint(18000, 36000)
    QQ = msg['user_id']
    QG = msg['group_id']
    msgtime = msg['time']
    timeget = time.localtime(msgtime)
    hh = time.strftime("%H", timeget)
    mm = time.strftime("%M", timeget)
    hh = str(int(hh)-1)
    if int(hh) < 21 and int(hh) > 10:
        mmg = MessageSegment.at(QQ)
        mmg1 = MessageSegment.text(f'才{hh}点{mm}分，睡什么睡起来嗨~')
        mmg = mmg1+mmg
    elif int(hh) > 3 and int(hh) < 12:
        rd = random.randint(25200, 43200)
        mmg = MessageSegment.at(QQ)
        mmg1 = MessageSegment.text(f'都{hh}点{mm}分了，你修仙啊~')
        mmg = mmg1+mmg
        await bot.set_group_ban_async(group_id=QG, user_id=QQ, duration=rd)
    else:
        await bot.set_group_ban_async(group_id=QG, user_id=QQ, duration=rd)
        mmg = MessageSegment.at(QQ)
        mmg1 = MessageSegment.text("睡眠模式已开启")
        mmg = mmg1+mmg
    return mmg
