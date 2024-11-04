# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :detail_content_convert.py
@Author     :wooght
@Date       :2024/9/26 16:26
@Content    :详情数据转换
"""
import re, json

def content_convert(txt):
    result_txt = txt.replace('\\', "")
    result_txt = re.sub(r'(\w+)\'(\w+)', r'\1\2', result_txt)  # 匹配名字之间有'的
    result_txt = result_txt.replace("'", '"')
    result_txt = result_txt.replace('"{', '{')
    result_txt = re.sub(r'([\u4e00-\u9fff]+)\}', r'\1', result_txt)  # 匹配 中文}"
    result_txt = result_txt.replace('}"', '}')

    result_txt = re.sub(r'(\[[\u4e00-\u9fff\+\-\[\]\s【】\w]{1,1000}\])', '', result_txt)  # [] 匹配中文字符串中有[]的
    result_txt = re.sub(r'(\w+)\[\d+\]', r'\1', result_txt)  # 匹配代码[]表达式

    result_txt = result_txt.replace('"[', '[')
    result_txt = result_txt.replace(']"', ']')
    result_txt = re.sub(r'([\u4e00-\u9fff\（\）]+\]),', '",', result_txt)  # 弥补上一步的错误,替换表情字符作为结束的字符串

    result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)\},', r'\1}",', result_txt)
    result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)\}\]', r'\1}"]', result_txt)
    result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)\}\}', r'\1}"}', result_txt)
    result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)"\}', r'\1}"', result_txt)
    result_txt = re.sub(r'(\$[\{a-zA-Z0-9\-\.\[\]\s\_]+)\},', r'\1}",', result_txt)  # 匹配 $单词{内容}
    result_txt = re.sub(r'(\$[\{a-zA-Z0-9\-\.\[\]\s\_]+)\}\}', r'\1}"}', result_txt)  # 匹配 $单词{内容}}
    result_txt = re.sub(r'("")([^"]*)("")', '""', result_txt)  # 连续双引号
    result_txt = re.sub(r'"[^:]+"[\u4e00-\u9fff]+"[\u4e00-\u9fff\w;\-\+]*"', '""', result_txt)  # 中文中的双引号

    result_txt = re.sub(r'<.*?>', '', result_txt)       # 替换html

    return result_txt


def core_to_json(txt):
    convert_body = content_convert(txt)
    list_body = [item for item in convert_body.split('\n')]  # 分组
    core_list = []
    for i in list_body:
        if len(i) > 1000:
            core_list.append(i.replace('data: ', ''))
    if len(core_list) < 1:
        raise ValueError('result length < 1000')
    core_content = core_list[0]
    try:
        return_json = json.loads(core_content)
        return return_json
    except json.decoder.JSONDecodeError as e:
        print(txt)
        print(core_content[e.colno-100: e.colno + 20])
        raise json.decoder.JSONDecodeError('JsonDecodeError', e.msg, e.pos)
