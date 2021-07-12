from bs4 import BeautifulSoup  # 网页解析
import re  # 正则，文字匹配
import urllib.request, urllib.error, urllib  # 制定url，获取网页数据
import requests
import sqlite3  # 数据库操作
import time
import random
from util.logmodule import LogModule
from util.proxy import Proxy

logger = LogModule()
proxy = Proxy(logger)

# 爬取网页

def getData(session, baseURL):
    topic_dataList = []  # 存储主题帖列表
    count = 0
    proxy_threshold = random.randint(50, 80)
    for i in range(222580919, 223916156):  # 133w个帖子
        topic_data = []
        url = baseURL + str(i)
        print(url)
        html, statuscode = askURL(session, url)
        if statuscode == 404 or statuscode == 403: #404帖子被删了，403私密小组
            continue
        # 解析帖子列表

        topic_soup = BeautifulSoup(html, "html.parser")
        topic_content = topic_soup.find("div", id="topic-content")
        # print(topic_content)
        topic_name = topic_content.find("table", class_="infobox")  # 标题
        if (topic_name is None):
            topic_name = topic_soup.find("h1").get_text()
        else:
            topic_name = topic_name.find("td", class_="tablecc").get_text().split(r'<strong>标题：</strong>')[1]

        # topic_name = topic_content.find("table", class_="infobox").find("td", class_="tablecc").get_text().split(r'<strong>标题：</strong>')[1]
        author = topic_content.find("span", class_="from").find("a").get_text()  # 楼主
        author_id = topic_content.find("span", class_="from").find("a").attrs['href'].split(r'/')[4]  # 楼主id
        major_topic_list = topic_content.find_all("p")  # 主楼内容
        major_topic = ""
        for line in major_topic_list:
            major_topic = major_topic + line.get_text()
        topic_id = str(i)  # 帖子编号
        update_time = topic_content.find("span", class_="create-time color-green").get_text()  # 更新时间
        # reply_count
        group_name = topic_soup.find("div", class_="group-item").find("div", class_="title").find("a").get_text()  # 组名
        group_id = \
        topic_soup.find("div", class_="group-item").find("div", class_="title").find("a").attrs['href'].split(r'/')[
            4]  # 组id
        print(topic_name, author, author_id, update_time, topic_id, major_topic, group_name, group_id)
        # check_str = topic_name+major_topic

        topic_data.append(topic_name)
        topic_data.append(author)
        topic_data.append(author_id)
        # topic_data.append(reply_count)
        topic_data.append(update_time)
        topic_data.append(topic_id)
        topic_data.append(major_topic)
        topic_data.append(group_name)
        topic_data.append(group_id)

        topic_dataList.append(topic_data)

        count += 1
        # 当前的proxy用到一定次数之后，换成一个新的
        if count == proxy_threshold:
            proxy.update_proxy()
            count = 0
            proxy_threshold = random.randint(50, 80)
            saveData2DB(topic_dataList, "topic.db")
            topic_dataList.clear()
            random_sleep = random.randint(5, 10)
            logger.info("Sleep for " + str(random_sleep) + " seconds")
            time.sleep(random_sleep)

    return topic_dataList


# 获取单个网页
def askURL(session, url):
    # 数据头，伪装浏览器
    html = ""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
        'Host': 'www.douban.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    r = []
    try:
        r = session.get(url, headers=headers, proxies=proxy.proxy, timeout=5)
        if r.status_code != 200:
            logger.error("Failed to retrieve group topics: " + str(r.status_code))
            proxy.update_proxy()
        html = r.content.decode()
    except Exception as e:
        logger.error("Failed to send request: " + str(e))
        print("开网页失败")

    return html, r.status_code


# 保存数据到数据库
def saveData2DB(datalist, dbpath):
    # init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    # topic_name, author, author_id, update_time, topic_id, major_topic, group_name, group_id
    sql = "insert into topics(topic_name,author,author_id,update_time,topic_id,major_topic,group_name,group_id) values(?,?,?,?,?,?,?,?)"
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
            update_time varchar,
            topic_id varchar,
            major_topic varchar,
            group_name varchar,
            group_id varchar
        )
    '''
    conn = sqlite3.connect(dbpath)  # 文件存在即打开，不存在即创建
    cursor = conn.cursor()
    cursor.execute(sql1)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    dbpath = "topic.db"

    s = requests.Session()

    baseURL = "https://www.douban.com/group/topic/"

    # init_db(dbpath)
    topic_dataList = getData(s, baseURL)
    saveData2DB(topic_dataList, dbpath)
    # http://115.221.246.62:9999
