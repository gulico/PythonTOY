from typing import List, Any

from bs4 import BeautifulSoup  # 网页解析
import re  # 正则，文字匹配
import urllib.request, urllib.error, urllib  # 制定url，获取网页数据
import requests
import sqlite3  # 数据库操作
import time
import random
import json


#name = input();

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
    'Host': 'www.douban.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'close'
}

ua_list = []
ip_list = []

proxies = {"http": "http://gulico:1996108wxy@111.74.88.96:57114",
           "https": "http://gulico:1996108wxy@111.74.88.96:57114"}

def getData(session, baseURL):
    topic_dataList = []  # 存储主题帖列表
    count = 0
    threshold = random.randint(50, 80)
    for i in range(222590265, 223916156):  # 133w个帖子
        topic_data = []
        url = baseURL + str(i)
        print(url)
        topic_soup, statuscode = askURL(session, url)
        if statuscode == 404 or statuscode == 403:  # 404帖子被删了，403私密小组
            continue
        # 解析帖子列表

        # topic_soup = BeautifulSoup(html, "html.parser")
        topic_content = topic_soup.find("div", id="topic-content")
        # print(topic_content)
        topic_name = topic_soup.find("h1").get_text()

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
        saveData2DB(topic_dataList, "topic.db")
        topic_dataList.clear()

    return topic_dataList

# 获取单个网页
def askURL(session, url):
    global headers
    global proxies
    html = ""
    r = []
    while True:
        try:
            _set_random_ua()
            _set_random_ip()
            r = session.get(url, headers=headers, proxies=proxies, timeout=5)
            html = r.content.decode("utf8", "ignore")
            soup = BeautifulSoup(html, "html.parser")
            title = soup.find("title").get_text()
            print(title)
            if r.status_code == 200 or (r.status_code == 404 and title == "页面不存在") or (
                    r.status_code == 403 and title == "没有访问权限"):
                return soup, r.status_code
            else:
                remove_ip(proxies.get("http"))
        except Exception as e:
            print("Failed to send request: " + str(e))
            remove_ip(proxies.get("http"))
    return None

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

# def _read_ip_list():
#     """
#     读取ip文件
#     :return:
#     """
#     ip_list_file_path = 'ip_list.txt'
#     ip_list = []
#     with open(ip_list_file_path, 'r') as f:
#         line = f.readline()
#         line = 'http://' + line
#         while line:
#             ip_list.append(line)
#             line = f.readline()
#     return ip_list

def get_ip():
    """
    远程获取ip
    :return:
    """
    proxyport = 57114  # 代理IP端口
    proxyusernm = "gulico"  # 代理帐号
    proxypasswd = "1996108wxy"  # 代理密码
    targetUrl = "http://gulico.v4.dailiyun.com/query.txt?key=NP659B93BB&word=&count=10&rand=false&ltime=0&norepeat=true&detail=false"
    response = requests.get(targetUrl)
    response_text = response.text
    # response_json = json.loads(response_text)
    html = response.content.decode()
    #print(html)
    html_list = html.split("\r\n")
    print(html_list)
    html_list.pop()
    #print(html.readline())
    # print(response_json)

    global ip_list
    for ip_port in html_list:
        proxyurl = 'http://' + proxyusernm + ":" + proxypasswd + "@" + ip_port
        #print(proxyurl)
        ip_list.append(proxyurl)

        # for info in response_json['msg']:
    #     ip = info['ip']
    #     port = info['port']
    #     ip_port = 'http://' + proxyusernm+":"+proxypasswd+"@"+ip+":"+"%d"%port
    #     print(ip_port)
    #     ip_list.append(ip_port)

    random_sleep = random.randint(5, 10)
    time.sleep(random_sleep)

def remove_ip(check_ip_proxies):
    """
    移除无用ip
    :return:
    """
    global ip_list
    ip_list.remove(check_ip_proxies)
    if (len(ip_list) < 5):
        get_ip()

def _set_random_test_url():
    """
    随机生成测试url
    :return:
    """
    test_url_list = ['https://www.baidu.com/', 'https://www.sogou.com/', 'http://soso.com/', 'https://www.so.com/']
    rand = random.randint(0, len(test_url_list) - 1)
    rand_url = test_url_list[rand]
    return rand_url

def _set_random_ip():
    """
    设置随机ip, 并检查可用性
    :return:
    """
    global proxies
    global ip_list
    ip_len = len(ip_list)
    rand = random.randint(0, ip_len - 1)
    print(rand)
    rand_ip = ip_list[rand]
    # if 'https' in rand_ip:
    #  check_ip_proxies = {'https': rand_ip.strip('\n'),'https'}
    # else:
    #  check_ip_proxies = {'http': rand_ip.strip('\n')}
    proxies.clear()
    proxies['http'] = rand_ip.strip('\n')
    proxies['https'] = rand_ip.strip('\n')
    # print('当前ip' + str(check_ip_proxies) + '可行')
    print('当前ip设置为' + str(proxies))
    # ip_flag = False
    # while not ip_flag:
    #     #ip_list = _read_ip_list()
    #     ip_len = len(ip_list)
    #     rand = random.randint(0, ip_len - 1)
    #     print(rand)
    #     rand_ip = ip_list[rand]
    #     if 'https' in rand_ip:
    #         check_ip_proxies = {'https': rand_ip.strip('\n')}
    #     else:
    #         check_ip_proxies = {'http': rand_ip.strip('\n')}
    #     print('检查ip' + str(check_ip_proxies) + '可行性...')
    #     try:
    #         rand_url = _set_random_test_url()
    #         check_ip_response = requests.get(rand_url, proxies=check_ip_proxies, timeout=5)
    #         check_ip_status = check_ip_response.status_code
    #         if check_ip_status == 200:
    #             proxies.clear()
    #             proxies['http'] = rand_ip.strip('\n')
    #             print('当前ip' + str(check_ip_proxies) + '可行')
    #             print('当前ip设置为' + str(proxies))
    #             ip_flag = True
    #         else:
    #             print('当前ip' + str(check_ip_proxies) + '不可行, 尝试其他中...')
    #             remove_ip(ip_list[rand])
    #     except Exception as err:
    #         print('当前ip' + str(check_ip_proxies) + '不可行, 尝试其他中...' + str(err))
    #         remove_ip(ip_list[rand])

def _set_random_ua():
    """
    设置随机ua
    :return:
    """
    global ua_list
    global headers
    ua_len = len(ua_list)
    rand = random.randint(0, ua_len - 1)
    headers['User-Agent'] = ua_list[rand]
    print('当前ua为' + str(ua_list[rand]))

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

def init_au():
    global ua_list
    try:
        ua_list_file_path = 'ua_list.txt'
        with open(ua_list_file_path, 'r') as f:
            line = f.readline()
            while line:
                ua_list.append(line.strip('\n'))
                line = f.readline()
        print('UA初始化成功')
        return ua_list
    except Exception as err:
        print('UA初始化失败' + str(err))
    return None

if __name__ == '__main__':
    dbpath = "topic.db"

    s = requests.Session()
    get_ip()
    baseURL = "https://www.douban.com/group/topic/"
    init_au()
    # init_db(dbpath)
    topic_dataList = getData(s, baseURL)
    saveData2DB(topic_dataList, dbpath)