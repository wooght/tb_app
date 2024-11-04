# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :ascii_convert.py
@Author     :wooght
@Date       :2024/9/25 16:12
@Content    :ASCII码转换   convert 转换
"""

import re

# 地址中需要转换的字符
ord_list = {'{':'%7B', '}':'%7D', '"':'%22', ':':'%3A', ',':'%2C', '\\':'%5C', '/':'%2F', '=':'%3D', '+':'%2B', '!':'%21'}

def to_up(s):
    v = s.group()
    return v.upper()

def to_low(s):
    v = s.group()
    return v.lower()

def zh_to_ascii(s):
    """
        中文转换为淘宝地址中的 ASCII
    """
    bytes_diannao = s.encode('utf-8')
    ascii_str = str(bytes_diannao).replace('\\x', '%')
    ascii_str = ascii_str.replace('\\\\', '\\')
    ascii_str = ascii_str.replace('b', '', 1)
    ascii_str = ascii_str.replace("'", '')
    for k, v in ord_list.items():
        ascii_str = ascii_str.replace(k, v)
    ascii_str = re.sub(r'%([^%]{2})', to_up, ascii_str)
    return ascii_str

def utf8_to_zh(s):
    '''
    Java UTF8 字节串 转中文
    :param s: 如:'%E7%89%9B%E4%BB%94%E8%A3%A4%E8%9C%9C%E6%A1%83%E8%87%80'
    :return:  中文
    '''
    # 转小写
    low_str = re.sub(r'%([^%]{2})', to_low, s)
    # 以%分割为list
    low_str_l = low_str.split('%')
    hex_str = ''.join(low_str_l[1:])    # 得到'e78998e4...'的hex字符串
    s_bytes = bytes.fromhex(hex_str)    # 将hex 字符串转换为字节对象 b'\xe7\x89...'
    return s_bytes.decode('utf-8')