import requests
import os

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

async def drawCard(qqid, qqnick, groupname, id, time):

    # 打开模板图
    template = Image.open('template.png')
    # 设置字体
    msyhbdFont60 = ImageFont.truetype('msyhbd.ttc', 60)
    FZDBSJWFont34 = ImageFont.truetype('FZDBSJW.TTF', 34)
    JetBrainsMonoExtraBoldFont68 = ImageFont.truetype('JetBrainsMono-ExtraBold.ttf', 68)
    JetBrainsMonoExtraBoldFont64 = ImageFont.truetype('JetBrainsMono-ExtraBold.ttf', 64)
    JetBrainsMonoExtraBoldFont32 = ImageFont.truetype('JetBrainsMono-ExtraBold.ttf', 32)
    # 填入头像
    avatarUrl = f"https://q1.qlogo.cn/g?b=qq&nk={str(qqid)}&s=5"
    avatarContent = requests.get(avatarUrl).content
    avatarBio = BytesIO()
    avatarBio.write(avatarContent)
    avatarImg = Image.open(avatarBio)
    avatarImg180 = avatarImg.resize((180, 180))
    avatarBox = (80, 80)
    template.paste(avatarImg180, avatarBox)
    # 填入文字
    qqnick = await getCutStr(qqnick, 11)
    groupname = await getCutStr(groupname, 10)
    draw = ImageDraw.Draw(template)
    draw.text((180, 510), str(id), font=JetBrainsMonoExtraBoldFont68, fill='black')
    draw.text((332, 88), str(qqid), font=JetBrainsMonoExtraBoldFont64, fill='black')
    draw.text((330, 172), qqnick, font=msyhbdFont60, fill='black')
    draw.text((625, 318), groupname, font=FZDBSJWFont34, fill="black")
    draw.text((625, 368), time, font=JetBrainsMonoExtraBoldFont32, fill='black')
    template.save(f'/www/wwwroot/trash.a60.one/{id}.png')
    return

async def getCutStr(str, cut):
    si = 0
    i = 0
    for s in str:
        if '\u4e00' <= s <= '\u9fff':
            si += 1.5
        else:
            si += 1
        i += 1
        if si > cut:
            cutStr = str[:i] + '....'
            break
        else:
            cutStr = str
    
    return cutStr