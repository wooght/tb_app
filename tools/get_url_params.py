# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :get_url_params.py
@Author     :wooght
@Date       :2024/9/9 18:39
@Content    :
"""
import json, re
import pprint
import time
from common.ascii_convert import zh_to_ascii, to_low, utf8_to_zh
def get_url_params(url):
    """
    获取get地址中的参数
    :param url:
    :return:
    """
    url_native = url.replace('\\', '')
    url_native = url_native.replace('"{', '{')
    url_native = url_native.replace('}"', '}')
    return json.loads(url_native)

def get_key_words(p):
    """
    返回参数列表, 多级按照:连接
    :param p:
    :return:
    """
    if isinstance(p, dict):
        key_words = []
        for key, value in p.items():
            if isinstance(value, dict):
                key_list = get_key_words(value)
                if isinstance(key_list, list):
                    for k in key_list:
                        key_words.append(key+':'+k)
            else:
                key_words.append(key)
        return key_words
    else:
        return None

def get_multi_dict(p, l):
    """
    获取多级(不定级)dict的值
    Parameters
    ----------
    p
    l

    Returns
    -------

    """
    if len(l)>1:
        c = p
        for k in l:
            c = c[k]
        return c
    else:
        return None

def get_params_diff(p1, p2):
    """
    参数对比,返回不同参数的key
    :param p1:
    :param p2:
    :return:
    """
    key_words = get_key_words(p1)
    key_words_p2 = get_key_words(p2)
    print('p1_key_words:', key_words, '\r\n p2_key_words:', key_words_p2)
    diff_key = {}
    for key in key_words:
        if key in key_words_p2:
            if ':' in key:
                p1_multi = get_multi_dict(p1, key.split(':'))
                p2_multi = get_multi_dict(p2, key.split(':'))
                if p1_multi != p2_multi:
                    diff_key[key] = f'p1:{key}:{p1_multi}, p2:{key}:{p2_multi}'
            else:
                if p1[key] != p2[key]:
                    diff_key[key] = f'p1:{key}:{p1[key]}, p2:{key}:{p2[key]}'
        else:
            if ':' in key:
                p1_multi = get_multi_dict(p1, key.split(':'))
                diff_key[key] = f'p1:{key}:{p1_multi}, p2:null'
            else:
                diff_key[key] = f'p1:{key}:{p1[key]}, p2:null'
    return diff_key

if __name__ == '__main__':
    post_params = '{"LBS":"{\"TMALL_MARKET_B2C\":\"{\\\"stores\\\":[{\\\"code\\\":\\\"112\\\",\\\"bizType\\\":\\\"REGION_TYPE_REGION\\\",\\\"addrId\\\":\\\"12204381200\\\",\\\"type\\\":\\\"CHOOSE_ADDR\\\"}]}\"}","appId":"66","apptimestamp":"1730125088","areaCode":"CN","behavior":"q:%E7%89%9B%E4%BB%94%E8%A3%A4%E8%9C%9C%E6%A1%83%E8%87%80;page_n:1;nid:843514897222,838916368838,684368721658;time_stamp:1730124961833","brand":"Xiaomi","bxFeature":"{\"TT\":1,\"data\":[[\"tb_bc_search_pcxt_rn_vstr\",\"rnIndex|rn\",\"4|25ca1c859245723d2a660efc2091b16c#5|34141d737e57730b1bd7f24c758338d7#6|d14fbc0fdd3dc723f49e117502b9545f#7|8a8c1b50d6fc98e69ef30b05460aab45\"],[\"tb_bc_search_pcxt_vstr\",\"item_id|pos|is_p4p|click|click_staytime|pv_timestamp|expCurDur|expEndDur|expEnd|price|rnIndex|click_buy|click_cart|click_fav\",\"637862156925|3|0|||1730124231019|0|299|1|185|5|||#838916368838|9|0|1|133609|1730124346737|0|710|1|89.9|5|||#843498238830|5|0|||1730124487787|20|1848|1|139|5|||#841914629729|6|0|||1730124235205|2326|||175.91|5|||#811640362049|4|1|||1730124487907|4|1347|1|89.00|5|||#844126073177|8|0|||1730124346623|1476|||185.91|5|||#843514897222|7|0|1|102258|1730124235306|1873|||132|5|||#696764507335|1|0|||1730124958823||||298|6|||#679905470444|2|0|||1730124958826||||216.91|6|||#613310120872|3|1|||1730124958830||||146.91|6|||#684368721658|0|1|1|36432|1730124958852||||139.00|6|||#734874381406|0|1|||1730125008644||||1199.00|7|||#696764507335|1|0|||1730125008647||||298|7|||#679905470444|3|0|||1730125008650||||216.91|7|||#635346453165|2|0|||1730125008653||||298|7|||\"]],\"fetchTime\":1730125088100}","canP4pVideoPlay":"true","client_os":"Android","client_os_version":"32","countryNum":"156","device":"2206122SC","editionCode":"CN","elderHome":"false","from":"input","globalLbs":"{\"biz_common\":{\"recommendedAddress\":{\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"蓝天多元智能幼儿园\",\"lat\":\"30.697662\",\"lng\":\"104.184410\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"location\"}},\"eleme\":{\"storeInfos\":[{}]},\"meeting_place\":{},\"same_city_buy\":{},\"tb_search_b2c\":{\"recommendedAddress\":{\"addressId\":\"12204381200\",\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"华实路13号 保利林语溪二期\",\"lat\":\"30.697837\",\"lng\":\"104.185644\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"deliver\"}},\"txd\":{\"storeInfos\":[{},{},{},{},{},{},{},{},{},{}]}}","goodPriceVersion":"false","gpsEnabled":"true","grayHair":"false","hasPreposeFilter":"false","homePageVersion":"v7","info":"wifi","isBeta":"false","isEnterSrpSearch":"true","n":"10","needTabs":"true","network":"wifi","newSortBar":"true","nsNative":"true","page":"1","q":"蜜桃臀牛仔裤","rainbow":"4541,4352,4195,12698740,2521,2397","schemaType":"auction","searchBoxShowType":"UOne","searchDoorFrom":"srp","searchElderHomeOpen":"false","search_action":"initiative","style":"list","sversion":"21.6","ttid":"703304@taobao_android_10.39.10","utd_id":"ZwzvF2Swb/gDAK2RdMwOnx2v","vm":"nw"}'
    post_params_json = get_url_params(post_params)
    print(post_params_json)
    key_words = get_key_words(post_params_json)
    print(key_words)
    zh_str = zh_to_ascii('蜜桃臀牛仔裤')
    hex_str = '蜜桃臀牛仔裤'.encode('utf-8')
    print('python hex:', hex_str)
    print(hex_str.decode('utf-8'))
    print(zh_str)
    print('给定中文转ASCII:', hex(ord('牛')))

    b = '%E7%89%9B%E4%BB%94%E8%A3%A4%E8%9C%9C%E6%A1%83%E8%87%80'
    print('params 编码是:', utf8_to_zh(b))

    b = '%E7%BA%A6%E4%BC%9A%E7%9F%AD%E8%A3%A4%E5%A5%B3'
    print(utf8_to_zh(b))


"""
列表 POST params, 变动:
{'containerParams:recommend_multi_channel:bizParams:firstPagePVID': 'p1:containerParams:recommend_multi_channel:bizParams:firstPagePVID:875dbbe3-2ac8-4eea-a7dc-960ef7710b3c, '
                                                                    'p2:containerParams:recommend_multi_channel:bizParams:firstPagePVID:deea930a-8d01-45a3-96ce-1819b06e1089',
 'containerParams:recommend_multi_channel:bizParams:guessChannelId': 'p1:containerParams:recommend_multi_channel:bizParams:guessChannelId:pindao_0010, '
                                                                     'p2:containerParams:recommend_multi_channel:bizParams:guessChannelId:pindao_0008',
 'containerParams:recommend_multi_channel:bizParams:latestHundredItem': 'p1:containerParams:recommend_multi_channel:bizParams:latestHundredItem:748705192025,828299970553,740193346984,670449884255,740166530682,796581996069,753262919589,692129574832,825182499349,745029309206,762909608692,805217920056, '
                                                                        'p2:containerParams:recommend_multi_channel:bizParams:latestHundredItem:808711172277,773214057940,769217836368,685172306683,727696669373,808685763734,816682770580,816171906360,756685857020,779890098171,632268542224,784379401632',
 'containerParams:recommend_multi_channel:passParams:firstPagePVID': 'p1:containerParams:recommend_multi_channel:passParams:firstPagePVID:875dbbe3-2ac8-4eea-a7dc-960ef7710b3c, '
                                                                     'p2:containerParams:recommend_multi_channel:passParams:firstPagePVID:deea930a-8d01-45a3-96ce-1819b06e1089'}

