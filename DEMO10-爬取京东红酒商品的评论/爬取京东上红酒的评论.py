# 爬取京东上红酒的差评与好评

# 选取了评论数最多的红酒
import requests
import re
import json
import time



def get_json_negative_comments(page):
    '''

    :param page:差评的页码
    :return: 返回包含差评的JSON
    '''
    url = 'https://sclub.jd.com/comment/productPageComments.action?' \
          'callback=fetchJSON_comment98vv7323&productId=4905796' \
          '&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1' \
        .format(page)  # url中的productId就是商品的id

    hd = {'User-Agent': 'Mozilla/5.0'}

    try:
        r = requests.get(url, headers=hd)
        r.raise_for_status()
    except:
        print('1111')
    else:
        r.encoding = r.apparent_encoding  # 设置编码

        # 将数据改为json格式的数据
        # 利用正则表达式将不需要的数据剔除
        print(r.text)
        result = re.sub(r'fetchJSON_comment98vv7323\(', '', r.text)
        result = re.sub(r'\);', '', result)

        result = json.loads(result)  # 将字符串转换为JSON对象，由于最外层式大括号，所以最总类型式字典
        # print(result)
        # print(type(result))  # 类型
        return result


def get_json_postive_comments(page):
    '''

    :param page: 好评的页码
    :return: 返回包含好评的JSON对象
    '''
    url = 'https://sclub.jd.com/comment/productPageComments.action?' \
          'callback=fetchJSON_comment98vv7324&productId=4905796&score=0&' \
          'sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(page)
    hd = {'User-Agent': 'Mozilla/5.0'}
    print(url)
    try:
        r = requests.get(url, headers=hd)
        r.raise_for_status()
    except:
        print('1111')
    else:
        r.encoding = r.apparent_encoding  # 设置编码

        # 将数据改为json格式的数据
        # 利用正则表达式将不需要的数据剔除
        print(r.text)
        result = re.sub(r'fetchJSON_comment98vv7324\(', '', r.text)
        result = re.sub(r'\);', '', result)
        print(result)
        result = json.loads(result)  # 将字符串转换为JSON对象，由于最外层式大括号，所以最总类型式字典
        return result


def pick_up_negative_comments(json, negative_list):
    items = json['comments']  # 找到评论所在的列表
    for item in items:
        negative_list.append(item['content'])


def pick_up_positive_comments(json, postive_list):
    items = json['comments']  # 找到评论所在的列表
    for item in items:
        postive_list.append(item['content'])
    print(postive_list)


def save_postive_comments(postive_list, index):
    """保存积极的评论"""
    with open('pos{}'.format(index), 'w', encoding='utf-8') as f:
        for item in postive_list:
            f.write(item + '\n')


def save_negative_comments(negative_list, index):
    """保存消极的评论"""
    with open("neg{}".format(index), 'w', encoding='utf-8') as f:
        for item in negative_list:
            f.write(item + "\n")

if __name__ == '__main__':
    for i in range(20):
        postive_list = []
        result1 = get_json_postive_comments(i)
        pick_up_positive_comments(result1, postive_list)
        save_postive_comments(postive_list,i)
        time.sleep(1)
        negative_list = []
        result2 = get_json_negative_comments(i)
        pick_up_negative_comments(result2, negative_list)
        save_negative_comments(negative_list, i)

        time.sleep(1)

