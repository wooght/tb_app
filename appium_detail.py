# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :appium_detail.py
@Author     :wooght
@Date       :2024/10/26 21:59
@Content    :通过Appium获取detail内容
"""
from common.appium_test import AppiumTest

app = AppiumTest()

total = 40
current_index = 0
keywords = ['牛仔裤 女', '瓜子', '开心果']
for key in keywords:
    app.click_search(key)
    current_index = 1
    while current_index < total:
        if current_index % 5 == 0:
            app.driver.swipe(app.random_int(200), app.random_int(600), app.random_int(120), app.random_int(300),
                          app.random_int(3000))
        elif current_index % 2 == 0:
            app.scroll_loop(1, True)
        app.click_item(True)
        app.scroll_item()

        print(f'当前已经点击:{current_index}个')
        current_index += 1