# -*- coding = utf-8 -*-
# @Time : 2022/1/21 20:08
# @Author : Ben Gao
# @File : SpiderTest.py
# @Software : PyCharm

import pandas as pd
from selenium import webdriver
import matplotlib
matplotlib.rc("font", family='KaiTi')
from matplotlib import pyplot
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import time
import socket
socket.setdefaulttimeout(20)

# 获取信息，pn为爬取的页数，uid为所爬UP主的UID
def getinfo(pn, uid, totalplay):
    # 初始化
    # pl = []
    # count = 0

    # totalplay = []
    name = ""

    for i in range(0, 12):
        totalplay.append(0)

    # 爬取网页
    for pn in range(1, pn+1):
        data = {
            "tid": 0,
            "page": pn,
            "keyword": "",
            "order": "pubdate",
        }
        url = "https://space.bilibili.com/" + uid + "/video?" + urlencode(data)

        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)                                       # 防止网页还没打开
        html = driver.page_source
        time.sleep(5)
        soup = BeautifulSoup(html, 'lxml')
        info = soup.find_all(name="li", class_=re.compile(r"small-item fakeDanmu-it.+"))

        # 获取UP主昵称
        name = soup.select_one("#app.visitor > div.h > div.wrapper > div.h-inner > div.h-user > div.h-info.clearfix > div.h-basic > div > span#h-name").text

        # result = ""

        for li_tag in info:

            # 获取标题、URL
            # tudata = li_tag.find_all(name="a", class_="title")
            # for a_tag in tudata:
            #     result = "TITLE: " + a_tag.get("title") + " " + "URL: " + a_tag.get("href")

            # 获取播放量
            ptdata = li_tag.find_all(name="div", class_="meta")
            sp = BeautifulSoup(str(ptdata), 'lxml')
            play = sp.select_one("span.play").text
            play = re.sub(" ", "", play)
            play = play.strip("\n")

            # 将播放量转换为整型数字
            if (play != re.sub("万", "", play)):
                play = re.sub("万", "", play)
                play = float(play) * 10000
                play = int(play)
            else:
                play = int(play)

            # pl.append(str(play))

            # 获取发布时间
            ti = sp.select_one("span.time").text
            ti = re.sub(" ", "", ti)
            ti = ti.strip("\n")

            # 统计每月播放量
            for i in range(1, 13):
                date = "2021-" + str(i) + "-.+"
                try:
                    tmp = re.compile(date)
                    y = tmp.match(ti)
                    y = y.group()                           # 无意义，为了判断是否匹配，如不匹配，则会报错
                    totalplay[i - 1] = totalplay[i - 1] + play
                except Exception as e:
                    pass

        time.sleep(5)

    # # 折线图显示
    # date = []
    # for i in range(1, 13):
    #     date.append("2021-" + str(i))
    #
    # pyplot.style.use("bmh")
    # pyplot.plot(date, tpl, marker="o", markerfacecolor="blue")
    # pyplot.legend(["播放量"])
    # current_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # title = name + " 2021年各月播放量统计" + "（截止时间：" + current_time + "）"
    # pyplot.title(title, fontsize=20)
    # pyplot.xlabel("月份", fontsize=10)
    # pyplot.ylabel("播放量", fontsize=10)
    # pyplot.tick_params(axis="both", labelsize=10)
    #
    # for (x, y) in zip(date, tpl):
    #     pyplot.text(x, y, y, ha="center", va="bottom", fontsize=10, family="MicroSoft YaHei")
    #
    # current_date = str(time.strftime("%Y-%m-%d", time.localtime()))
    # pyplot.savefig(name + " 2021年各月播放量统计 " + current_date + ".jpg")
    # pyplot.show()

    # result = result + " " + "PLAY: " + play + " " + "TIME: " + ti + "\n"
    # f = open("data.txt", "a", encoding="utf-8")
    # f.write(result)
    # f.close()
    # print(result)
    # result = ""

    # global count
    #
    # for i in pl:
    #     if(i != re.sub("万", "", i)):
    #         i = re.sub("万", "", i)
    #         i = float(i) * 10000
    #         i = int(i)
    #         pl[count] = i
    #     else:
    #         pl[count] = int(pl[count])
    #     count = count + 1
    #
    # for i in pl:
    #     print(i)

    return name

def comparison(num):
    # 初始化
    uidlist = []
    for i in range (0, num):
        uidlist.append(input("请输入UP主的UID："))

    date = []
    for i in range(1, 13):
        date.append("2021-" + str(i))

    data = {}

    namelist = ""

    # 通过pandas储存数据
    for uid in uidlist:
        totalplay = []
        name = getinfo(5, str(uid), totalplay)
        namelist = namelist + name + " "
        data[name] = pd.Series(data=totalplay, index=date)

    result = pd.DataFrame(data)

    # 柱状图显示
    pyplot.style.use("bmh")
    current_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    result.plot(kind="bar", style="--o", title=namelist + "2021年各月播放量对比（截止时间：" + current_time + "）", color=["red", "blue", "green"])
    pyplot.xlabel("月份", fontsize=10)
    pyplot.ylabel("播放量", fontsize=10)
    current_date = str(time.strftime("%Y-%m-%d", time.localtime()))
    pyplot.savefig(namelist + " 2021年各月播放量对比 " + current_date + ".jpg")
    pyplot.show()

if __name__ == "__main__":
    comparison(3)                                            # 输入UP主数量，后通过函数比较UP主2021年各月播放量

    # getinfo(5, "147166910")                                # 输入爬取页数及UID
    # getinfo(5, "5970160")                                  # 输入爬取页数及UID
    # getinfo(5, "562197")                                   # 输入爬取页数及UID

    # time.sleep(10)