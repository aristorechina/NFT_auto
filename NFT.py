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
print("哔哩哔哩钻石标自定义头像程序")
print("作者:Aristore 转发请注明出处")
print("制作不易 求关注")
print("本程序仅供学习交流,请勿用于违规用途")
path = os.path.dirname(os.path.realpath(sys.argv[0]))
new_path = "/".join(path.split("\\"))
login_method = str(input("您希望以什么方式登录呢?(1:复制链接 2:扫码 3:自行输入数据)\n"))
if login_method == "1" or login_method == "2":
    def tvsign(params, appkey='4409e2ce8ffd12b8', appsec='59b43e04ad6965f34319062b478f83dd'):
        params.update({'appkey': appkey})
        params = dict(sorted(params.items()))
        query = urlencode(params)
        sign = md5((query+appsec).encode()).hexdigest()
        params.update({'sign':sign})
        return params
    loginInfo = requests.post('https://passport.bilibili.com/x/passport-tv-login/qrcode/auth_code',params=tvsign({
        'local_id':'0',
        'ts':int(time.time())
    })).json()
    if login_method == "1":
        print("以下为登录链接:")
        print(loginInfo['data']['url'])
    elif login_method == "2":
        creat_qrcode = qrcode.make(loginInfo['data']['url'])
        with open('{}/qrcode.jpg'.format(new_path), 'wb') as f:
            creat_qrcode.save(f)
        print("已在本目录下生成登录二维码,用手机打开B站扫码登录")
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
    UID = loginData['mid']
    ACCESS_KEY = loginData['access_token']
    print("UID{}".format(UID))
    print("ACCESS_KEY".format(ACCESS_KEY))
elif login_method == "2":
    UID = input("UID:\n")
    ACCESS_KEY = input("ACCESS_KEY:\n")
else:
    print("输入有误")
if os.path.exists("{}/{}.jpg".format(new_path,UID)):
    FACE_PATH = "{}/{}.jpg".format(new_path,UID)
elif os.path.exists("{}/{}.png".format(new_path,UID)):
    FACE_PATH = "{}/{}.png".format(new_path,UID)
else:
    pass
card_type = str(input("请在选择您想使用数字周边的卡片种类后再下方输入其对应id后按下回车\n目前存在的数字周边:\nSNH48荣耀时刻数字写真集:1\n胶囊计划数字典藏集:4\n天官赐福动画2周年数字典藏:5\nA-AKB48TSH四周年数字集换卡:6\nB-AKB48TSH四周年数字集换卡:7\nC-AKB48TSH四周年数字集换卡:8\nD-AKB48TSH四周年数字集换卡:9\nE-AKB48TSH四周年数字集换卡:10\nF-AKB48TSH四周年数字集换卡:11\nG-AKB48TSH四周年数字集换卡:12\nH-AKB48TSH四周年数字集换卡:13\n三体动画数字周边:14\n2022百大UP主数字卡集:18\n"))
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