url params :
{'detail_v': '3.3.2',                                   # 固定
 'exParams': {'appReqFrom': 'detail',                   # 固定
              'container_type': 'xdetail',              # 固定
              'countryCode': 'CN',                      # 固定
              'cpuCore': '4',                           # 可以固定
              'cpuMaxHz': 'null',                       # 固定
              'deviceLevel': 'medium',                  # ....
              'dinamic_v3': 'true',
              'dynamicJsonData': 'true',
              'finalUltron': 'true',
              'id': '706070532779',                     # id 
              'industryMainPicDegrade': 'false',
              'isPadDevice': 'false',
              'item_id': '706070532779',
              'itemid': '706070532779',
              'latitude': '39.633542',
              'liveAutoPlay': 'true',
              'locate': 'guessitem-item',
              'longitude': '115.109334',
              'newStruct': 'true',
              'nick': 'tb793426967',
              'openFrom': 'pagedetail',
              'originalHost': 'item.taobao.com',
              'osVersion': '32',
              'phoneType': '2206122SC',
              'prefetchImg': '//img.alicdn.com/bao/uploaded/i1/1745959548/O1CN012CoWRC2KP2SB52o4m_!!1745959548.jpg',
              'prefetchImgRatio': '1:1',
              'preload_v': 'industry',
              'pvid': 'ba60f752-4658-4e5e-8b95-6d9f57ef7ed4',
              'rmdChannelCode': 'guessULike',
              'scm': '1007.52183.392693.0002',
              'screenHeight': '1280',
              'screenWidth': '720',
              'skuId': '5044312052943',
              'skuPriceType': '1',
              'soVersion': '2.0',
              'spm': 'a2141.1.guessitemtab_null.5',
              'spm-cnt': 'a2141.7631564',
              'supportIndustryMainPic': 'true',
              'ultron2': 'true',
              'utdid': 'Zs7Pnkn0r40DAKSy/CBlF7cX',
              'videoAutoPlay': 'true'},
 'id': '706070532779'}


