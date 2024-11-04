# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :extract_data.py
@Author     :wooght
@Date       :2024/9/18 17:05
@Content    :提取数据
"""
import json
import pprint


class ExtractData:
    @staticmethod
    def get_headers_dict(headers_text):
        """
        从字符串中提取headers
        Parameters
        ----------
        headers_text

        Returns
        -------
        返回headers 字典
        """
        headers_list = headers_text.split('|||')
        headers_dict = {header.split('=')[0]: header.split('=', 1)[1].strip() for header in headers_list}
        return headers_dict

    @staticmethod
    def get_cookies_dict(txt):
        """
        从字符串中提取cookies(headers中cookie单独一行)
        Parameters
        ----------
        txt

        Returns
        -------

        """
        txt_list = txt.split(';')
        result_dict = {}
        for l in txt_list:
            split_list = l.split('=')
            if len(split_list) == 2:
                k, v = split_list[0], split_list[1]
            elif len(split_list) >= 3:
                k = split_list[0]
                v = '='.join(split_list[1:])
            else:
                k, v = split_list[0], ''
            result_dict[k.strip()] = v.strip()
        return result_dict

    @staticmethod
    def extract_category_params(hashmap_txt):
        """
        extract:提取    category:分类
        获取已经保存的params,并对其进行值改变,返回字典
        Parameters
        ----------
        hashmap_txt

        Returns
        -------

        """
        hashmap_txt = hashmap_txt.replace('\\', '')
        # 分成前后两部分
        data_params = hashmap_txt.replace('}"', "}")
        data_params = data_params.replace('"{', "{")
        # 转换为json
        data_json = json.loads(data_params)
        return data_json

    @staticmethod
    def get_sign_params(params_txt):
        """
        根据hook返回值,提取sign等headers核心内容
        :return:    dict
        """
        import re
        params_list = params_txt.split(',')
        result_dict = {}
        print(params_list)
        for p in params_list:
            pattern = r'([a-zA-Z0-9_\-]+)=([^,]*)'
            re_result = re.findall(pattern, p)[0]
            print(re_result[1])
            result_dict[re_result[0]] = re_result[1]
        return result_dict


if __name__ == '__main__':
    Ed = ExtractData
    str = '''{"BS":"{\"TMALL_MARKET_B2C\":\"{\\\"stores\\\":[{\\\"code\\\":\\\"112\\\",\\\"bizType\\\":\\\"REGION_TYPE_REGION\\\",\\\"addrId\\\":\\\"12204381200\\\",\\\"type\\\":\\\"CHOOSE_ADDR\\\"}]}\"}","appId":"66","apptimestamp":"1730125088","areaCode":"CN","behavior":"q:%E7%89%9B%E4%BB%94%E8%A3%A4%E8%9C%9C%E6%A1%83%E8%87%80;page_n:1;nid:843514897222,838916368838,684368721658;time_stamp:1730124961833","brand":"Xiaomi","bxFeature":"{\"TT\":1,\"data\":[[\"tb_bc_search_pcxt_rn_vstr\",\"rnIndex|rn\",\"4|25ca1c859245723d2a660efc2091b16c#5|34141d737e57730b1bd7f24c758338d7#6|d14fbc0fdd3dc723f49e117502b9545f#7|8a8c1b50d6fc98e69ef30b05460aab45\"],[\"tb_bc_search_pcxt_vstr\",\"item_id|pos|is_p4p|click|click_staytime|pv_timestamp|expCurDur|expEndDur|expEnd|price|rnIndex|click_buy|click_cart|click_fav\",\"637862156925|3|0|||1730124231019|0|299|1|185|5|||#838916368838|9|0|1|133609|1730124346737|0|710|1|89.9|5|||#843498238830|5|0|||1730124487787|20|1848|1|139|5|||#841914629729|6|0|||1730124235205|2326|||175.91|5|||#811640362049|4|1|||1730124487907|4|1347|1|89.00|5|||#844126073177|8|0|||1730124346623|1476|||185.91|5|||#843514897222|7|0|1|102258|1730124235306|1873|||132|5|||#696764507335|1|0|||1730124958823||||298|6|||#679905470444|2|0|||1730124958826||||216.91|6|||#613310120872|3|1|||1730124958830||||146.91|6|||#684368721658|0|1|1|36432|1730124958852||||139.00|6|||#734874381406|0|1|||1730125008644||||1199.00|7|||#696764507335|1|0|||1730125008647||||298|7|||#679905470444|3|0|||1730125008650||||216.91|7|||#635346453165|2|0|||1730125008653||||298|7|||\"]],\"fetchTime\":1730125088100}","canP4pVideoPlay":"true","client_os":"Android","client_os_version":"32","countryNum":"156","device":"2206122SC","editionCode":"CN","elderHome":"false","from":"input","globalLbs":"{\"biz_common\":{\"recommendedAddress\":{\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"蓝天多元智能幼儿园\",\"lat\":\"30.697662\",\"lng\":\"104.184410\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"location\"}},\"eleme\":{\"storeInfos\":[{}]},\"meeting_place\":{},\"same_city_buy\":{},\"tb_search_b2c\":{\"recommendedAddress\":{\"addressId\":\"12204381200\",\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"华实路13号 保利林语溪二期\",\"lat\":\"30.697837\",\"lng\":\"104.185644\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"deliver\"}},\"txd\":{\"storeInfos\":[{},{},{},{},{},{},{},{},{},{}]}}","goodPriceVersion":"false","gpsEnabled":"true","grayHair":"false","hasPreposeFilter":"false","homePageVersion":"v7","info":"wifi","isBeta":"false","isEnterSrpSearch":"true","n":"10","needTabs":"true","network":"wifi","newSortBar":"true","nsNative":"true","page":"1","q":"蜜桃臀牛仔裤","rainbow":"4541,4352,4195,12698740,2521,2397","schemaType":"auction","searchBoxShowType":"UOne","searchDoorFrom":"srp","searchElderHomeOpen":"false","search_action":"initiative","style":"list","sversion":"21.6","ttid":"703304@taobao_android_10.39.10","utd_id":"ZwzvF2Swb/gDAK2RdMwOnx2v","vm":"nw"}'''
    request_post_1 = '''{"LBS":"{\"TMALL_MARKET_B2C\":\"{\\\"stores\\\":[{\\\"code\\\":\\\"112\\\",\\\"bizType\\\":\\\"REGION_TYPE_REGION\\\",\\\"addrId\\\":\\\"12204381200\\\",\\\"type\\\":\\\"CHOOSE_ADDR\\\"}]}\"}","_navigation_params":"{\"needdismiss\":\"0\",\"animated\":\"0\",\"needpoptoroot\":\"0\"}","appId":"66","apptimestamp":"1730269103","areaCode":"CN","brand":"Xiaomi","bxFeature":"{\"TT\":1,\"data\":[],\"error_code\":20807,\"fetchTime\":1730269103675}","canP4pVideoPlay":"true","client_os":"Android","client_os_version":"32","countryNum":"156","device":"2206122SC","display_text":"紧身开叉裤","editionCode":"CN","elderHome":"false","from":"suggest_all-queryBE2","globalLbs":"{\"biz_common\":{\"recommendedAddress\":{\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"蓝天多元智能幼儿园\",\"lat\":\"30.697662\",\"lng\":\"104.184410\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"location\"}},\"eleme\":{\"storeInfos\":[{}]},\"meeting_place\":{},\"same_city_buy\":{},\"tb_search_b2c\":{\"recommendedAddress\":{\"addressId\":\"12204381200\",\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"华实路13号 保利林语溪二期\",\"lat\":\"30.697837\",\"lng\":\"104.185644\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"deliver\"}},\"txd\":{\"storeInfos\":[{},{},{},{},{},{},{},{},{},{}]}}","goodPriceVersion":"false","gpsEnabled":"true","grayHair":"false","hasPreposeFilter":"false","homePageVersion":"v7","index":"1","info":"wifi","isBeta":"false","isEnterSrpSearch":"true","is_multi_hintq":"false","n":"10","needTabs":"true","network":"wifi","newSortBar":"true","nsNative":"true","page":"1","pvFeature":"676692711438;725579064064;813178463025;710440100392;768631520134","q":"约会短裤","rainbow":"4541,4352,4195,12698740,2521,2397","schemaType":"auction","scm":"1007.home_topbar.searchbox.d","searchBoxShowType":"UOne","searchElderHomeOpen":"false","searchTextRT":"150","search_action":"initiative","spm":"a2141.1.searchbar.searchbox","style":"list","subtype":"text","sug_session_id":"62f79647-d76f-46be-8a54-54ad84bb8428","sugg":"约会_1_0","suggest_rn":"bucketid_16-rn_f78e4b27-bad3-40ab-b0c4-da268dc6aabc","sversion":"21.6","ttid":"703304@taobao_android_10.39.10","utd_id":"ZwzvF2Swb/gDAK2RdMwOnx2v","vm":"nw"}'''
    request_post_2 = '''{"LBS":"{\"TMALL_MARKET_B2C\":\"{\\\"stores\\\":[{\\\"code\\\":\\\"112\\\",\\\"bizType\\\":\\\"REGION_TYPE_REGION\\\",\\\"addrId\\\":\\\"12204381200\\\",\\\"type\\\":\\\"CHOOSE_ADDR\\\"}]}\"}","appId":"66","apptimestamp":"1730269877","areaCode":"CN","brand":"Xiaomi","bxFeature":"{\"TT\":1,\"data\":[[\"tb_bc_search_pcxt_rn_vstr\",\"rnIndex|rn\",\"1|5a8c5db558268b59129f4f819a997d56\"],[\"tb_bc_search_pcxt_vstr\",\"item_id|pos|is_p4p|click|click_staytime|pv_timestamp|expCurDur|expEndDur|expEnd|price|rnIndex|click_buy|click_cart|click_fav\",\"730148640721|2|0|||1730269104733||||58.01|1|||#673456889982|0|1|||1730269104735||||56.00|1|||#748338389429|3|0|||1730269104772||||168|1|||#728228038321|1|0|||1730269104777||||58.01|1|||\"]],\"fetchTime\":1730269877588}","canP4pVideoPlay":"true","client_os":"Android","client_os_version":"32","countryNum":"156","device":"2206122SC","editionCode":"CN","elderHome":"false","from":"suggest_all-queryBE2","globalLbs":"{\"biz_common\":{\"recommendedAddress\":{\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"蓝天多元智能幼儿园\",\"lat\":\"30.697662\",\"lng\":\"104.184410\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"location\"}},\"eleme\":{\"storeInfos\":[{}]},\"meeting_place\":{},\"same_city_buy\":{},\"tb_search_b2c\":{\"recommendedAddress\":{\"addressId\":\"12204381200\",\"area\":\"成华区\",\"areaDivisionCode\":\"510108\",\"city\":\"成都市\",\"cityDivisionCode\":\"510100\",\"detailText\":\"华实路13号 保利林语溪二期\",\"lat\":\"30.697837\",\"lng\":\"104.185644\",\"province\":\"四川省\",\"provinceDivisionCode\":\"510000\",\"town\":\"龙潭街道\",\"townDivisionCode\":\"510108016\",\"type\":\"deliver\"}},\"txd\":{\"storeInfos\":[{},{},{},{},{},{},{},{},{},{}]}}","goodPriceVersion":"false","gpsEnabled":"true","grayHair":"false","hasPreposeFilter":"false","homePageVersion":"v7","index":"2","info":"wifi","isBeta":"false","isEnterSrpSearch":"true","n":"10","needTabs":"true","network":"wifi","newSortBar":"true","nsNative":"true","page":"1","q":"约会短裤女","rainbow":"4541,4352,4195,12698740,2521,2397","schemaType":"auction","searchBoxShowType":"UOne","searchDoorFrom":"srp","searchElderHomeOpen":"false","search_action":"initiative","style":"list","subtype":"text","sug_session_id":"16d06a88-fe1e-4f99-a286-06ee0e6ac946","sugg":"约会短裤_3_0","suggest_rn":"bucketid_16-rn_7a0846e2-b555-4d42-b144-b3bd6fa62b57","sversion":"21.6","ttid":"703304@taobao_android_10.39.10","utd_id":"ZwzvF2Swb/gDAK2RdMwOnx2v","vm":"nw"}'''
    str_json = Ed.extract_category_params(str)
    pprint.pprint(str_json)
    print('88888888888888888888888888888888')
    pprint.pprint(Ed.extract_category_params(request_post_1))
    print('88888888888888888888888888888888')
    pprint.pprint(Ed.extract_category_params(request_post_2))