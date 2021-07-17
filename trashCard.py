
import time
from typing import Optional

from peewee import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from drawWasteCertificate import drawCard

db = SqliteDatabase('CardData.db')


class BModel(Model):
    class Meta:
        database = db


class Card(BModel):
    id = AutoField()
    qqid = CharField()
    qqnick = CharField()
    groupname = CharField()
    time = CharField()

    class Meta:
        table_name = 'card'


db.create_tables([Card], safe=True)


class DrawCard(BaseModel):
    qqid: int
    qqnick: str
    groupname: str


class Response(BaseModel):
    code: int = 200
    msg: str
    id: Optional[str] = None
    time: Optional[str] = None
    pic: Optional[str] = None


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


RUNING = 0


@app.post("/getCard", response_model=Response)
async def drawPic(draw: DrawCard,):
    # return
    global RUNING
    ft = time.time()

    qqid = str(draw.qqid)
    qqnick = draw.qqnick
    groupname = draw.groupname
    timeStr = time.strftime("%Y-%m-%d\n%H:%M:%S", time.localtime())

    data = Card.select().where(Card.qqid == qqid)
    if data.exists():
        id = id = "%012d" % data[0].id
        return Response(code=1001, msg="该QQ号已存在一个证书", id=id, pic=f"http://trash.a60.one:88/{id}.png")
    else:
        if RUNING > 2:
            return Response(code=1002, msg="API繁忙，请稍后")

        else:
            RUNING += 1
            data = Card(qqid=qqid,
                        qqnick=qqnick,
                        groupname=groupname,
                        time=timeStr)
            data.save()
            id = "%012d" % data.id
            await drawCard(qqid, qqnick, groupname, id, timeStr)
            RUNING -= 1
            tt = time.time()
            times = tt - ft
            print(f"成功制作id为{id}的证书")
            return Response(code=200, msg="制图完成", id=id, time=times, pic=f"http://trash.a60.one:88/{id}.png")
