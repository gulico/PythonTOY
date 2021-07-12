from bs4 import BeautifulSoup #网页解析
import re #正则，文字匹配
import urllib.request,urllib.error,urllib #制定url，获取网页数据
import requests
import xlwt #excel操作
import sqlite3 #数据库操作
import time
import random
from util.logmodule import LogModul
from util.proxy import Proxy

logger = LogModule()
proxy = Proxy(logger)
# 爬取网页

def getData(baseURL):
    topic_dataList = []  # 存储主题帖列表
    rely_dataList = []  # 存储回复的列表
    count =0
    for i in range(77, 143):  # n页人，每页25帖
        url = baseURL + str(i * 25)
        count += 1
        html = askURL(url,count)
        print(url)
        # 解析帖子列表
        topic_soup = BeautifulSoup(html, "html.parser")
        # print(topic_soup)
        topic_list = topic_soup.find("table", class_="olt").find_all('tr')
        # print(topic_list)

        for j in range(1, 26):  # 遍历每页25个帖子

            topic_data = []
            try:
                topic_name = topic_list[j].find_all("a")[0].get_text()  # 标题
                author = topic_list[j].find_all("a")[1].get_text()  # 楼主
                author_id = topic_list[j].find_all("a")[1].attrs['href'].split(r'/')[4]  # 楼主id
                reply_count = topic_list[j].find("td", class_="r-count").get_text()  # 回复数
                if (reply_count == ''):
                    reply_count = 0
                update_time = topic_list[j].find("td", class_="time").get_text()  # 最后更新时间
                topic_url = topic_list[j].find_all("a")[0].attrs['href']  # 帖子链接
                topic_id = topic_url.split(r'/')[5]  # 帖子id
                major_topic = ""  # 主楼内容
                print(topic_name, author, author_id, reply_count, update_time, topic_id, major_topic)
                # print(int(int(reply_count)/100)+1)
                for page in range(0, int(int(reply_count) / 100) + 1):  # 遍历帖子
                    topic_url_page = topic_url + "?start=" + str(page * 100)
                    count += 1
                    topic_html_page = askURL(topic_url_page,count)

                    # 解析回复
                    topic_soup_page = BeautifulSoup(topic_html_page, "html.parser")
                    if (page == 0):
                        major_topic_list = topic_soup_page.find("div", class_="topic-content").find_all("p")  # 主楼内容
                        for line in major_topic_list:
                            major_topic = major_topic + line.get_text()
                    reply_list = topic_soup_page.find_all("div", class_="reply-doc content")  # 回复列表
                    for reply in reply_list:
                        rely_data = []
                        user_id = reply.a.attrs['href'].split(r'/')[4]  # 回复人id
                        user_name = reply.find_all("a", class_="")[0].get_text()  # 回复人昵称
                        rely_time = reply.find_all("span", class_="pubtime")[0].get_text()  # 回复时间
                        comment = reply.find_all("p", class_="reply-content")[0].get_text()  # 回复内容

                        print(user_id, user_name, rely_time, comment)
                        rely_data.append(user_id)
                        rely_data.append(user_name)
                        rely_data.append(rely_time)
                        rely_data.append(comment)
                        rely_data.append(topic_id)

                        rely_dataList.append(rely_data)

                topic_data.append(topic_name)
                topic_data.append(author)
                topic_data.append(author_id)
                topic_data.append(reply_count)
                topic_data.append(update_time)
                topic_data.append(topic_id)
                topic_data.append(major_topic)

                topic_dataList.append(topic_data)

                #

            except Exception as e:
                print(e)
                print("帖子解析失败")
            else:
                print("解析成功")
        saveData2DB(rely_dataList, dbpath, 1)
        rely_dataList.clear()
        saveData2DB(topic_dataList, dbpath, 0)
        topic_dataList.clear()
        print(i)
    return topic_dataList, rely_dataList


def make_cookie(cookie_info):
    cookie_list = [info.strip().split('=') for info in cookie_info.split(';')]
    cookie = {data[0]: data[1].replace('"', '') for data in cookie_list}
    return cookie


