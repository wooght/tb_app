# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :run_convert.py
@Author     :wooght
@Date       :2024/9/25 17:28
@Content    :
"""
import re, json, pprint

import dateutil.parser

with open('goods_content.txt', 'r', encoding='utf-8') as f:
    result_txt = f.read()


result_txt = result_txt.replace('\\', "")
result_txt = re.sub(r'(\w+)\'(\w+)', r'\1\2', result_txt)   # 匹配名字之间有'的
result_txt = result_txt.replace("'", '"')
result_txt = result_txt.replace('"{', '{')
result_txt = re.sub(r'([\u4e00-\u9fff]+)\}',r'\1',result_txt)      # 匹配 中文}"
result_txt = result_txt.replace('}"', '}')

result_txt = re.sub(r'(\[[\u4e00-\u9fff\+\-\[\]\s【】\w]{1,1000}\])','',result_txt)   # [] 匹配中文字符串中有[]的
result_txt = re.sub(r'(\w+)\[\d+\]', r'\1', result_txt)        # 匹配代码[]表达式

result_txt = result_txt.replace('"[', '[')
result_txt = result_txt.replace(']"', ']')
result_txt = re.sub(r'([\u4e00-\u9fff\（\）]+\]),','",',result_txt)   # 弥补上一步的错误,替换表情字符作为结束的字符串

result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)\},', r'\1}",', result_txt)
result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)\}\]',r'\1}"]', result_txt)
result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)\}\}',r'\1}"}', result_txt)
result_txt = re.sub(r'(\$\{[a-zA-Z0-9\-\.\[\]\s\_]+)"\}',r'\1}"', result_txt)
result_txt = re.sub(r'(\$[\{a-zA-Z0-9\-\.\[\]\s\_]+)\},',r'\1}",', result_txt)   # 匹配 $单词{内容}
result_txt = re.sub(r'(\$[\{a-zA-Z0-9\-\.\[\]\s\_]+)\}\}',r'\1}"}', result_txt)   # 匹配 $单词{内容}}
result_txt = re.sub(r'("")([^"]*)("")', '""', result_txt)                                   # 连续双引号
result_txt = re.sub(r'"[^:]+"[\u4e00-\u9fff]+"[\u4e00-\u9fff\w;\-\+]*"', '""', result_txt)  # 中文中的双引号

result_txt = result_txt.replace('”', "")
result_txt = result_txt.replace('“', "")

result_txt = re.sub(r'<.*?>', '', result_txt)
result_list = [item for item in result_txt.split('\n')]
content_list = []
for i in result_list:
    if len(i) > 1000:
        content_list.append(i.replace('data: ', ''))

# print(content_list[0])
json_txt = content_list[0]
try:
    core_json = json.loads(json_txt)
except json.decoder.JSONDecodeError as e:
    print(json_txt)
    print(e.colno)
    print(json_txt[e.colno - 100: e.colno+20])
    json_txt = json_txt.replace(json_txt[e.colno - 1], '')
    core_json = json.loads(json_txt)
goods_dict = {}
"""商品详情"""
print(core_json)
base_contents = core_json["data"]["props"]["groupProps"][0]["基本信息"]
base_contents_list = [key+':'+val for item in base_contents for key, val in item.items()]
goods_dict['contents'] = ';'.join(base_contents_list)
"""商品属性"""
core_item = core_json['data']['item']  # 商品Item信息
goods_dict['t_id'] = core_item['itemId']                # 商品id 列表中的t_id
goods_dict['title'] = core_item['title']
goods_dict['h5_url'] = core_item['h5ItemUrl']           # 可以直接访问的h5地址
goods_dict['category_id'] = core_item['categoryId']     # 分类id
try:
    goods_dict['brand_id'] = core_item['brandValueId']      # brand id
except Exception as e:
    goods_dict['brand_id'] = 0
images = [item for item in core_item['images']]
goods_dict['images'] = ';'.join(images)                 # 图片地址,用;连接多个
"""价格"""
try:
    price_item = core_json["data"]["apiStack"][0]["value"]["data"]["detail3Price"]
    try:
        goods_dict['sku_id'] = price_item["events"]["priceClick"][0]["fields"]["exParams"]["content"]["skuMoney"]["skuId"]
    except:
        goods_dict['sku_id'] = core_json["data"]["apiStack"][0]["value"]["global"]["data"]["skuBase"]["skus"][0]["skuId"]
    goods_dict['price'] = price_item["fields"]["price"]["priceText"]                                  # 实际折扣后价格
    try:
        goods_dict['extra_discount'] = price_item["fields"]["extraDiscount"]["infoList"][0]["text"]       # 活动/折扣名称
    except:
        # 无活动
        goods_dict['extra_discount'] = ''
    try:
        goods_dict['extra_price'] = price_item["fields"]["extraPrice"]["priceText"]                       # 活动前价格
    except Exception as e:
        goods_dict['extra_price'] = goods_dict['price']
except Exception as e:
    extra_price = core_json["data"]["apiStack"][0]["value"]["global"]["data"]["priceSectionData"]
    goods_dict['sku_id'] = core_json["data"]["apiStack"][0]["value"]["global"]["data"]["params"]["trackParams"]["hotSkuId"]
    try:
        goods_dict['price'] = extra_price["extraPrice"]['priceText']                                  # 实际折扣后价格
        goods_dict['extra_discount'] = extra_price["extraPrice"]['priceTitle']                        # 活动/折扣名称
        goods_dict['extra_price'] = int(extra_price['price']['priceMoney']) / 100  # 活动前价格
    except Exception as e:
        goods_dict['extra_discount'] = extra_price['price']['priceTitle']
        goods_dict['extra_price'] = int(extra_price['price']['priceMoney']) / 100  # 活动前价格
        goods_dict['price'] = goods_dict['extra_price']

"""服务保障"""
goods_service = core_json["data"]["apiStack"][0]["value"]["data"]["detail3Service"]["fields"]["group"]["items"][0]["values"]
print(goods_service)
goods_dict['sale_service'] = ';'.join([val for item in goods_service for key, val in item.items()]) # 多个保障用;连接
"""物流信息"""
logistic_service = core_json["data"]["apiStack"][0]["value"]["data"]["detail3LogisticService"]["fields"]
goods_dict['logistic_time'] = logistic_service['agingDesc']
goods_dict['logistic_addr'] = logistic_service['deliveryFromAddr']
goods_dict['logistic_freight'] = logistic_service['freight']
"""商家信息"""
seller = core_json['data']['seller']
goods_dict['seller_id'] = seller['userId']      # 商家用户id
goods_dict['shop_id'] = seller['shopId']        # 店铺id

pprint.pprint(goods_dict)