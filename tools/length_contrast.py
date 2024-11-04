# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :length_contrast.py
@Author     :wooght
@Date       :2024/9/19 15:45
@Content    :content-length 对比
"""
from common.extract_data import ExtractData as Ed

run_params = '''{"tryRequest":"false","address":"河北省 保定市 涞水县 108国道 靠近东河山村 ","globalLbs":"{\"globalAreaCode\":\"510104\",\"globalCityCode\":\"510100\",\"globalLat\":\"30.633133\",\"globalLng\":\"104.110722\",\"globalProvinceCode\":\"510000\",\"globalTownCode\":\"510104030\"}","cityCode":"130600","provinceCode":"130000","utdid":"Zs7Pnkn0r40DAKSy/CBlF7cX","latitude":"39.633542","edition":"{\"actualLanguageCode\":\"zh-CN\",\"countryId\":\"CN\",\"countryNumCode\":\"156\",\"currencyCode\":\"CNY\"}","containerParams":"{\"recommend_multi_channel\":{\"baseCacheTime\":0,\"bizParams\":{\"guessChannelId\":\"pindao_0002\",\"hundredClickItemId\":\"\",\"isComplexTexture\":false,\"isNeedSubSelectionData\":false,\"isPullRefresh\":false,\"new2021UIEnable\":true,\"tb_homepage_clientCache_lbs\":{}},\"clientReqOffsetTime\":25374,\"clientReqTime\":1726706626289,\"deltaCacheTime\":0,\"pageParams\":{\"firstRequestInAdvance\":-1,\"lastPage\":false,\"pageNum\":0,\"requestInAdvance\":10,\"virtualPageNum\":0},\"passParams\":{},\"realBaseCacheTime\":0,\"requestType\":\"pageEnter\"}}","userId":"4060247732","nick":"tb793426967","areaCode":"130623","poiRefreshTime":"1726706620","cityName":"保定","areaName":"涞水县","countryCode":"CN","countryName":"中国","provinceName":"河北省","gatewayVersion":"2.0","longitude":"115.109334","commonBizParams":"{\"deviceInfo\":\"{\\\"deviceModel\\\":\\\"phone\\\"}\"}"}'''
form_data = """{"tryRequest":"false","address":"河北省 保定市 涞水县 108国道 靠近东河山村 ","globalLbs":"{\"globalAreaCode\":\"510104\",\"globalCityCode\":\"510100\",\"globalLat\":\"30.633133\",\"globalLng\":\"104.110722\",\"globalProvinceCode\":\"510000\",\"globalTownCode\":\"510104030\"}","cityCode":"130600","provinceCode":"130000","utdid":"Zs7Pnkn0r40DAKSy/CBlF7cX","latitude":"39.633542","edition":"{\"actualLanguageCode\":\"zh-CN\",\"countryId\":\"CN\",\"countryNumCode\":\"156\",\"currencyCode\":\"CNY\"}","containerParams":"{\"recommend_multi_channel\":{\"baseCacheTime\":0,\"bizParams\":{\"guessChannelId\":\"pindao_0002\",\"hundredClickItemId\":\"\",\"isComplexTexture\":false,\"isNeedSubSelectionData\":false,\"isPullRefresh\":false,\"new2021UIEnable\":true,\"tb_homepage_clientCache_lbs\":{}},\"clientReqOffsetTime\":25374,\"clientReqTime\":1726706626289,\"deltaCacheTime\":0,\"pageParams\":{\"firstRequestInAdvance\":-1,\"lastPage\":false,\"pageNum\":0,\"requestInAdvance\":10,\"virtualPageNum\":0},\"passParams\":{},\"realBaseCacheTime\":0,\"requestType\":\"pageEnter\"}}","userId":"4060247732","nick":"tb793426967","areaCode":"130623","poiRefreshTime":"1726706620","cityName":"保定","areaName":"涞水县","countryCode":"CN","countryName":"中国","provinceName":"河北省","gatewayVersion":"2.0","longitude":"115.109334","commonBizParams":"{\"deviceInfo\":\"{\\\"deviceModel\\\":\\\"phone\\\"}\"}"}"""
content_length = 856

print(len(run_params), len(form_data))
run_params_json = Ed.extract_category_params(run_params)
print(run_params_json)

json_txt = '''{'tryRequest': 'false', 'address': '河北省 保定市 涞水县 108国道 靠近东河山村 ', 'globalLbs': {'globalAreaCode': '510104', 'globalCityCode': '510100', 'globalLat': '30.633133', 'globalLng': '104.110722', 'globalProvinceCode': '510000', 'globalTownCode': '510104030'}, 'cityCode': '130600', 'provinceCode': '130000', 'utdid': 'Zs7Pnkn0r40DAKSy/CBlF7cX', 'latitude': '39.633542', 'edition': {'actualLanguageCode': 'zh-CN', 'countryId': 'CN', 'countryNumCode': '156', 'currencyCode': 'CNY'}, 'containerParams': {'recommend_multi_channel': {'baseCacheTime': 0, 'bizParams': {'guessChannelId': 'pindao_0002', 'hundredClickItemId': '', 'isComplexTexture': False, 'isNeedSubSelectionData': False, 'isPullRefresh': False, 'new2021UIEnable': True, 'tb_homepage_clientCache_lbs': {}}, 'clientReqOffsetTime': 25374, 'clientReqTime': 1726706626289, 'deltaCacheTime': 0, 'pageParams': {'firstRequestInAdvance': -1, 'lastPage': False, 'pageNum': 0, 'requestInAdvance': 10, 'virtualPageNum': 0}, 'passParams': {}, 'realBaseCacheTime': 0, 'requestType': 'pageEnter'}}, 'userId': '4060247732', 'nick': 'tb793426967', 'areaCode': '130623', 'poiRefreshTime': '1726706620', 'cityName': '保定', 'areaName': '涞水县', 'countryCode': 'CN', 'countryName': '中国', 'provinceName': '河北省', 'gatewayVersion': '2.0', 'longitude': '115.109334', 'commonBizParams': {'deviceInfo': {'deviceModel': 'phone'}}}'''.replace(' ', '')
print(json_txt)
new_str = ''
target_char = ["'", "{", "}"]
total_char = 0
for c in json_txt:
    if c not in target_char:
        total_char += 1
        new_str += c
print(len(new_str), total_char, new_str)

