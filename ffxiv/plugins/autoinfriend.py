from none import on_request, RequestSession


# 将函数注册为好友请求处理器
@on_request('friend')
async def _(session: RequestSession):
    # 判断验证信息是否符合要求
    if session.ctx['comment'] == 'FF14' or session.ctx['comment'] == '最终幻想14' or session.ctx['comment'] == '咩咩':
        # 验证信息正确，同意入群
        await session.approve()
        return
    # 验证信息错误，拒绝入群
    await session.reject('请输入暗号')
