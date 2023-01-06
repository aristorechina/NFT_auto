#!/usr/bin/python 
# -*- coding: utf-8 -*-

import qrcode
import time
import requests
from urllib.parse import urlencode
from hashlib import md5
from typing import Union
from requests_toolbelt.multipart.encoder import MultipartEncoder
import imghdr
import os
import sys

# 声明
# =================================================================================================
print("哔哩哔哩钻石标自定义头像程序")
print("作者:Aristore 转发请注明出处")
print("制作不易 求三连 求关注")
#仓库地址
print("本程序在github开源 https://github.com/aristorechina/NFT_auto/")
print("本程序仅供学习交流,请勿用于违规用途")
print("使用方法:请将需要更改的头像放置与当前程序所在目录下,名字应为 face ,格式应为 jpg 或 png ,程序默认优先识别 face.jpg")


#获取当前文件所在目录
path = os.path.dirname(os.path.realpath(sys.argv[0]))
new_path = "/".join(path.split("\\"))

# 头像所在目录
if os.path.exists("{}/face.jpg".format(new_path)):
    FACE_PATH = "{}/face.jpg".format(new_path)
elif os.path.exists("{}/face.png".format(new_path)):
    FACE_PATH = "{}/face.png".format(new_path)
else:
    pass

# 登录模块
# =================================================================================================

# 为请求参数进行 api 签名
def tvsign(params, appkey='4409e2ce8ffd12b8', appsec='59b43e04ad6965f34319062b478f83dd'):
    params.update({'appkey': appkey})
    params = dict(sorted(params.items())) # 重排序参数 key
    query = urlencode(params) # 序列化参数
    sign = md5((query+appsec).encode()).hexdigest() # 计算 api 签名
    params.update({'sign':sign})
    return params

# 获取二维码数据
loginInfo = requests.post('https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code',params=tvsign({
    'local_id':'0',
    'ts':int(time.time())
})).json()

# 生成二维码
creat_qrcode = qrcode.make(loginInfo['data']['url'])

#保存二维码
with open('{}/qrcode.jpg'.format(new_path), 'wb') as f:
    creat_qrcode.save(f)
print("已在本目录下生成登录二维码,用手机打开B站扫码登录")

#校验
while True:
    pollInfo = requests.post('https://passport.bilibili.com/x/passport-tv-login/qrcode/poll',params=tvsign({
        'auth_code':loginInfo['data']['auth_code'],
        'local_id':'0',
        'ts':int(time.time())
    })).json()
    
    if pollInfo['code'] == 0:
        loginData = pollInfo['data']
        print("登录成功!")
        break
        
    elif pollInfo['code'] == -3:
        print('API校验密匙错误')
        raise
    
    elif pollInfo['code'] == -400:
        print('请求错误')
        raise
        
    elif pollInfo['code'] == 86038:
        print('二维码已失效')
        raise
        
    elif pollInfo['code'] == 86039:
        time.sleep(5)
    
    else:
        print('未知错误')
        raise

# 返回数据

UID = loginData['mid']
ACCESS_KEY = loginData['access_token']

#选择需要的卡片种类
card_type = str(input("请在选择您想使用的卡片种类后再下方输入其对应id后按下回车\n可选择id_(胶囊计划:4 三体:14)\n"))

# 更改头像模块
# =================================================================================================
class Crypto:

    APPKEY = '4409e2ce8ffd12b8'
    APPSECRET = '59b43e04ad6965f34319062b478f83dd'

    @staticmethod
    def md5(data: Union[str, bytes]) -> str:
        '''generates md5 hex dump of `str` or `bytes`'''
        if type(data) == str:
            return md5(data.encode()).hexdigest()
        return md5(data).hexdigest()

    @staticmethod
    def sign(data: Union[str, dict]) -> str:
        '''salted sign funtion for `dict`(converts to qs then parse) & `str`'''
        if isinstance(data, dict):
            _str = urlencode(data)
        elif type(data) != str:
            raise TypeError
        return Crypto.md5(_str + Crypto.APPSECRET)


class SingableDict(dict):
    @property
    def sorted(self):
        '''returns a alphabetically sorted version of `self`'''
        return dict(sorted(self.items()))

    @property
    def signed(self):
        '''returns our sorted self with calculated `sign` as a new key-value pair at the end'''
        _sorted = self.sorted
        return {**_sorted, 'sign': Crypto.sign(_sorted)}


def get_image_type(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return imghdr.what(None, data)


def upload_image(file_path):
    url = "https://api.bilibili.com/x/upload/app/image?access_key=" + ACCESS_KEY

    payload = {'bucket': 'medialist', 'dir': 'nft'}

    with open(file_path, 'rb') as f:
        type = f'image/{imghdr.what(f)}'
        print(type)
        files = [
            (
                'file',
                (file_path, f, type),
            )
        ]
        response = requests.request("POST", url, data=payload, files=files)
        print(response.text)
        return response.json()['data']['location']

#获取卡片信息
def get_one_card_id():
    url = "https://api.bilibili.com/x/vas/nftcard/cardlist"
    params = SingableDict(
        {
            "access_key": ACCESS_KEY,
            "act_id": card_type,
            "appkey": "4409e2ce8ffd12b8",
            "disable_rcmd": "0",
            "ruid": UID,
            "statistics": "{\"appId\":1,\"platform\":3,\"version\":\"7.9.0\",\"abtest\":\"\"}",
            "ts": int(time.time()),
        }
    ).signed
    response = requests.request("GET", url, params=params)
    data = response.json()

    #遍历数据，得出可用结果输出供用户选择

    print("请在下列卡片中选择一个(卡片名称:对应卡片id)")
    for round in data['data']['round_list']:
        for card in round['card_list']:
            if card['card_id_list']:
                print(card['card_name'], ":", card['card_id_list'][0]['card_id'])
    if data['data']['pre_list']:
        for pre in data['data']['pre_list']:
            if pre['card_id_list']:
                print(pre['card_name'], ":", pre['card_id_list'][0]['card_id'])
    choose_card_id = input("在下方输入其id后回车继续(如果没有就回车退出):\n")
    return choose_card_id

def set_face(card_id):
    api = "https://api.bilibili.com/x/member/app/face/digitalKit/update"
    params = SingableDict(
        {
            "access_key": ACCESS_KEY,
            "appkey": "4409e2ce8ffd12b8",
            "build": "7090300",
            "c_locale": "zh_CN",
            "channel": "xiaomi",
            "disable_rcmd": "0",
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "statistics": "{\"appId\":1,\"platform\":3,\"version\":\"7.9.0\",\"abtest\":\"\"}",
            "ts": int(time.time()),
        }
    ).signed
    m = MultipartEncoder(
        fields={
            'digital_kit_id': str(card_id),
            'face': ('face', open(FACE_PATH, 'rb'), 'application/octet-stream'),
        }
    )
    headers = {
        "Content-Type": m.content_type,
    }
    response = requests.request("POST", api, data=m, headers=headers, params=params)
    if response.json()['code'] != 0:
        print(response.json())
        return
    print('设置头像成功, 请等待审核')

def main():
    card_id = get_one_card_id()
    if not card_id:
        return
    set_face(card_id)

if __name__ == '__main__':
    main()
    input("按下回车键结束")