category api 调用ryw.mo140317a(HaspMap,HaspMap, String, String, bool) 参数:
hashMap={
    data={
        "tryRequest":"false",
        "address":"河北省保定市涞水县其中口乡108国道",
        "globalLbs":{
            "globalAreaCode":"510104",
            "globalCityCode":"510100",
            "globalLat":"30.633133",
            "globalLng":"104.110722",
            "globalProvinceCode":"510000",
            "globalTownCode":"510104030"}",
            "cityCode":"130600",
            "provinceCode":"130000",
            "utdid":"Zs7Pnkn0r40DAKSy/CBlF7cX",
            "latitude":"39.633542",
            "edition":{
                "actualLanguageCode":"zh-CN",
                "countryId":"CN",
                "countryNumCode":"156",
                "currencyCode":"CNY"
            },
            "containerParams":{
                "recommend_multi_channel":
                    {
                    "baseCacheTime":0,
                    "bizParams":{
                        "deviceLevel":"m",
                        "guessChannelId":"pindao_0008",
                        "hundredClickItemId":"702470611817,827985722911,645304625379,820296944836",
                        "isComplexTexture":false,
                        "isNeedSubSelectionData":false,
                        "isPullRefresh":false,
                        "new2021UIEnable":true,
                        "tb_homepage_clientCache_lbs":{}
                    },
                    "clientReqOffsetTime":0,
                    "clientReqTime":1726055567957,
                    "deltaCacheTime":0,
                    "pageParams":{
                        "firstRequestInAdvance":-1,
                        "lastPage":false,
                        "pageNum":0,
                        "requestInAdvance":10,
                        "virtualPageNum":0
                    },
                    "passParams":{},
                    "realBaseCacheTime":0,
                    "requestType":"pageEnter"
                }
            },
            "userId":"4060247732",
            "nick":"tb793426967",
            "areaCode":"130623",
            "poiRefreshTime":"1726049172",
            "cityName":"保定",
            "areaName":"涞水县",
            "countryCode":"CN",
            "countryName":"中国",
            "provinceName":"河北省",
            "gatewayVersion":"2.0",
            "longitude":"115.109334",
            "commonBizParams":{
                "deviceInfo":{
                    "deviceModel":"phone"
                }
            }
        }, 
        deviceId=AqG65eu5Gpa1TRU6pBy5oeIvE-NbacZRFaSYUrt0qtBF, 
        sid=25601ccd9fad1321ce4f2a5cebbd86dd, 
        uid=4060247732, 
        x-features=27, 
        appKey=21646297, 
        api=mtop.taobao.wireless.home.category, 
        lat=39.633542, 
        lng=115.109334, 
        mtopBusiness=true, 
        utdid=Zs7Pnkn0r40DAKSy/CBlF7cX, 
        extdata=openappkey=DEFAULT_AUTH, 
        ttid=703304@taobao_android_10.39.10, 
        t=1726055567, 
        v=1.0
    }, hashMap2={pageId=http://m.taobao.com/index.htm, pageName=com.taobao.tao.welcome.Welcome}, str=21646297, str2=null, z=false, str3=r_134
"""