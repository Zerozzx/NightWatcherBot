from enum import Enum
import re
from time import time
class MoodType(Enum):
    NORMAL = 0
    HAPPEY = 1
    ANGERY = 2
    SAD = 3


class XJ:
    '小姬机器人类，具有记录当前小姬心情状态、处于什么对话语境'
    __NoPrefixMode = False # 是否启用无前缀响应模式
    __MoodScore = 100 # 心情分数
    
    def __init__(self,mood:MoodType):
        self.mood = mood

# 处理信息
    def __HandleMessage(self,msgStr:str):
        if re.search(r'^(小姬*)([！!. \n]?$)',msgStr): # 如果单纯只是叫一下她
                return f"小姬收到！"
        
        if re.search(r'天气',msgStr):
            return f"我觉得应该是非常热的天气吧"
        elif re.search(r'玩',msgStr):
            return f"我觉得吧，Apex 最好玩"
        elif re.search(r'[(智障)(傻逼)(SB)(垃圾)(2B)]',msgStr):
            restr = re.search(r'[(智障)(傻逼)(SB)(垃圾)(2B)]',msgStr).group()
            return f"你才是{restr}!，*￥@￥%￥@%……*（&*&……*&xxx"
        else:
            return "阿巴阿巴阿巴..."

# 根据模式选择回复
    def FindReply(self,msgStr:str):
        if XJ.__NoPrefixMode == False :
            if re.search(r'^(小姬*)',msgStr):# 如果你在呼叫小姬
                return XJ.__HandleMessage(self,msgStr)
        else:
            return XJ.__HandleMessage(self,msgStr)