from email.header import Header
from enum import Enum
import re,random,io
from time import time
from wget import GetImageURL
from khl.card import CardMessage, Card,Module,Element,Types,Struct
import requests
from khl import Bot,Message
CARDJSON = '''[
  {
    "type": "card",
    "theme": "secondary",
    "size": "lg",
    "modules": [
      {
        "type": "container",
        "elements": [
          {
            "type": "image",
            "src": "https://img.kaiheila.cn/assets/2021-01/7kr4FkWpLV0ku0ku.jpeg"
          }
        ]
      }
    ]
  }
]'''
class MoodType(Enum):
    NORMAL = 0
    HAPPEY = 1
    ANGERY = 2
    SAD = 3



class XJ:
    '小姬机器人类，具有记录当前小姬心情状态、处于什么对话语境'
    __NoPrefixMode = False # 是否启用无前缀响应模式
    __MoodScore = 100 # 心情分数
    
    def __init__(self,bot:Bot,mood:MoodType):
        self.mood = mood
        self.bot = bot

# 处理信息
    async def __HandleMessage(self,msg:Message):
        if re.search(r'^(小姬*)([！!. \n]?$)',msg.content): # 如果单纯只是叫一下她
            return f"小姬收到！"
        if re.search(r'天气',msg.content):
            return f"我觉得应该是非常热的天气吧"
        elif re.search(r'玩',msg.content):
            return f"我觉得吧，Apex 最好玩"
        elif re.search(r'[(智障)(傻逼)(SB)(垃圾)(2B)]',msg.content):
            restr = re.search(r'[(智障)(傻逼)(SB)(垃圾)(2B)]',msg.content).group()
            return f"你才是{restr}!，*￥@￥%￥@%……*（&*&……*&xxx"
        elif re.search(r'[(帮我搜)(搜索)]',msg.content):
            return f"自己搜！"
        elif re.search(r'[(虚幻文档)(虚幻引擎)(引擎文档)(UE文档)(UE5文档)]',msg.content):
            return "[虚幻文档](https://docs.unrealengine.com/zh-CN/index.html)"
        elif re.search(r'[(图片)]',msg.content):
            #await msg.reply(f"")
            keyword = re.search(r'(?<=[(:)(：)])[\S]*',msg.content).group()
            URLs = GetImageURL(keyword,1)
            K_URL = await self.url_to_asset(URLs[random.randint(1,len(URLs))])
            c1 = Card(Module.Header(f"{keyword}"), color='#5A3BD7')
            c1.append(Module.Container(Element.Image(src=K_URL)))
            cm = CardMessage()
            cm.append(c1)
            return cm
        else:
            return "阿巴阿巴阿巴..."

# 根据模式选择回复
    async def FindReply(self,msg:Message):
        if XJ.__NoPrefixMode == False :
            if re.search(r'^(小姬*)',msg.content):# 如果你在呼叫小姬
                return await XJ.__HandleMessage(self,msg)
        else:
            return await XJ.__HandleMessage(self,msg)

# 将外链图片，先用接口上传到 KOOK 图床，再获得 KOOK 图床的 URL 返回
    async def url_to_asset(self,pic_url):
        img_src = pic_url
        response = requests.get(img_src)
        img = io.BytesIO(response.content)
        asset_url = (await self.bot.create_asset(img))
        return asset_url