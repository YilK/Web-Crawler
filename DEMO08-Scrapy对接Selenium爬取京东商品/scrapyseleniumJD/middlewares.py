# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from logging import getLogger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from scrapy.http import HtmlResponse


class ScrapyseleniumjdSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyseleniumjdDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# 编辑自己的下载中间件
class SeleniumMiddleware():
    def __init__(self):
        self.logger = getLogger(__name__)
        self.browser = webdriver.Chrome()  # 声明浏览器对象
        self.browser.set_page_load_timeout(10)  # 设定页面加载设定时间
        self.wait = WebDriverWait(self.browser, 10)  # 显式等待

    def __del__(self):
        self.browser.close()  # 关闭页面

    def process_reqest(self, request, spider):  # 抓取页面
        self.logger.debug('staring !!!!!!!')
        page = request.meta.get('page')  # 获得页码
        try:
            self.browser.get(request.url)  # 访问初始页面
            for i in range(1, 3):  # 将页面拖拽到底部，页面全部加载出来，不然后面找不到其他页面的信息
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            if page > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span input.input-txt')))  # 直到节点加载出来
                button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.p-skip a')))  # 直到该节点可点击
                input.clear()  # 清除节点里内容
                input.send_keys(page)  # 输入要到达的页面
                button.click()  # 点击确定按钮
                # 判断是否是当前的页码
            self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'span.p-num a.curr'), str(page)))
            self.browser.execute_script("window.scrollBy(0, 5000)")  # 滑倒页面中部，等待2s，加载剩余的商品信息
            # self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  ，到页面的底部应该也可以没尝试
            time.sleep(2)
            # 返回Response对象，会直接将Response对象交给Spier处理
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)

        except:
            return HtmlResponse(url=request.url, status=500, request=request)
