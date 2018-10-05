'''
首先先将热门的景点爬取下来
在去哪儿的官网点击门票，在输入栏输入中国并选择人气即可得到去哪儿推荐的人气景点
我所要做的就是将推荐的景点爬取下来
'''
import requests
from bs4 import BeautifulSoup
import time
import re
import pymysql


def get_html(url):  # 得到信息
    hd = {'User-Agent': 'Mozilla/5.0'}  # 模拟浏览器进行访问
    try:
        r = requests.get(url, headers=hd)
        r.raise_for_status()  # 抛出异常
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r.text
    except:
        print('1111')


def parse_html_1(html, area_list):  # 解析信息,使用BeautifulSoup解析库,将景区信息找到
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.select('h3.sight_item_caption a'))
    scenic_spots_tags = soup.select('h3.sight_item_caption a')  # 返回的是一个列表，存储着景区名称
    area_tags = soup.select('span.area a')  # 存储地址信息
    for i in range(len(area_tags)):
        area_list.append([scenic_spots_tags[i].string, area_tags[i].string.split('·')[0]])


def parse_html_2(html, area):  # 利用正则表达式将景区的搜索指数匹配出来，并添加到存储景区信息的列表
    match = re.search(r'"avgPv":(\d+)}', html)  # 匹配出指数
    if match:  # 如果存在
        area.append(int(match.group(1)))


def insertDatabase(list):  # 将数据存入数据库
    db = pymysql.connect(host='localhost', user='root', password='yellowkk', port=3306, db='spiders',
                         charset='utf8')
    cursor = db.cursor()  # 获得MySQL的操作游标
    sql1 = 'CREATE TABLE IF NOT EXISTS scenic_spots(scenic_area VARCHAR(255),location VARCHAR(255),heat_rate INT)'
    cursor.execute(sql1)  # 执行语句
    sql2 = 'INSERT INTO scenic_spots(scenic_area,location,heat_rate) values(%s,%s,%s)'
    for item in list:
        if len(item) == 3:
            # print(item[0],item[1],item[2])
            try:
                cursor.execute(sql2, (item[0], item[1], item[2]))
                db.commit()
            except:
                db.rollback()
    db.close()


def main():
    area_list = []  # 存储景区的信息
    for page in range(1, 10):  # 爬取前9页的人气景点
        url1 = 'http://piao.qunar.com/ticket/list.htm?keyword=中国&sort=pp&page=' + str(page)
        html = get_html(url1)
        parse_html_1(html, area_list)  # 找到景点的信息，然后将其存入area_list
        time.sleep(1)
    # 以上就找到了部分人气景点的信息
    # 接下来取找景点的搜索指数
    for area in area_list:
        # 搜狗指数
        url2 = 'http://zhishu.sogou.com/index/searchHeat?kwdNamesStr={}&timePeriodType=MONTH&dataType=SEARCH_ALL&queryType=INPUT'.format(
            area[0])
        html2 = get_html(url2)
        parse_html_2(html2, area)
        time.sleep(0.5)

    insertDatabase(area_list)


main()
