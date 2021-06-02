#!usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2021/6/2 15:07
# @Author  : Fandes
# @FileName: test.py
# @Software: PyCharm
import datetime
import random
import sys
import time

import pytz
import requests


def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()  # 返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = '【奇怪的知识】\n' + english + '\n' + zh_CN
    return str


def get_weather():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'  # API地址，必须配合城市代码使用
        city_code = '101110105'  # 进入https://where.heweather.com/index.html查询你的城市代码
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()  # 将数据以json形式返回，这个d就是返回的json数据
        if d['status'] == 200:  # 当返回状态码为200，输出天气状况
            parent = d["cityInfo"]["parent"]  # 省
            city = d["cityInfo"]["city"]  # 市
            update_time = d["time"]  # 更新时间
            date = d["data"]["forecast"][0]["ymd"]  # 日期
            week = d["data"]["forecast"][0]["week"]  # 星期
            weather_type = d["data"]["forecast"][0]["type"]  # 天气
            wendu_high = d["data"]["forecast"][0]["high"]  # 最高温度
            wendu_low = d["data"]["forecast"][0]["low"]  # 最低温度
            shidu = d["data"]["shidu"]  # 湿度
            pm25 = str(d["data"]["pm25"])  # PM2.5
            pm10 = str(d["data"]["pm10"])  # PM10
            quality = d["data"]["quality"]  # 天气质量
            fx = d["data"]["forecast"][0]["fx"]  # 风向
            fl = d["data"]["forecast"][0]["fl"]  # 风力
            ganmao = d["data"]["ganmao"]  # 感冒指数
            tips = d["data"]["forecast"][0]["notice"]  # 温馨提示
            # 天气提示内容
            tdwt = "【今日份天气】\n城市： " + parent + city + \
                   "\n日期： " + date + "\n星期: " + week + "\n天气: " + weather_type + "\n温度: " + wendu_high + " / " + wendu_low + "\n湿度: " + \
                   shidu + "\nPM25: " + pm25 + "\nPM10: " + pm10 + "\n空气质量: " + quality + \
                   "\n风力风向: " + fx + fl + "\n感冒指数: " + ganmao + "\n温馨提示： " + tips + "\n更新时间: " + update_time + "\n✁-----------------------------------------\n" + get_iciba_everyday()
            # print(tdwt)
            return tdwt, d
            # requests.post(cpurl,tdwt.encode('utf-8'))         #把天气数据转换成UTF-8格式，不然要报错。
    except Exception:
        print(sys.exc_info())
        print(Exception)
        return None, None
def gethour():
    cn = pytz.country_timezones('cn')[0]
    tz = pytz.timezone(cn)
    return datetime.datetime.now(tz).hour

def get_email():
    now = gethour()
    print(now)
    try:
        weatherstr, d = get_weather()
        high = int(str(d["data"]["forecast"][0]["high"]).split(" ")[-1][:2])
        tips = ""
        if now <= 8:
            if "雨" in weatherstr:
                tips = "今天要下雨了噢,记得带伞!\n"

            emailstr = "宝宝早上好\n" + tips + weatherstr
        elif now <= 15:
            if high > 30 and random.randint(0, 80) % 2 == 0:
                tips = "天气好热啊,记得多喝水!"
            elif "干燥" in weatherstr and random.randint(0, 80) % 3 == 0:
                tips = "天气好干燥啊,记得多喝热水!\n"
            if random.randint(0, 80) % 3 == 0:
                tips += "有没有好好起床吃饭\n"
            emailstr = "宝宝中午好\n" + tips
        else:
            if "注意保暖" in weatherstr:
                tips = "天气有点凉了,记得盖好被子!"
            elif high > 30 and random.randint(0, 80) % 5 == 0:
                tips = "空调不要开太低!小心着凉!"
            if random.randint(0, 80) % 5 == 0:
                tips = "别告诉我你又跑出去了 哼~"
            elif random.randint(0, 80) % 5 == 0:
                tips = "放下那手机!"
            emailstr = "宝宝晚安!\n" if random.randint(0, 20) % 2 == 0 else "宝宝该睡觉了\n" + tips
    except:
        print(sys.exc_info(), 92)
        if now < 6:
            emailstr = "宝宝早上好"
        elif now < 15:
            emailstr = "宝宝中午好"
        else:
            emailstr = "宝宝快睡觉,晚安!"
    print(emailstr)
    with open("emailtext.txt", "w", encoding="utf-8") as f:
        f.write(emailstr)

if __name__ == '__main__':
    get_email()
