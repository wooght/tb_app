# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :get_request_headers.py
@Author     :wooght
@Date       :2024/9/9 19:27
@Content    :
"""
import pprint
from get_url_params import get_params_diff
import re

headers_text = """x-sgext: JBP5jfBIBGdY8CByizXt%2Bo3Ivcm%2Bza7BucG%2F2rzKutquyLrLuMG7zrzBvNq9z7qfucm%2Fye6btZu4zLmdrsi%2Bzq7Orsm92r3Jvc6uyq7IrsiuyK7Krsquy67Jrsu82r7avdq92r3avdq92r3avdqunK7Jrsmun7qd65q42r3Jvcm92r3auMC52r3arsiuyK7Krsmug86X3Nq92q3Zus%2Bt2a3JrsnSuOqM7Lv6uMm4z8HMsfq4sKa5pr%2Ffus%2BryKvJq86%2F376cq8ro373fvMmryL3fvMmryavItcy9zLjf%2BJP%2Bprimvd%2B937vP6Zzpyr2fq8mryavJq8mryujf66a7przfv9%2B%2B37jftN%2Fu3%2BnfvMjSztLNv9S8ybXUu9S91L3UvdS91LzUvdS81LzIvKbspr%2FfuN%2B9pu%2BmucCgyKDIuMmgyNKa0sigy7zUvtS91OzI752gm7XUuM6gz%2Bim6abYr8Or28jDq9jIyMTSn9LLoMmgy7TM0si9pty%2B2aPulP%2BR5bTM1rm4zLGiuMa756O9vcqA%2BrjMuMy4zLjMuMeM45jlyL2rz83nvNya35b%2Fku%2BV7pTPzcu46L36ssmOzLjMuMC4zLLXvcihwLjSyLymvd%2B917TOtcu6yqvKtN%2B8377Pq8y137nJq8mryLXfvMq737TMq8i%2FprzL0sugy7zUvMm9ydLIvqbMqua4%2BbjM0sy9%2BrjMuMyAzLvmuOyozKDMusi40si7pr2mvM7SyKDIoMugy7rUvMC71L3Uv9S5yqDNu9S%2FwNI%3D
x-social-attr: 3
x-sign: azYBCM006xAAK8b0SXon17aahxoOa8b7zwc6HaFlCdKW2zbvXR91M8%2B6htLbr8saD6ksCp9gwsm9QeK%2FZbHy959HkGJW%2B8b7xkvG%2B8
x-sid: 25601ccd9fad1321ce4f2a5cebbd86dd
x-uid: 4060247732
x-nettype: WIFI
Accept-Encoding: zstd, gzip
x-pv: 6.3
x-nq: WIFI
x-region-channel: CN
x-features: 27
x-app-edition: ST
x-app-conf-v: 0
x-mini-wua: aiwSHTYZm6vbW%2BG2ULbOc1R%2FDl%2Br9pkzvNoQdUwHb1JpJnvfbtoAxKf90tIU1oGxaMPeG1P%2F0FeClHJamPgfP1n1CMr0y1Ye2DN42yfYesA6ctnHJ5Vh5iYiLP40s0it5laV88WyxLhBK%2FVCSf61%2BrX6tRf7lt8zIB33oIwnjnx%2FmccjqXUT2ewMm0QWZpDufGng%3D
content-type: application/x-www-form-urlencoded;charset=UTF-8
cache-control: no-cache
x-t: 1725879059
x-bx-version: 6.6.240704
f-refer: mtop
x-extdata: openappkey%3DDEFAULT_AUTH
x-ttid: 703304%40taobao_android_10.39.10
x-app-ver: 10.39.10
x-c-traceid: 04C61g3Z
x-location: 115.109334%2C39.633542
a-orange-dq: appKey=21646297&appVersion=10.39.10&clientAppIndexVersion=1120240909183902431
x-accept-stream: true
x-regid: reg0pnFeVn0umJbetWmmuBkv0BEL1rHS
x-umt: Ag8BSb5LPICUFAKR1UDeHJUurxWZsEMn
x-utdid: Zs7Pnkn0r40DAKSy%2FCBlF7cX
c-launch-info: 2,0,1725879059280,1725867180520,2
x-appkey: 21646297
x-falco-id: 04C61g3Z
x-page-url: http%3A%2F%2Fm.taobao.com%2Findex.htm
x-page-name: com.taobao.tao.welcome.Welcome
x-devid: AqG65eu5Gpa1TRU6pBy5oeIvE-NbacZRFaSYUrt0qtBF
user-agent: MTOPSDK%2F3.1.1.7+%28Android%3B12%3BXiaomi%3B2206122SC%29+DeviceType%28Phone%29
Host: trade-acs.m.taobao.com
Connection: Keep-Alive"""

headers_text_2 = """x-sgext: JBN6kO3LGeRFcz3xlrbweZBLoEqjTrNCpEKiWaFOolmzS6dIpUKmTaFCoVmgTKccpEqiSvMYqBilT6Qes0ukSLNNs0qgWaBKoE2zSbNLs0uzS7NJs0mzSLNKs0ijWaNZoFmgWaBZoFmgWaBZoFmzH7NKs0qzHKce9hmlWaBKoEqgWaBZpUOkWaBZs0uzS7NJs0qzANMUwVmgWbBapxuwWrBKs0rPO%2FcP9TLBO9Q70kLRMuc7rSWkJaJcp0y2S7ZLqEK2TadcpEm2TqNcoFyhSrZLoFyhSrZKtkuoT6BPpVzlEOMlpSWgXKBcpkz0H%2FROqU22SrZKtkq2SrZOo1z2JaYloVyiXKNcpVypXPNc9FyhS89Nz06lV6FLo1emV6BXoFegV6BXoVegV6FXp0nPG89Itk%2B2Ss8Yz06pV6FXoU%2BgV6El8yWhV6JJvUm9Sr1LoEmlV%2FIYvU%2F1V6Yfzx7PL8Y0wiyhNMIvoT%2BtJfYlolegV6JDpSWhSs880RvaGf0I%2BBLdO79O0TvYVdEx0hDKStQ96Q3RO9E70TvRO9Ew5RTxEqFKwjikENUr8yj%2FCPsY%2FBn9OKQ80R%2FUDds%2B5zvRO9E30TvbI8UZ9TvRJaFLz0q2Sr5DpEKmQqVcpEq2S7ZJp1ylQ7ZOoVygXKFCtkukS7ZLoEq2S6MloUjPSL1Io1ehSqBKz0ujJdEp%2BzvkO9FR0T7nO9E70QPROPs78SvRI9E51TvPS6YloCWhTc9LvUu9SL1IqFehQ6dXoFeiV6ROvU6nV6JDzw%3D%3D
x-social-attr: 3
x-sign: azYBCM006xAAJAM9zZ7dnlevN38L1AM0Csj%2F0mSqzB1TFPMgmNCw%2FAp1Qx0eYA7VymbpxVqvBwZ4jidwoH43OFqIVa3zNAM0A%2FQDNA
x-sid: 25601ccd9fad1321ce4f2a5cebbd86dd
x-uid: 4060247732
x-nettype: WIFI
Accept-Encoding: zstd, gzip
x-pv: 6.3
x-nq: WIFI
x-region-channel: CN
x-features: 27
x-app-edition: ST
x-app-conf-v: 0
x-mini-wua: aigRhMvKJnuqb4W8kXxlNdYNZ9AxZ1vQa2PA%2BDuJdoc1iir08wH3ww%2FY3g8owvED%2BCzY4PJh5Kl8%2BWq2he0DzLl%2FyJWpLzjUHvkbB5EIe%2Fl7hQ5TgSMBfpVNJ5p0OMO5XOoD3KsMq1iJdKipLLN%2Btr7jKw78nJV8WXpURAFZBAAA7e34EvEiBI4vT8Kx7RV4iI9E%3D
content-type: application/x-www-form-urlencoded;charset=UTF-8
cache-control: no-cache
x-t: 1725879447
x-bx-version: 6.6.240704
f-refer: mtop
x-extdata: openappkey%3DDEFAULT_AUTH
x-ttid: 703304%40taobao_android_10.39.10
x-app-ver: 10.39.10
x-c-traceid: 04C812k2E
x-location: 115.109334%2C39.633542
a-orange-dq: appKey=21646297&appVersion=10.39.10&clientAppIndexVersion=1120240909185301901
x-accept-stream: true
x-regid: reg0pnFeVn0umJbetWmmuBkv0BEL1rHS
x-umt: Ag8BSb5LPICUFAKR1UDeHJUurxWZsEMn
x-utdid: Zs7Pnkn0r40DAKSy%2FCBlF7cX
c-launch-info: 2,0,1725879447342,1725867180520,2
x-appkey: 21646297
x-falco-id: 04C812k2E
x-page-url: http%3A%2F%2Fm.taobao.com%2Findex.htm
x-page-name: com.taobao.tao.welcome.Welcome
x-devid: AqG65eu5Gpa1TRU6pBy5oeIvE-NbacZRFaSYUrt0qtBF
user-agent: MTOPSDK%2F3.1.1.7+%28Android%3B12%3BXiaomi%3B2206122SC%29+DeviceType%28Phone%29
Host: trade-acs.m.taobao.com
Connection: Keep-Alive"""

def get_headers_dict(headers_text):
    headers_list = headers_text.split('\n')
    headers_dict = {header.split(': ')[0]:header.split(': ')[1] for header in headers_list}
    return headers_dict

def ascii_to_str(s):
    """
    替换地址中的ASCII码
    :param s:
    :return:
    """
    ascii_pattern = re.compile(r"(%[^%]{2})")
    ascii_result = re.findall(ascii_pattern, s)
    for item in ascii_result:
        ascii_str = chr(int(item[1:], 16))
        s = s.replace(item, ascii_str)
    return s

headers_1 = get_headers_dict(headers_text)
headers_2 = get_headers_dict(headers_text_2)
pprint.pprint(headers_1)
diff_headers = get_params_diff(headers_1, headers_2)
pprint.pprint(diff_headers)

mini_wua = '''aiwSHTYZm6vbW%2BG2ULbOc1R%2FDl%2Br9pkzvNoQdUwHb1JpJnvfbtoAxKf90tIU1oGxaMPeG1P%2F0FeClHJamPgfP1n1CMr0y1Ye2DN42yfYesA6ctnHJ5Vh5iYiLP40s0it5laV88WyxLhBK%2FVCSf61%2BrX6tRf7lt8zIB33oIwnjnx%2FmccjqXUT2ewMm0QWZpDufGng%3D'''
print(ascii_to_str(mini_wua))
sgext = '''JBN6kO3LGeRFcz3xlrbweZBLoEqjTrNCpEKiWaFOolmzS6dIpUKmTaFCoVmgTKccpEqiSvMYqBilT6Qes0ukSLNNs0qgWaBKoE2zSbNLs0uzS7NJs0mzSLNKs0ijWaNZoFmgWaBZoFmgWaBZoFmzH7NKs0qzHKce9hmlWaBKoEqgWaBZpUOkWaBZs0uzS7NJs0qzANMUwVmgWbBapxuwWrBKs0rPO%2FcP9TLBO9Q70kLRMuc7rSWkJaJcp0y2S7ZLqEK2TadcpEm2TqNcoFyhSrZLoFyhSrZKtkuoT6BPpVzlEOMlpSWgXKBcpkz0H%2FROqU22SrZKtkq2SrZOo1z2JaYloVyiXKNcpVypXPNc9FyhS89Nz06lV6FLo1emV6BXoFegV6BXoVegV6FXp0nPG89Itk%2B2Ss8Yz06pV6FXoU%2BgV6El8yWhV6JJvUm9Sr1LoEmlV%2FIYvU%2F1V6Yfzx7PL8Y0wiyhNMIvoT%2BtJfYlolegV6JDpSWhSs880RvaGf0I%2BBLdO79O0TvYVdEx0hDKStQ96Q3RO9E70TvRO9Ew5RTxEqFKwjikENUr8yj%2FCPsY%2FBn9OKQ80R%2FUDds%2B5zvRO9E30TvbI8UZ9TvRJaFLz0q2Sr5DpEKmQqVcpEq2S7ZJp1ylQ7ZOoVygXKFCtkukS7ZLoEq2S6MloUjPSL1Io1ehSqBKz0ujJdEp%2BzvkO9FR0T7nO9E70QPROPs78SvRI9E51TvPS6YloCWhTc9LvUu9SL1IqFehQ6dXoFeiV6ROvU6nV6JDzw%3D%3D'''
print(ascii_to_str(sgext))
"""
动态改变 headers:
a-orange-dq
p1:a-orange-dq:appKey=21646297&appVersion=10.39.10&clientAppIndexVersion=1120240909183902431,
p2:a-orange-dq:appKey=21646297&appVersion=10.39.10&clientAppIndexVersion=1120240909185301901'   
                                                                         11+时间  时间在此之前?
 'c-launch-info': 'p1:c-launch-info:2,0,1725879059280,1725867180520,2, '
                  'p2:c-launch-info:2,0,1725879447342,1725867180520,2',
                                        时间戳         时间戳
