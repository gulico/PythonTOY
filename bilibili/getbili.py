import random
import time
import requests
import datetime
from lxml import etree
import json
from bs4 import BeautifulSoup #网页解析
import csv

import re
import urllib.parse
import base64
import hmac
from hashlib import sha1

# 豆瓣的sig算法
def hash_hmac(key, code, sha1):
    hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
    return base64.b64encode(hmac_code).decode()

def getguankanrenshu(vedioID):
    count = "error"
    total = "error"
    try:
        baseURL = "https://api.bilibili.com/x/player/online/total?"
        r = requests.get(baseURL+vedioID,timeout=5)
        if r.status_code != 200:
            print("Failed to retrieve webset: " + str(r.status_code))
            return None
        group_json = json.loads(r.text)
        count = 0
        total = 0
        #print(group_json)
        count = group_json["data"]["count"]
        total = group_json["data"]["total"]
        # print(count,total)
        return count,total
    except Exception as e:
        print("Failed to send request: " + str(e))
        return None

def getbufangliang(vedioID):
    bofang = "error"
    danmu = "error"
    try:
        baseURL = "https://www.bilibili.com/video/"
            # print(baseURL+vedioID)
        r = requests.get(baseURL+vedioID,timeout=5)
        if r.status_code != 200:
            print("Failed to retrieve webset: " + str(r.status_code))
            return bofang,danmu
        html = r.content.decode()
        soup = BeautifulSoup(html,"html.parser")
        video_data = soup.find("div",class_="video-data")
        bofang = video_data.find("span",class_="view").attrs['title'].split(r'总播放数')[1]
        danmu = video_data.find("span",class_="dm").attrs['title'].split(r'历史累计弹幕数')[1]
        # print(bofang,danmu)
        return bofang,danmu
    except Exception as e:
        print("Failed to send request: " + str(e))
        return bofang,danmu

def post_comment(session, topic_id,comment):
    try:
        create_comment_url = comment_url_template.format(topic_id=topic_id)

        timestamp = str(int(time.time()))
        sig = hash_hmac(
            client_secret,
            sig_code_template.format(topic_id=topic_id, timestamp=timestamp),
            sha1,
        )
        content = comment_content_template.format(
            comment=urllib.parse.quote(comment),
            sig=urllib.parse.quote(sig),
            timestamp=timestamp,
        )
        r = session.post(
            create_comment_url, data=content, timeout=5
        )
        #print(json.loads(r.text))
#         print(
#             "comment: {}, {}, status_code: {}".format(
#                 comment, create_comment_url, r.status_code
#             )
#         )
        if r.status_code == 200 or r.status_code == 404:
            return True
        else:
            return False
    except Exception as e:
        print("Failed to send request: " + str(e))
        return False

def write_csv(path, data_row):
    with open(path,'a+') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(data_row)

if __name__ == '__main__':
    """
    通过抓豆瓣app登录包获得的client_secret
    参考：https://bbs.125.la/thread-14226779-1-1.html
    """
    client_secret = "bf7dddc7c9cfe6f7"  # 这是不变的

    """
    通过抓豆瓣app小组首页帖子列表获得的headers和小组信息
    """
    # b2880ff9b3680de717982fed1a3829b5
    # 1160e596c2fb71463422b0c448f253d2
    authorization = "1160e596c2fb71463422b0c448f253d2"  # 每次重新登录后都要更新（与小组无关）
    headers = {
        "Authorization": "Bearer " + authorization,
        "User-Agent": "api-client/1 com.douban.frodo/6.43.0(195) Android/23 product/cancro vendor/Netease model/MuMu rom/android network/wifi platform/mobile",
        "Host": "frodo.douban.com",
        "Connection": "close",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    # os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Douban&udid=566c578109fbd3e1c1ac11d4a0f582ac118c3179"
    # os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Douban&udid=566c578109fbd3e1c1ac11d4a0f582ac118c3179
    device_info = "os_ rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Douban&udid=566c578109fbd3e1c1ac11d4a0f582ac118c3179"  # 抓包后填入相应的值

    # post需要实时更新sig和ts，不然服务器会拒绝
    comment_url_template = (
        "https://frodo.douban.com/api/v2/group/topic/{topic_id}/create_comment"
    )
    comment_content_template = (
            "text={comment}&" + device_info + "&_sig={sig}&_ts={timestamp}"
    )
    sig_code_template = (
            "POST&%2Fapi%2Fv2%2Fgroup%2Ftopic%2F{topic_id}%2Fcreate_comment&"
            + authorization
            + "&{timestamp}"
    )

    bvid = ["BV1fy4y1K75G", "BV1AK4y1u7y4"]
    cid_bvid = ["cid=367421985&bvid=BV1fy4y1K75G", "cid=367413791&bvid=BV1AK4y1u7y4"]
    s = requests.Session()
    s.headers.update(headers)
    vedio_data_list = []
    path = "bili.csv"

    while True:
        comment = ""
        for i in range(2):
            vedio_data = []
            bofang, danmu = getbufangliang(bvid[i])
            count, total = getguankanrenshu(cid_bvid[i])
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            vedio_data.append(bvid[i])
            vedio_data.append(count)
            vedio_data.append(total)
            vedio_data.append(bofang)
            vedio_data.append(danmu)
            vedio_data.append(now)
            vedio_data_list.append(vedio_data)

            write_csv(path, vedio_data)
            comment = comment + "总播放量：" + bofang + "累计弹幕数量：" + danmu + "pc端观看人数：" + count + "全平台观看人数：" + total + "\n"
            print("总播放量：", bofang, "累计弹幕数量：", danmu, "pc端观看人数：", count, "pc端观看人数：", total)

        post_comment(s, 234587140, comment)
        time.sleep(10 * 60-3)