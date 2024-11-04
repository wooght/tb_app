# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :appium_test.py
@Author     :wooght
@Date       :2024/10/5 21:26
@Content    :
"""
import selenium.webdriver.common.devtools.v85.network
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
import time, random

class AppiumTest:
    APPIUM_PORT = 4723          # appium 端口
    APPIUM_HOST = '127.0.0.1'   # appium 地址
    driver = object             # driver

    top_nav = []                # 顶部导航列表
    current_nav = 0             # 当前导航位置
    frame = []                  # 列表元素
    click_item_nums = 0         # item点击次数


    def set_driver(self):
        """
            设置driver, 开启noReset
        Returns
        -------

        """
        option = UiAutomator2Options()
        option.load_capabilities({
            "platformName": "Android",                              # 系统名称
            "appium:platformVersion": "12",                         # 系统版本
            "appium:deviceName": "127.0.0.1:16384",                 # 虚拟机地址
            # "appium:appPackage": "com.ss.android.article.news",     # package
            # "appium:appActivity": "com.ss.android.article.news.activity.MainActivity",  # activity
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True,
            "noReset": True,                                        # 不清理数据
            "autoGrantPermissions": True                            # 自动授权
        })
        self.driver = webdriver.Remote(f'http://{self.APPIUM_HOST}:{self.APPIUM_PORT}/wd/hub', options=option)
        self.action = ActionChains(self.driver)

    def __init__(self):
        self.set_driver()

    def get_nav(self):
        """
            获取头部导航元素,只保留能点击的导航
        Returns
        -------

        """
        # 获取顶部导航元素
        multi_tab = self.driver.find_element(AppiumBy.ID, 'com.taobao.taobao:id/multi_tab_container')
        action_bar = multi_tab.find_elements(AppiumBy.CLASS_NAME, 'android.support.v7.app.ActionBar$b')
        top_nav = []
        not_allow = ['推荐', '小时达', '关注', '双11']
        for item in action_bar:
            try:
                # 是否能找到/显示
                current_bar = item.find_element(AppiumBy.CLASS_NAME, 'android.widget.TextView').text
                print(current_bar)
                if current_bar not in not_allow:
                    top_nav.append(item)
            except Exception as e:
                print(e)

        self.top_nav = top_nav

    def click_nav(self):
        """
            点击头部导航
        Returns
        -------

        """
        self.get_nav()                                  # 获取导航栏内容
        len_nav = len(self.top_nav)
        choose_nums = random.choice(range(0, len_nav))  # 随机选择一栏导航
        print('choose:', choose_nums)
        self.top_nav[choose_nums].click()               # 点击导航
        self.random_sleep()
        # 往上滑动,触发刷新
        self.driver.swipe(100, 200, random.randint(100, 200), random.randint(300, 400), self.random_int(1200))
        self.random_sleep()


    def get_frame(self, is_search=False):
        """
            获取商品列表框架
        Returns
        -------

        """
        if is_search:
            frame_layout = self.driver.find_elements(AppiumBy.XPATH, '//android.support.v7.widget.RecyclerView/android.widget.FrameLayout')
        else:
            # 获取商品列表
            frame_layout = self.driver.find_elements(AppiumBy.XPATH,
                                                 '//android.widget.FrameLayout[@resource-id="com.taobao.taobao:id/rv_main_container_wrapper"]/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.support.v4.view.ViewPager/android.widget.FrameLayout/android.support.v7.widget.RecyclerView/android.widget.FrameLayout')

        max_frame = len(frame_layout)
        self.frame = frame_layout

    def click_item(self, is_search=False):
        """
            点击商品
        Returns
        -------

        """
        self.get_frame(is_search)
        if len(self.frame) <= 1:
            print('frame 为空')
            return False
        choice_nums = random.randint(1 if is_search else 0, len(self.frame) - 1)
        choice_item = self.frame[choice_nums]
        choice_view = choice_item.find_elements(AppiumBy.CLASS_NAME, 'android.view.View')
        # if len(choice_view) < 32:
        #     print(choice_nums, len(choice_view), '个')
        #     self.w3c_move()
        #     self.click_item(is_search)
        # else:
        print(f'点击第:{choice_nums}个')
        try:
            self.frame[choice_nums].click()
        except Exception as e:
            print(e)
            self.click_item(is_search)
        self.random_sleep()

    def scroll_item(self):
        # 每三次停留20秒
        if self.click_item_nums % 3 == 0:
            time.sleep(self.random_int(10))
        # 向下移动
        self.w3c_move()
        self.random_sleep()
        # 向下移动
        self.driver.swipe(self.random_int(200), self.random_int(600), self.random_int(120), self.random_int(300),
                          self.random_int(400))
        self.random_sleep()
        # 点击评价按钮
        try:
            pj = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="评价"]')
            pj.click()
        except Exception as e:
            print('点击评价失败')
            # 向上移动
            self.driver.swipe(self.random_int(200), self.random_int(600), self.random_int(120), self.random_int(100))
            self.click_back()
            return False

        # 随机向上滚动一次
        if random.randint(0, 5) % 2 == 0:
            self.driver.swipe(self.random_int(200), self.random_int(600), self.random_int(120), self.random_int(100))
            self.random_sleep()
        # 向下移动
        self.w3c_move()
        # 向上滑动
        self.w3c_move(True)
        time.sleep(1)
        self.w3c_move(True)
        self.click_back()
        self.random_sleep()
        self.click_item_nums += 1

    def click_back(self):
        try:
            self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="返回，按钮"]').click()
        except Exception as e:
            print(e)
            try:
                self.driver.find_element(AppiumBy.ID, 'com.taobao.taobao:id/nav_back').click()
            except Exception as e:
                print(e)
                try:
                    self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text=""]').click()
                except Exception as e:
                    print(e)

    def click_search(self, key_words):
        """
        搜索操作
        :param key_words:
        :return:
        """
        search_box = self.driver.find_element(AppiumBy.XPATH, '//android.view.View[@content-desc="搜索栏"]')
        search_box.click()
        # 重新定位搜索框
        time.sleep(0.8)
        search_box = self.driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.taobao.taobao:id/searchEdit"]')
        search_box.send_keys(key_words)
        time.sleep(1.2)
        # 定位第一个提示框
        first_text_view = self.driver.find_element(AppiumBy.XPATH, '(//android.widget.FrameLayout[@resource-id="com.taobao.taobao:id/dynamic_container"])[2]/android.view.ViewGroup/android.view.View[3]')
        first_text_view.click()

    def scroll_loop(self, direction=1, is_search=False):
        """
        滑动
        Parameters
        ----------
        direction

        Returns
        -------

        """
        self.w3c_move()
        # self.get_frame(is_search)
        # max_frame = len(self.frame) - 1
        # # 选择商品块进行滑动
        # if direction < 0:
        #     self.driver.scroll(self.frame[0], self.frame[max_frame])
        # else:
        #     self.driver.scroll(self.frame[max_frame], self.frame[0], self.random_int(800))     # duration 持续时间\
        # 按压进行滑动
        # self.w3c_move()
        # self.driver.swipe(self.random_int(300), self.random_int(400), self.random_int(300), self.random_int(400), self.random_int(1200))
        self.random_sleep()

    def w3c_move(self, is_up=False):
        """
            基于w3c的操作
            模拟按压, 滑动,释放
        Returns
        -------

        """
        start_y = self.random_int(200) if is_up else self.random_int(700)
        end_y = self.random_int(700) if is_up else self.random_int(200)
        self.action.w3c_actions.pointer_action.move_to_location(self.random_int(300), start_y)
        self.action.w3c_actions.pointer_action.click_and_hold()                     # 按压
        # self.action.w3c_actions.pointer_action.pause(1)    # 等待 单位秒
        self.action.w3c_actions.pointer_action.move_to_location(self.random_int(300), end_y)
        self.action.w3c_actions.pointer_action.pause(1)    # 等待 单位秒
        self.action.w3c_actions.pointer_action.release()                            # 释放
        self.action.perform()                                                       # 执行动作

    def get_cookie(self):
        print('cookies:')
        cookies = selenium.webdriver.common.devtools.v85.network.get_cookies()
        for cookie in cookies:
            print(cookie)

    def random_sleep(self):
        time.sleep(random.randint(1, 5))

    def random_int(self, point):
        return random.randint(int(point*0.8), int(point * 1.2))

if __name__ == '__main__':
    app = AppiumTest()
    app.get_frame(True)
    # i = 1
    # while i < 10:
    #     print(i)
    #     if i % 3 == 0:
    #         app.click_nav()
    #         time.sleep(2)
    #         app.scroll_loop()
    #     elif i % 2 == 0:
    #         app.click_item()
    #     else:
    #         app.scroll_loop()
    #     app.random_sleep()
    #     i += 1













