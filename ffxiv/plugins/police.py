from none import on_command, CommandSession, Message, message_preprocessor, MessageSegment, get_bot, permission
import json
import requests
import os
import none
from os import path
# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」

bot = none.get_bot()


@on_command('police', aliases=('进度', '进度警察'), only_to_me=False, permission=permission.GROUP)
async def police(session: CommandSession):
    text = session.get('text')
    msg = session.ctx
    if text == '':
        await session.send('请正确输入 /进度 游戏版本 服务器 玩家ID （只支持查询3.0以后的版本）')
    else:
        text_report = await get_police(text)
        await session.send(text_report)


@police.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    session.args['text'] = stripped_arg


async def get_police(text: str) -> str:
    text_list = text.split()
    if len(text_list) == 3:
        url1 = "http://act.ff.sdo.com/HeroList/Server/HreoList.ashx?"
        url2 = "http://act.ff.sdo.com/HeroList/Server/HreoList0712.ashx?"
        url3 = "http://act.ff.sdo.com/HeroList/Server/HreoList0220.ashx?"
        url4 = "http://act.ff.sdo.com/20171213HeroList/Server/HeroList171213.ashx?"
        url5 = "http://act.ff.sdo.com/20180525HeroList/Server/HeroList171213.ashx?"
        url6 = "http://act.ff.sdo.com/20180525HeroList/Server/HeroList190128.ashx?"
        if text_list[1] == "拉诺西亚"or text_list[1] == "拉诺":
            text_list[1] = "拉诺西亚"
            areid = 1
            groupid = 3
            cnareid = 1
            cngroupid = 3
        elif text_list[1] == "紫水栈桥" or text_list[1] == "紫水":
            text_list[1] = "紫水栈桥"
            areid = 1
            groupid = 4
            cnareid = 1
            cngroupid = 4
        elif text_list[1] == "幻影群岛" or text_list[1] == "幻影" or text_list[1] == "群岛":
            text_list[1] = "幻影群岛"
            areid = 1
            groupid = 5
            cnareid = 1
            cngroupid = 5
        elif text_list[1] == "摩杜纳":
            areid = 1
            groupid = 6
            cnareid = 1
            cngroupid = 6
        elif text_list[1] == "神意之地" or text_list[1] == "神意":
            text_list[1] = "神意之地"
            areid = 1
            groupid = 24
            cnareid = 1
            cngroupid = 24
        elif text_list[1] == "静语庄园" or text_list[1] == "静语":
            text_list[1] = "静语庄园"
            areid = 1
            groupid = 23
            cnareid = 1
            cngroupid = 23
        elif text_list[1] == "萌芽池":
            areid = 2
            groupid = 1
            cnareid = 1
            cngroupid = 25
        elif text_list[1] == "延夏":
            areid = 1
            groupid = 26
            cnareid = 1
            cngroupid = 26
        elif text_list[1] == "红玉海":
            areid = 1
            groupid = 27
            cnareid = 1
            cngroupid = 27
        elif text_list[1] == "潮风亭":
            areid = 1
            groupid = 61
            cnareid = 1
            cngroupid = 61
        elif text_list[1] == "神拳痕":
            areid = 1
            groupid = 62
            cnareid = 1
            cngroupid = 62
        elif text_list[1] == "白银乡":
            areid = 1
            groupid = 63
            cnareid = 1
            cngroupid = 63
        elif text_list[1] == "白金幻象" or text_list[1] == "白金":
            text_list[1] = "白金幻象"
            areid = 1
            groupid = 64
            cnareid = 1
            cngroupid = 64
        url1 = f"{url1}Method=queryhreodata&Name={text_list[2]}&AreaId={areid}&GroupId={groupid}"
        url2 = f"{url2}Method=queryhreodata&Name={text_list[2]}&AreaId={areid}&GroupId={groupid}"
        url3 = f"{url3}Method=queryhreodata&Name={text_list[2]}&AreaId={cnareid}&GroupId={cngroupid}"
        url4 = f"{url4}Method=queryhreodata&Name={text_list[2]}&AreaId={cnareid}&GroupId={cngroupid}"
        url5 = f"{url5}Method=queryhreodata&Name={text_list[2]}&AreaId={cnareid}&GroupId={cngroupid}"
        url6 = f"{url6}Method=queryhreodata&Name={text_list[2]}&Stage=1&AreaId={cnareid}&GroupId={cngroupid}"
        if text_list[0] == "3.0" or text_list[0] == "苍穹" or text_list[0] == "3":
            response1 = requests.get(url1)
            re1 = json.loads(response1.text)
            response2 = requests.get(url2)
            re2 = json.loads(response2.text)
            response3 = requests.get(url3)
            re3 = json.loads(response3.text)
            le3 = await mesg3(text_list, re1, re2, re3)
            return le3
        elif text_list[0] == "4.0" or text_list[0] == "红莲" or text_list[0] == "4":
            response4 = requests.get(url4)
            re4 = json.loads(response4.text)
            response5 = requests.get(url5)
            re5 = json.loads(response5.text)
            response6 = requests.get(url6)
            re6 = json.loads(response6.text)
            le4 = await mesg4(text_list, re4, re5, re6)
            return le4
        else:
            return "请正确输入 版本号 例如：3.0 4.0 苍穹 红莲"
    else:
        return "请正确输入 /进度 游戏版本 服务器 玩家ID （只支持查询3.0以后的版本）"