'x-c-traceid': 'p1:x-c-traceid:04C61g3Z, 
                p2:x-c-traceid:04C812k2E',
'x-falco-id': 'p1:x-falco-id:04C61g3Z, 
               p2:x-falco-id:04C812k2E',
               
'x-mini-wua': 'p1:x-mini-wua:aiwSHTYZm6vbW%2BG2ULbOc1R%2FDl%2Br9pkzvNoQdUwHb1JpJnvfbtoAxKf90tIU1oGxaMPeG1P%2F0FeClHJamPgfP1n1CMr0y1Ye2DN42yfYesA6ctnHJ5Vh5iYiLP40s0it5laV88WyxLhBK%2FVCSf61%2BrX6tRf7lt8zIB33oIwnjnx%2FmccjqXUT2ewMm0QWZpDufGng%3D, '
              'p2:x-mini-wua:aigRhMvKJnuqb4W8kXxlNdYNZ9AxZ1vQa2PA%2BDuJdoc1iir08wH3ww%2FY3g8owvED%2BCzY4PJh5Kl8%2BWq2he0DzLl%2FyJWpLzjUHvkbB5EIe%2Fl7hQ5TgSMBfpVNJ5p0OMO5XOoD3KsMq1iJdKipLLN%2Btr7jKw78nJV8WXpURAFZBAAA7e34EvEiBI4vT8Kx7RV4iI9E%3D',
              
