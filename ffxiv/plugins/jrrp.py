from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import random
import none
import re

bot = none.get_bot()
temp = ""
i = 0


@on_command('roll', only_to_me=False, permission=permission.GROUP)
async def jrrp(session: CommandSession):
    msg = session.ctx
    text_report = await get_jrrp(msg)
    await session.send(text_report)


async def get_jrrp(msg) -> dict:
    rd = str(random.randint(1, 99))
    QQ = msg['user_id']
    mmg = MessageSegment.at(QQ)
    mmg1 = MessageSegment.text('您的roll点是：')
    mmg = mmg+mmg1+rd
    return mmg


@bot.on_message
async def f(ctx):
    global temp
    global i
    x = str(ctx['message'])+str(ctx['group_id'])
    QQ = str(ctx['user_id'])
    if 'group_id' in ctx:
        QG = str(ctx['group_id'])
    else:
        QG = 'NULL'
    if "/roll" not in x and "/luck" not in x and "/sleep" not in x and "/艾欧泽亚时间" not in x:
        if x == temp:
            e = random.randint(0, 2)
            if e == 1:
                if i < 999:
                    if QG == 'NULL':
                        await bot.send_private_msg(user_id=QQ, message=ctx['message'])
                        i = 999
                    else:
                        await bot.send_group_msg(group_id=QG, message=ctx['message'])
            i = i+1
        else:
            temp = x
            i = 0
