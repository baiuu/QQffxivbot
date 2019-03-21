from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import none
import re

bot = none.get_bot()


@on_command('wake', only_to_me=False, permission=permission.GROUP)
async def wake(session: CommandSession):
    msg = session.ctx
    msgx = await go_sleeo(msg)
    await session.send(msgx)


async def go_sleeo(msg) -> dict:
    res = r'(?<=\[CQ\:at\,qq=).*?(?=\])'
    pattern = re.compile(res)
    QQ = str(msg['message'])
    rex = re.search(pattern, QQ)
    if rex:
        QQ = rex.group()
    QG = msg['group_id']
    await bot.set_group_ban_async(group_id=QG, user_id=QQ, duration=0)
    mmg = MessageSegment.at(msg['user_id'])
    mmg1 = MessageSegment.text("已唤醒")
    mmg2 = MessageSegment.at(QQ)
    mmg = mmg+mmg1+mmg2
    return mmg