'x-sgext': 'p1:x-sgext:JBP5jfBIBGdY8CByizXt%2Bo3Ivcm%2Bza7BucG%2F2rzKutquyLrLuMG7zrzBvNq9z7qfucm%2Fye6btZu4zLmdrsi%2Bzq7Orsm92r3Jvc6uyq7IrsiuyK7Krsquy67Jrsu82r7avdq92r3avdq92r3avdqunK7Jrsmun7qd65q42r3Jvcm92r3auMC52r3arsiuyK7Krsmug86X3Nq92q3Zus%2Bt2a3JrsnSuOqM7Lv6uMm4z8HMsfq4sKa5pr%2Ffus%2BryKvJq86%2F376cq8ro373fvMmryL3fvMmryavItcy9zLjf%2BJP%2Bprimvd%2B937vP6Zzpyr2fq8mryavJq8mryujf66a7przfv9%2B%2B37jftN%2Fu3%2BnfvMjSztLNv9S8ybXUu9S91L3UvdS91LzUvdS81LzIvKbspr%2FfuN%2B9pu%2BmucCgyKDIuMmgyNKa0sigy7zUvtS91OzI752gm7XUuM6gz%2Bim6abYr8Or28jDq9jIyMTSn9LLoMmgy7TM0si9pty%2B2aPulP%2BR5bTM1rm4zLGiuMa756O9vcqA%2BrjMuMy4zLjMuMeM45jlyL2rz83nvNya35b%2Fku%2BV7pTPzcu46L36ssmOzLjMuMC4zLLXvcihwLjSyLymvd%2B917TOtcu6yqvKtN%2B8377Pq8y137nJq8mryLXfvMq737TMq8i%2FprzL0sugy7zUvMm9ydLIvqbMqua4%2BbjM0sy9%2BrjMuMyAzLvmuOyozKDMusi40si7pr2mvM7SyKDIoMugy7rUvMC71L3Uv9S5yqDNu9S%2FwNI%3D, '
           'p2:x-sgext:JBN6kO3LGeRFcz3xlrbweZBLoEqjTrNCpEKiWaFOolmzS6dIpUKmTaFCoVmgTKccpEqiSvMYqBilT6Qes0ukSLNNs0qgWaBKoE2zSbNLs0uzS7NJs0mzSLNKs0ijWaNZoFmgWaBZoFmgWaBZoFmzH7NKs0qzHKce9hmlWaBKoEqgWaBZpUOkWaBZs0uzS7NJs0qzANMUwVmgWbBapxuwWrBKs0rPO%2FcP9TLBO9Q70kLRMuc7rSWkJaJcp0y2S7ZLqEK2TadcpEm2TqNcoFyhSrZLoFyhSrZKtkuoT6BPpVzlEOMlpSWgXKBcpkz0H%2FROqU22SrZKtkq2SrZOo1z2JaYloVyiXKNcpVypXPNc9FyhS89Nz06lV6FLo1emV6BXoFegV6BXoVegV6FXp0nPG89Itk%2B2Ss8Yz06pV6FXoU%2BgV6El8yWhV6JJvUm9Sr1LoEmlV%2FIYvU%2F1V6Yfzx7PL8Y0wiyhNMIvoT%2BtJfYlolegV6JDpSWhSs880RvaGf0I%2BBLdO79O0TvYVdEx0hDKStQ96Q3RO9E70TvRO9Ew5RTxEqFKwjikENUr8yj%2FCPsY%2FBn9OKQ80R%2FUDds%2B5zvRO9E30TvbI8UZ9TvRJaFLz0q2Sr5DpEKmQqVcpEq2S7ZJp1ylQ7ZOoVygXKFCtkukS7ZLoEq2S6MloUjPSL1Io1ehSqBKz0ujJdEp%2BzvkO9FR0T7nO9E70QPROPs78SvRI9E51TvPS6YloCWhTc9LvUu9SL1IqFehQ6dXoFeiV6ROvU6nV6JDzw%3D%3D',
 
 'x-sign': 'p1:x-sign:azYBCM006xAAK8b0SXon17aahxoOa8b7zwc6HaFlCdKW2zbvXR91M8%2B6htLbr8saD6ksCp9gwsm9QeK%2FZbHy959HkGJW%2B8b7xkvG%2B8, '
           'p2:x-sign:azYBCM006xAAJAM9zZ7dnlevN38L1AM0Csj%2F0mSqzB1TFPMgmNCw%2FAp1Qx0eYA7VymbpxVqvBwZ4jidwoH43OFqIVa3zNAM0A%2FQDNA',
           
