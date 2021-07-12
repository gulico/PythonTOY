from bs4 import BeautifulSoup  # 网页解析
import re  # 正则，文字匹配
import urllib.request, urllib.error, urllib  # 制定url，获取网页数据
import requests
import sqlite3  # 数据库操作
import time
import random
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5',
    'Host': 'www.douban.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'close'
}

dbpath = "LH.db"
ua_list = []
ip_list = ['https://113.103.140.35:42805',
'https://114.97.37.184:38097',
'https://117.68.192.248:33941',
'https://114.226.161.127:46190',
'https://121.228.112.190:41986',
'https://49.86.181.30:55917',
'https://36.56.147.220:49855',
'https://114.227.160.120:42445',
'https://49.85.54.94:34149',
'https://113.73.67.254:36216']

proxies = {"http": "http://182.34.37.112:15936"}
# 爬取网页

def getData(baseURL):
    count = 0;
    dataList = []
    for i in range(0, 6):  # n页人，每页35人
        url = baseURL + str(i * 35)
        soup, code = askURL(url)
        # 解析数据
        # soup = BeautifulSoup(html, "html.parser")
        member_list = soup.find_all("div", class_="member-list")[-1]
        #print(member_list)

        for item in member_list.find_all("div", class_="name"):
            count += 1
            data = []
            user_id = item.a.attrs['href']
            user_id = user_id.split(r'/')[4]
            user_name = item.find_all("a", class_="")[0].get_text()
            print(user_id, user_name)

            data.append(user_id)
            data.append(user_name)

            dataList.append(data)
        print(i)
        global dbpath
        saveData2DB(dataList, dbpath)
        dataList.clear()
        # # 为了避免豆瓣反爬虫机制，连续回复的次数越多，sleep的时间越长
        # random_sleep = random.randint(10, 20)
        # # logger.info("Sleep for " + str(random_sleep) + " seconds")
        # time.sleep(random_sleep)
    return dataList, count


# 获取单个网页
def askURL(url):
    global headers
    global proxies
    html = ""
    r = []
    while True:
        try:
            _set_random_ua()
            _set_random_ip()
            r = requests.get(url, headers=headers, proxies=proxies, timeout=5)
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

def get_ip():
    """
    远程获取ip
    :return:
    """
    targetUrl = "http://piping.mogumiao.com/proxy/api/get_ip_al?appKey=1b02954cf24540e79f1e6875026f3bbb&count=10&expiryDate=0&format=1&newLine=2"
    response = requests.get(targetUrl)
    response_text = response.text
    response_json = json.loads(response_text)
    print(response)
    print(response_json)

    global ip_list
    for info in response_json['msg']:
        ip = info['ip']
        port = info['port']
        ip_port = 'https://' + ip + ":" + port
        print(ip_port)
        ip_list.append(ip_port)

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
    proxies.clear()
    proxies['http'] = rand_ip.strip('\n')
    proxies['https'] = rand_ip.strip('\n')
    print('当前ip设置为' + str(proxies))

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


# 保存数据到数据库
def saveData2DB(datalist, dbpath):
    #init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    for data in datalist:
        # sql = 'insert into mjq values(?,?,?,?)'%(data[0].strip('"'),data[1].strip('"'),data[2].strip('"'),data[3].strip('"'))
        cursor.execute("insert into zzptlms(user_id,user_name) values(?,?)", data)
        conn.commit()
    cursor.close()
    conn.close()

def init_db(dbpath):
    sql = '''
        CREATE TABLE zzptlms
        (
            id INTEGER  PRIMARY KEY AUTOINCREMENT,
            user_id varchar,
            user_name varchar
        )
    '''
    conn = sqlite3.connect(dbpath) #文件存在即打开，不存在即创建
    cursor = conn.cursor()
    cursor.execute(sql)
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
    baseURL = "https://www.douban.com/group/719203/members?start="
    dbpath = "LH.db"
    init_au()
    init_db(dbpath)
    datalist, count = getData(baseURL)

    saveData2DB(datalist,dbpath)