# 获取单个网页
def askURL(url,count):
    # 数据头，伪装浏览器

    print("count",count)
    if(count%2==0):
        # 为了避免豆瓣反爬虫机制，连续回复的次数越多，sleep的时间越长
        random_sleep = random.randint(30, 40)
        # logger.info("Sleep for " + str(random_sleep) + " seconds")
        time.sleep(random_sleep)

    cookie_info = [
        'douban-fav-remind=1; _vwo_uuid_v2=D98484F3513B163F539656BA2F6A8DE51|db2c768bb07b9f13eef10390c0a60413; __gads=ID=ac84f573b549c2d9:T=1570668553:S=ALNI_MZHP-oU0A9pgzkM8aDMvNcdt6k8jQ; douban-profile-remind=1; gr_user_id=9bc17822-5856-494b-a366-5c5e46d6bcf7; _ga=GA1.2.1623359302.1569843891; ll="118172"; bid=ByTvLwM3R-Y; __yadk_uid=z5tIITZHJyKnSfmfXHnc49KrGogSy6Ss; ct=y; __utmz=30149280.1619427712.390.9.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; push_doumail_num=0; frodotk_db="0b8a9047778d480a229fb0d666a7d81e"; push_noty_num=0; dbcl2="8679427:ktm1AK7dMrk"; ck=j60t; __utmv=30149280.867; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1620562683%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1623359302.1569843891.1620557590.1620562684.448; __utmt=1; _pk_id.100001.8cb4=d9893e1ac327953c.1569843890.2233.1620562736.1620560627.; __utmb=30149280.31.5.1620562735876',
        '__utma=30149280.1672118031.1620539799.1620563402.1620567768.3; __utmb=30149280.28.6.1620567814411; __utmc=30149280; __utmv=30149280.18987; __utmz=30149280.1620567768.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_doumail_num=0; push_noty_num=0; _pk_id.100001.8cb4=f3868e338ec3a9fb.1620539798.4.1620567814.1620563402.; _pk_ses.100001.8cb4=*; __utmt=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1620567759%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DmU54B1Ki8opgywdv1-So_C2qtCJa5bNkthAWgUYGMdVNo606OzGjqlm_VFLV1ohY%26wd%3D%26eqid%3Dcbf9a1140014d914000000056097e6c7%22%5D; ck=XvUM; dbcl2="189871423:ufC/MXrC934"; douban-fav-remind=1; __yadk_uid=HkI9bCMBM7sA79IGZCJWaAR9oBa8Ho0b; bid=oG0d-p4KEV8; ll="118172"'
    ]
    cookies = []
    for e in cookie_info:
        cookies.append(make_cookie(e))

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
    }
    try:
        now_cookie = random.choice(cookies)
        html = requests.get(url, headers=headers, cookies=now_cookie).content.decode()
    except Exception as e:
        print(e)
        print("开网页失败")

    return html


# 保存数据到数据库
def saveData2DB(datalist, dbpath, flag):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    sql = ""
    if (flag == 0):
        sql = "insert into topics(topic_name,author,author_id,reply_count,update_time,topic_id,major_topic) values(?,?,?,?,?,?,?)"
    else:
        sql = "insert into replies(user_id,user_name,rely_time,comment,topic_id) values(?,?,?,?,?)"
    for data in datalist:
        cursor.execute(sql, data)

        conn.commit()
    cursor.close()
    conn.close()

def init_db(dbpath):
    sql1 = '''
        CREATE TABLE topics
        (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            topic_name varchar,
            author varchar,
            author_id varchar,
            reply_count varchar,
            update_time varchar,
            topic_id varchar,
            major_topic varchar 
        )
    '''
    sql2 = '''
        CREATE TABLE replies
        (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            user_id varchar,
            user_name varchar,
            rely_time varchar,
            comment varchar,
            topic_id varchar
        )
    '''
    conn = sqlite3.connect(dbpath) #文件存在即打开，不存在即创建
    cursor = conn.cursor()
    cursor.execute(sql1)
    cursor.execute(sql2)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    dbpath = "topic.db"
    # init_db(dbpath)
    baseURL = "https://www.douban.com/group/697229/discussion?start="
    count = 0
    topic_dataList,rely_dataList = getData(baseURL)
    # http://115.221.246.62:9999