GET /gw/mtop.taobao.detail.data.get/1.0/?data=%7B%22detail_v%22%3A%223.3.2%22%2C%22exParams%22%3A%22%7B%5C%22appReqFrom%5C%22%3A%5C%22detail%5C%22%2C%5C%22container_type%5C%22%3A%5C%22xdetail%5C%22%2C%5C%22countryCode%5C%22%3A%5C%22CN%5C%22%2C%5C%22cpuCore%5C%22%3A%5C%224%5C%22%2C%5C%22cpuMaxHz%5C%22%3A%5C%22null%5C%22%2C%5C%22deviceLevel%5C%22%3A%5C%22medium%5C%22%2C%5C%22dinamic_v3%5C%22%3A%5C%22true%5C%22%2C%5C%22dynamicJsonData%5C%22%3A%5C%22true%5C%22%2C%5C%22finalUltron%5C%22%3A%5C%22true%5C%22%2C%5C%22id%5C%22%3A%5C%22570955047570%5C%22%2C%5C%22industryMainPicDegrade%5C%22%3A%5C%22false%5C%22%2C%5C%22isPadDevice%5C%22%3A%5C%22false%5C%22%2C%5C%22item_id%5C%22%3A%5C%22570955047570%5C%22%2C%5C%22itemid%5C%22%3A%5C%22570955047570%5C%22%2C%5C%22latitude%5C%22%3A%5C%2239.633542%5C%22%2C%5C%22liveAutoPlay%5C%22%3A%5C%22true%5C%22%2C%5C%22locate%5C%22%3A%5C%22guessitem-item%5C%22%2C%5C%22longitude%5C%22%3A%5C%22115.109334%5C%22%2C%5C%22newStruct%5C%22%3A%5C%22true%5C%22%2C%5C%22nick%5C%22%3A%5C%22tb793426967%5C%22%2C%5C%22openFrom%5C%22%3A%5C%22pagedetail%5C%22%2C%5C%22originalHost%5C%22%3A%5C%22item.taobao.com%5C%22%2C%5C%22osVersion%5C%22%3A%5C%2232%5C%22%2C%5C%22phoneType%5C%22%3A%5C%222206122SC%5C%22%2C%5C%22prefetchImg%5C%22%3A%5C%22%2F%2Fimg.alicdn.com%2Fbao%2Fuploaded%2Fi1%2F646849948%2FO1CN01JaLy292NMErkPV3Kk_%21%21646849948.jpg%5C%22%2C%5C%22prefetchImgRatio%5C%22%3A%5C%221%3A1%5C%22%2C%5C%22preload_v%5C%22%3A%5C%22industry%5C%22%2C%5C%22pvid%5C%22%3A%5C%2299fc0c74-9113-4d95-8d46-03f9f4939200%5C%22%2C%5C%22rmdChannelCode%5C%22%3A%5C%22guessULike%5C%22%2C%5C%22scm%5C%22%3A%5C%221007.52183.392693.0001%5C%22%2C%5C%22screenHeight%5C%22%3A%5C%221280%5C%22%2C%5C%22screenWidth%5C%22%3A%5C%22720%5C%22%2C%5C%22skuId%5C%22%3A%5C%225151866163537%5C%22%2C%5C%22skuPriceType%5C%22%3A%5C%221%5C%22%2C%5C%22soVersion%5C%22%3A%5C%222.0%5C%22%2C%5C%22spm%5C%22%3A%5C%22a2141.1.guessitemtab_null.0%5C%22%2C%5C%22spm-cnt%5C%22%3A%5C%22a2141.7631564%5C%22%2C%5C%22supportIndustryMainPic%5C%22%3A%5C%22true%5C%22%2C%5C%22ultron2%5C%22%3A%5C%22true%5C%22%2C%5C%22utdid%5C%22%3A%5C%22Zs7Pnkn0r40DAKSy%2FCBlF7cX%5C%22%2C%5C%22videoAutoPlay%5C%22%3A%5C%22true%5C%22%7D%22%2C%22id%22%3A%22570955047570%22%7D HTTP/1.1
x-sgext: JBOtfQAc9DOopNAme2Edrn2cTZ1OmV6cSZhNmF6VT45enEqfSJRFnEqVT45Nm0rLSZ1PnR7PRc9ImEnJXpVNjkqOTZ1enU2dSo5OjkyOTI5MjkyOT45Pjk2OS45Pjk2OTY5Njk2OTY5Njk2OXshenV6dXpobmkqdGY5NnU2dTY5NjkiUSY5Njl6cXpxenl6dXtc%2BwyyOTY5djUmdXY1dnV6dIuwa2Sj9Guw57D%2BVPOUK7EDySfJPi0qbW59bm0vITZtKz0SLTpRbnVudW55Ei02LTYtNi02LIpginVudW5tLyE2bSs9Ei02LTYtNi02LTYtN8kvyTItPi0iLRIseixmLTJwimiKfTYBIn1CZUJ1QnVCdUJ1QnFCdUJxQmkTyHPJPi0yLTfIf8kmUUJxQnEidUJwiziKcUJRQnVCdUJxNnkiASctQyByAGJoiySL4K%2BMv%2B0zjL%2FhM6EDyG%2FJPgE2ATJoinE3yM%2BQ4zx7AD8UV4DyCSew85VLsNu8X903pOtQK7DzsPOw87DzsN9gTzBWcTf8%2FmRfoLM4vwg%2FGH8EewD%2BZO%2BwY6QrmOdo87DzsMOw85iTXNPo87CKcTPJNi02DRJVNnU6eW5pbmVuaW5xPi0ycW51bnEWLRZxbn0WLSvJMnyKdUJRQnE2dT%2FJMniLsLsY82TzsVuw52jzsPOwE7D%2FGPMws7CTsPug88kybIp0inEryTIBMgEyARIBPnVCdUJ1QnEmATJlQn0Ty
x-social-attr: 3
x-sign: azYBCM006xAAIiZfUmXRD%2FuZmo3TciZSL67atEHM6Xt48%2FZLybaVmAhHFns74ws469hSM6MzW32d6AIWhRgSXn%2FucMJWUiZSJmImUi
x-sid: 25601ccd9fad1321ce4f2a5cebbd86dd
x-uid: 4060247732
x-nettype: WIFI
Accept-Encoding: zstd, gzip
x-pv: 6.3
x-nq: WIFI
x-region-channel: CN
x-features: 27
x-app-edition: ST
x-app-conf-v: 0
x-mini-wua: abQTfiNOHHanBPhyCMIZitWiGk%2FPNqMulWy7OxzLyht1g4vrLT5n1IyZ6MZlfx%2BhDfn6zxF7eHyxG7%2FuBgiVUdp9Gb%2F7s%2FUQKRCbcDTHACeSQgSoEnWwaL9Kgn6o3WDjsWLMlRrPecQ%2BZOtk2Tha6YhhCOwNoGbs9ROlx2L9LBKxpCCbBAzxsP6OgEe4JD3xJ29s%3D
content-type: application/x-www-form-urlencoded;charset=UTF-8
cache-control: no-cache
x-t: 1725982840
Cookie: thw=cn; cna=1XdcH3s7PDQCAbaLojpdshsD; unb=4060247732; sn=; uc3=nk2=F5RCbI%2BdXCZjiwE%3D&vt3=F8dD3iTw3f9c8cirhBw%3D&id2=VyyX5kzmWC8CWg%3D%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; uc1=cookie15=UIHiLt3xD8xYTw%3D%3D&cookie14=UoYcBhZSJwRRuA%3D%3D&existShop=false&cookie21=UtASsssme%2BBq; csg=5b879bba; lgc=tb793426967; cancelledSubSites=empty; t=246d89171b7d7a6c1d6496ee37c7e4d7; cookie17=VyyX5kzmWC8CWg%3D%3D; dnk=tb793426967; skt=5d510fcc62c688bc; munb=4060247732; cookie2=25601ccd9fad1321ce4f2a5cebbd86dd; uc4=nk4=0%40FY4JgmlkWt%2B6XxD3jaRVcHRbqCq6fw%3D%3D&id4=0%40VXtYihzZEIb4DvOjlg%2F035PjZfjo; tracknick=tb793426967; _cc_=VT5L2FSpdA%3D%3D; ti=; sg=723; _l_g_=Ug%3D%3D; _nk_=tb793426967; cookie1=U7VhKT6Zogpj186DxzpRZK5AYBnOeYztZVynMtSn0wA%3D; _tb_token_=e63ba63568e10; sgcookie=W100f68wmYCN4r5pnaxrSRU%2B4EmlS4TcwQ47rV82SbZRM3L%2FjLT82SpQa20twcTXsyVYP7WiCwmnescD14VWpoZNHfmPo5gBbEnGLD8hFkPAlZf%2FdBqvlMQpmn6SH7Xd3aCQ; imewweoriw=3HFZhIVZ19FH41I%2FrjUwKNxgzBzO9U%2FXXkMiAYoLc2k%3D; WAPFDFDTGFG=%2B4cMKKP%2B8PI%2BKK8ZAgr1JMu5InNYCg%3D%3D; _w_tb_nick=tb793426967; ockeqeudmj=tCGyKNE%3D; isg=BCwsfJuRZiFRanIWv4gAkEX19ghe5dCPs4eyh4ZtLld6kc2brvXLHv8gtV8pKQjn; tfstk=f24IXgizUPojRqPsEDCZfjA7wfgUOJ_VyQG8i7Lew23Kw0ezHkodx9D8fRkwz60Fq4wSC8DEY23pFLHTCUkEz7h-PRePtvPREUG8UJgr2Tjnw4M_nk8rJDd3j-Pv8ySnzUg3r4BV3Z7qtW0oyWdUyeM365cRWXVDwWVnr4dweirTt3t6qesSy8QtBXD9JXe-pCCswbJp2ee861GoBLhKv4dt6jcJMzInsBM0O1n4_fgD1VNKCENQ5X3MxWM6yUU_CDMvFATJyPG3sC-FKebmHo2TXkUOahcnPVejXlXX-Yo75JZSxILxXPFLJD4PCUIzuEkfQcKWqvL-1x5113xzObwHaGBtcooKsfPR11trZDhi1x5113xovfcZe1164bf..
x-bx-version: 6.6.240704
f-refer: mtop
x-extdata: openappkey%3DDEFAULT_AUTH
x-ttid: 703304%40taobao_android_10.39.10
x-app-ver: 10.39.10
x-c-traceid: 04MFvHk2i
x-location: 115.109334%2C39.633542
a-orange-dq: appKey=21646297&appVersion=10.39.10&clientAppIndexVersion=1120240910225502650
x-accept-stream: true
x-regid: reg0pnFeVn0umJbetWmmuBkv0BEL1rHS
x-umt: 6h0Bnv5LPKLhUwKR2xLWrNinRhhWF9L7
x-utdid: Zs7Pnkn0r40DAKSy%2FCBlF7cX
c-launch-info: 2,0,1725982840752,1725981779819,2
x-appkey: 21646297
x-falco-id: 04MFvHk2i
x-page-url: http%3A%2F%2Fm.taobao.com%2Findex.htm
x-page-name: com.taobao.tao.welcome.Welcome
x-devid: AqG65eu5Gpa1TRU6pBy5oeIvE-NbacZRFaSYUrt0qtBF
user-agent: MTOPSDK%2F3.1.1.7+%28Android%3B12%3BXiaomi%3B2206122SC%29+DeviceType%28Phone%29
Host: trade-acs.m.taobao.com
Connection: Keep-Alive





"""