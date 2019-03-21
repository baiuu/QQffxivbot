from none import on_request, RequestSession
import none

bot = none.get_bot()
# 将函数注册为好友请求处理器


@on_request('group')
async def _(session: RequestSession):
    # 判断验证信息是否符合要求
    if session.ctx['sub_type'] == 'invite':
        # 验证信息正确，同意入群
        await session.approve()
        await session.send('大家好我是叶小妖妖，请多关照~')
        return
    elif session.ctx['sub_type'] == 'add':
        return
    else:
        # 验证信息错误，拒绝入群
        await session.reject('请输入暗号')
