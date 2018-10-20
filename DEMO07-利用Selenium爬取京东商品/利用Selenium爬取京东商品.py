# 使用Selenium爬取京东商品
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scrapy import Selector
import pymongo


browser = webdriver.Chrome()  # 声明浏览器对象
wait = WebDriverWait(browser, 10)  # 显式等待，指定最长等待时间为10s
KEYWORD = 'iphone'  # 要搜索的关键字


def index_page(page):  # 爬取指定页
    url = 'https://search.jd.com/Search?keyword=' + KEYWORD
    print('正在爬取第 {} 页'.format(page))
    try:
        browser.get(url)  # 请求网页
        for i in range(1, 3):  # 将页面拖拽到底部，页面全部加载出来，不然后面找不到其他页面的信息
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span input.input-txt')))  # 直到节点加载出来
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.p-skip a')))  # 直到该节点可点击
            input.clear()  # 清除节点里内容
            input.send_keys(page)  # 输入要到达的页面
            button.click()  # 点击确定按钮
        # 判断是否是当前的页码
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.p-num a.curr'), str(page)))
        browser.execute_script("window.scrollBy(0, 5000)")  # 滑倒页面中部，等待2s，加载信息
        time.sleep(2)

        get_products()
    except:
        print('wrong')


def get_products():  # 提取商品的信息
    html = browser.page_source  # 获取页面的源代码
    selector = Selector(text=html)  # 使用Scrapy提供的Selector来解析
    items = selector.css('li.gl-item')
    for item in items:
        product = {
            'img_url': item.css('a[target="_blank"] img').extract_first(),
            'title': item.css('div.p-name a::attr(title)').extract_first(),
            'price': item.css('div div.p-price strong i::text').extract_first(),
            'shop': item.css('div.p-shop span a::attr(title)').extract_first()

        }
        print(product)
        save_to_mongo(product)  # 存入数据库


def save_to_mongo(product):  # 存入数据库
    try:
        collection.insert(product)
    except:
        print('2222')


if __name__ == '__main__':
    # 连接到到MongoDB
    MONGO_URL = 'localhost'
    MONGO_DB = 'test'
    MONGO_COLLECTION = 'JDproducts'
    client = pymongo.MongoClient(host=MONGO_URL)  # 连接到MongoDB
    db = client[MONGO_DB]  # 指定数据库
    collection = db[MONGO_COLLECTION]  # 指定集合

    for i in range(1, 10):  # 爬取1-9页
        index_page(i)
        # index_page(3)
        time.sleep(1)
