# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :get_cookie.py
@Author     :wooght
@Date       :2024/9/13 17:31
@Content    :分析request cookie
"""

import json

def get_txt(names):
    result_txt = []
    for name in names:
        with open(f'save_http/{name}.txt') as f:
            result_txt.append(f.read())
    return result_txt

def txt_to_dict(txt):
    txt_list = txt.split(';')
    result_dict = {}
    for l in txt_list:
        split_list = l.split('=')
        if len(split_list) > 1:
            k, v = split_list[0], split_list[1]
        else:
            k, v = split_list[0], None
        result_dict[k.strip()] = v.strip()
    return result_dict

def get_diff_single_dict(d1, d2):
    """
    获取单层dict的不同
    :param d:
    :return:
    """
    d2_keys = list(d2.keys())
    diff_dict = {}
    for key, val in d1.items():
        if key in d2_keys:
            if val != d2[key]:
                diff_dict[key] = f'd1:{val}, d2:{d2[key]}'
            else:
                pass
                # diff_dict[key] = 'same'
            k = d2_keys.index(key)
            del d2_keys[k]
        else:
            diff_dict[key] = f'd1:{val}:d2:null'
    for key in d2_keys:
        diff_dict[key] = f'd1:null, d2:{d2[key]}'
    return diff_dict


c1, c2 = get_txt(['cookie1', 'cookie2'])
cookie1 = txt_to_dict(c1)
cookie2 = txt_to_dict(c2)
print(cookie1)
diff_dict = get_diff_single_dict(cookie1, cookie2)
print(diff_dict)

print('*'*50)
for key, val in cookie1.items():
    print(key, ':', val)