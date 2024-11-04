# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :time_convert_tools.py
@Author     :wooght
@Date       :2024/10/26 14:07
@Content    :时间转换 手动输入时间戳然后转换为datetime
"""
import time, sys

while True:
    time_stamp = int(input('时间戳:'))
    if time_stamp > 100000:
        print('Datetime:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp)))