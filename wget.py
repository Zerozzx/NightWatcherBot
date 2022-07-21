import requests
import re
import os
import random
from collections import Counter
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}

url = 'https://image.baidu.com/search/acjson?'

def GetImageFromBaidu(keyword:str,page:int,savePath:str):
    for pn in range(0,30*page,30):
        param = {'tn': 'resultjson_com',
            # 'logid': '7603311155072595725',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': -1,
            'z': '',
            'ic': '',
            'hd': '',
            'latest': '',
            'copyright': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0,
            'istype': 2,
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'force': '',
            'cg': '',    # 这个参数没公开，但是不可少
            'pn': pn,    # 显示：30-60-90
            'rn': '30',  # 每页显示 30 条
            'gsm': '1e',
            '1618827096642': ''
        }
        respons = requests.get(url = url,headers = headers,params = param)
        if respons.status_code == 200:
            print('Request success!')
        respons.encoding = 'utf-8'

        html = respons.text
        imageUrls = re.findall(r'"thumbURL":(.*?)',html,re.S)
        
        if not os.path.exists(savePath):
            os.mkdirs(savePath)

        i_url = imageUrls[random.randint(0,Counter(imageUrls))]
        data = requests.get(url = i_url,headers =headers).content
        with open(os.path.join(savePath,f'{keyword}.jpg'),'wb') as f:
            f.write(data)

def GetImageURL(keyword:str,page:int):
    for pn in range(0,30*page,30):
        param = {'tn': 'resultjson_com',
            # 'logid': '7603311155072595725',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': -1,
            'z': '',
            'ic': '',
            'hd': '',
            'latest': '',
            'copyright': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': 0,
            'istype': 2,
            'qc': '',
            'nc': '1',
            'fr': '',
            'expermode': '',
            'force': '',
            'cg': '',    # 这个参数没公开，但是不可少
            'pn': pn,    # 显示：30-60-90
            'rn': '30',  # 每页显示 30 条
            'gsm': '1e',
            '1618827096642': ''
        }
        respons = requests.get(url = url,headers = headers,params = param)
        if respons.status_code == 200:
            print('Request success!')
        respons.encoding = 'utf-8'

        ReJSON = respons.text
        #imageUrls = re.findall(r'((?<=(data-thumburl="))[\S]*)(?=")',html,re.S)
        #print(ReJSON)
        imageUrls = re.findall('"thumbURL":"(.*?)",',ReJSON,re.S)
        return imageUrls