async def mesg3(text_list, re1, re2, re3):
    reday1 = {0: {""}}
    if re1['Attach']['Level1'] != "" and str(re1['Attach']['Level1']) != "None":
        reyy = re1['Attach']['Level1'][:4]
        remm = re1['Attach']['Level1'][4:6]
        redd = re1['Attach']['Level1'][6:]
        reday1[1] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式启动之章1"
    if re1['Attach']['Level2'] != "" and str(re1['Attach']['Level2']) != "None":
        reyy = re1['Attach']['Level2'][:4]
        remm = re1['Attach']['Level2'][4:6]
        redd = re1['Attach']['Level2'][6:]
        reday1[2] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式启动之章2"
    if re1['Attach']['Level3'] != "" and str(re1['Attach']['Level3']) != "None":
        reyy = re1['Attach']['Level3'][:4]
        remm = re1['Attach']['Level3'][4:6]
        redd = re1['Attach']['Level3'][6:]
        reday1[3] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式启动之章3"
    if re1['Attach']['Level4'] != "" and str(re1['Attach']['Level4']) != "None":
        reyy = re1['Attach']['Level4'][:4]
        remm = re1['Attach']['Level4'][4:6]
        redd = re1['Attach']['Level4'][6:]
        reday1[4] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式启动之章4"
    if (re1['Attach']['Level1'] == "" and re1['Attach']['Level2'] == "" and re1['Attach']['Level3'] == "" and re1['Attach']['Level4'] == "") or (str(re1['Attach']['Level1']) == "None" and str(re1['Attach']['Level2']) == "None" and str(re1['Attach']['Level3']) == "None" and str(re1['Attach']['Level4']) == "None"):
        reday1[1] = "该玩家未攻破任意亚历山大零式启动之章"
    reday2 = {0: {""}}
    if re2['Attach']['Level1'] != "" and str(re2['Attach']['Level1']) != "None":
        reyy = re2['Attach']['Level1'][:4]
        remm = re2['Attach']['Level1'][4:6]
        redd = re2['Attach']['Level1'][6:]
        reday2[1] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式律动之章1"
    if re2['Attach']['Level2'] != "" and str(re2['Attach']['Level2']) != "None":
        reyy = re2['Attach']['Level2'][:4]
        remm = re2['Attach']['Level2'][4:6]
        redd = re2['Attach']['Level2'][6:]
        reday2[2] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式律动之章2"
    if re2['Attach']['Level3'] != "" and str(re2['Attach']['Level3']) != "None":
        reyy = re2['Attach']['Level3'][:4]
        remm = re2['Attach']['Level3'][4:6]
        redd = re2['Attach']['Level3'][6:]
        reday2[3] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式律动之章3"
    if re2['Attach']['Level4'] != "" and str(re2['Attach']['Level4']) != "None":
        reyy = re2['Attach']['Level4'][:4]
        remm = re2['Attach']['Level4'][4:6]
        redd = re2['Attach']['Level4'][6:]
        reday2[4] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式律动之章4"
    if (re2['Attach']['Level1'] == "" and re2['Attach']['Level2'] == "" and re2['Attach']['Level3'] == "" and re2['Attach']['Level4'] == "") or (str(re2['Attach']['Level1']) == "None" and str(re2['Attach']['Level2']) == "None" and str(re2['Attach']['Level3']) == "None" and str(re2['Attach']['Level4']) == "None"):
        reday2[1] = "该玩家未攻破任意亚历山大零式律动之章"
    reday3 = {0: {""}}
    if re3['Attach']['Level1'] != "" and str(re3['Attach']['Level1']) != "None":
        reyy = re3['Attach']['Level1'][:4]
        remm = re3['Attach']['Level1'][4:6]
        redd = re3['Attach']['Level1'][6:]
        reday3[1] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式天动之章1"
    if re3['Attach']['Level2'] != "" and str(re3['Attach']['Level2']) != "None":
        reyy = re3['Attach']['Level2'][:4]
        remm = re3['Attach']['Level2'][4:6]
        redd = re3['Attach']['Level2'][6:]
        reday3[2] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式天动之章2"
    if re3['Attach']['Level3'] != "" and str(re3['Attach']['Level3']) != "None":
        reyy = re3['Attach']['Level3'][:4]
        remm = re3['Attach']['Level3'][4:6]
        redd = re3['Attach']['Level3'][6:]
        reday3[3] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式天动之章3"
    if re3['Attach']['Level4'] != "" and str(re3['Attach']['Level4']) != "None":
        reyy = re3['Attach']['Level4'][:4]
        remm = re3['Attach']['Level4'][4:6]
        redd = re3['Attach']['Level4'][6:]
        reday3[4] = f"{reyy}年{remm}月{redd}日 攻破了亚历山大零式天动之章4"
    if (re3['Attach']['Level1'] == "" and re3['Attach']['Level2'] == "" and re3['Attach']['Level3'] == "" and re3['Attach']['Level4'] == "") or (str(re3['Attach']['Level1']) == "None" and str(re3['Attach']['Level2']) == "None" and str(re3['Attach']['Level3']) == "None" and str(re3['Attach']['Level4']) == "None"):
        reday3[1] = "该玩家未攻破任意亚历山大零式天动之章"
    reslut1 = "亚历山大零式启动之章\r\n"
    for i in range(len(reday1)):
        if i > 0:
            reslut1 = f"{reslut1}{reday1[i]}\r\n"
    reslut1 += "=============================\r\n"
    reslut2 = "亚历山大零式律动之章\r\n"
    for i in range(len(reday2)):
        if i > 0:
            reslut2 = f"{reslut2}{reday2[i]}\r\n"
    reslut2 += "=============================\r\n"
    reslut3 = "亚历山大零式天动之章\r\n"
    for i in range(len(reday3)):
        if i > 0:
            reslut3 = f"{reslut3}{reday3[i]}\r\n"
    reslut3 += "=============================\r\n"
    res = f"{text_list[1]} 服的 {text_list[2]} 玩家进度：\r\n"
    reslut = str(res) + str(reslut1)+str(reslut2) + str(reslut3)
    return reslut


async def mesg4(text_list, re4, re5, re6):
    reday4 = {0: {""}}
    if re4['Attach']['Level1'] != "" and str(re4['Attach']['Level1']) != "None":
        reyy = re4['Attach']['Level1'][:4]
        remm = re4['Attach']['Level1'][4:6]
        redd = re4['Attach']['Level1'][6:]
        reday4[1] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 德尔塔幻境1"
    if re4['Attach']['Level2'] != ""and str(re4['Attach']['Level2']) != "None":
        reyy = re4['Attach']['Level2'][:4]
        remm = re4['Attach']['Level2'][4:6]
        redd = re4['Attach']['Level2'][6:]
        reday4[2] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 德尔塔幻境2"
    if re4['Attach']['Level3'] != ""and str(re4['Attach']['Level3']) != "None":
        reyy = re4['Attach']['Level3'][:4]
        remm = re4['Attach']['Level3'][4:6]
        redd = re4['Attach']['Level3'][6:]
        reday4[3] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 德尔塔幻境3"
    if re4['Attach']['Level4'] != ""and str(re4['Attach']['Level4']) != "None":
        reyy = re4['Attach']['Level4'][:4]
        remm = re4['Attach']['Level4'][4:6]
        redd = re4['Attach']['Level4'][6:]
        reday4[4] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 德尔塔幻境4"
    if (re4['Attach']['Level1'] == "" and re4['Attach']['Level2'] == "" and re4['Attach']['Level3'] == "" and re4['Attach']['Level4'] == "")or(str(re4['Attach']['Level1']) == "None"and str(re4['Attach']['Level2']) == "None" and str(re4['Attach']['Level4']) == "None"):
        reday4[1] = "该玩家未攻破任意欧米茄零式时空狭缝 德尔塔幻境"
    reday5 = {0: {""}}
    if re5['Attach']['Level1'] != "" and str(re5['Attach']['Level1']) != "None":
        reyy = re5['Attach']['Level1'][:4]
        remm = re5['Attach']['Level1'][4:6]
        redd = re5['Attach']['Level1'][6:]
        reday5[1] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 西格玛幻境1"
    if re5['Attach']['Level2'] != ""and str(re5['Attach']['Level2']) != "None":
        reyy = re5['Attach']['Level2'][:4]
        remm = re5['Attach']['Level2'][4:6]
        redd = re5['Attach']['Level2'][6:]
        reday5[2] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 西格玛幻境2"
    if re5['Attach']['Level3'] != ""and str(re5['Attach']['Level3']) != "None":
        reyy = re5['Attach']['Level3'][:4]
        remm = re5['Attach']['Level3'][4:6]
        redd = re5['Attach']['Level3'][6:]
        reday5[3] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 西格玛幻境3"
    if re5['Attach']['Level4'] != ""and str(re5['Attach']['Level4']) != "None":
        reyy = re5['Attach']['Level4'][:4]
        remm = re5['Attach']['Level4'][4:6]
        redd = re5['Attach']['Level4'][6:]
        reday5[4] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 西格玛幻境4"
    if (re5['Attach']['Level1'] == "" and re5['Attach']['Level2'] == "" and re5['Attach']['Level3'] == "" and re5['Attach']['Level4'] == "") or (str(re5['Attach']['Level1']) == "None" and str(re5['Attach']['Level2']) == "None" and str(re5['Attach']['Level3']) == "None" and str(re5['Attach']['Level4']) == "None"):
        reday5[1] = "该玩家未攻破任意欧米茄零式时空狭缝 西格玛幻境"
    reday6 = {0: {""}}
    if re6['Attach']['Level1'] != "" and str(re6['Attach']['Level1']) != "None":
        reyy = re6['Attach']['Level1'][:4]
        remm = re6['Attach']['Level1'][4:6]
        redd = re6['Attach']['Level1'][6:]
        reday6[1] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 阿尔法幻境1"
    if re6['Attach']['Level2'] != "" and str(re6['Attach']['Level2']) != "None":
        reyy = re6['Attach']['Level2'][:4]
        remm = re6['Attach']['Level2'][4:6]
        redd = re6['Attach']['Level2'][6:]
        reday6[2] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 阿尔法幻境2"
    if re6['Attach']['Level3'] != "" and str(re6['Attach']['Level3']) != "None":
        reyy = re6['Attach']['Level3'][:4]
        remm = re6['Attach']['Level3'][4:6]
        redd = re6['Attach']['Level3'][6:]
        reday6[3] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 阿尔法幻境3"
    if re6['Attach']['Level4'] != "" and str(re6['Attach']['Level4']) != "None":
        reyy = re6['Attach']['Level4'][:4]
        remm = re6['Attach']['Level4'][4:6]
        redd = re6['Attach']['Level4'][6:]
        reday6[4] = f"{reyy}年{remm}月{redd}日 攻破了欧米茄零式时空狭缝 阿尔法幻境4"
    if (re6['Attach']['Level1'] == "" and re6['Attach']['Level2'] == "" and re6['Attach']['Level3'] == "" and re6['Attach']['Level4'] == "") or (str(re6['Attach']['Level1']) == "None" and str(re6['Attach']['Level2']) == "None" and str(re6['Attach']['Level3']) == "None" and str(re6['Attach']['Level4']) == "None"):
        reday6[1] = "该玩家未攻破任意欧米茄零式时空狭缝 阿尔法幻境"
    reslut4 = "欧米茄零式时空狭缝 德尔塔幻境\r\n"
    for i in range(len(reday4)):
        if i > 0:
            reslut4 = f"{reslut4}{reday4[i]}\r\n"
    reslut4 += "=============================\r\n"
    reslut5 = "欧米茄零式时空狭缝 西格玛幻境\r\n"
    for i in range(len(reday5)):
        if i > 0:
            reslut5 = f"{reslut5}{reday5[i]}\r\n"
    reslut5 += "=============================\r\n"
    reslut6 = "欧米茄零式时空狭缝 阿尔法幻境\r\n"
    for i in range(len(reday6)):
        if i > 0:
            reslut6 = f"{reslut6}{reday6[i]}\r\n"
    reslut6 += "============================="
    res = f"{text_list[1]} 服的 {text_list[2]} 玩家进度：\r\n"
    reslut = str(res) + str(reslut4) + str(reslut5) + str(reslut6)
    return reslut
