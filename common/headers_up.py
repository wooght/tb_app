# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :headers_up.py
@Author     :wooght
@Date       :2024/9/24 19:17
@Content    : headers 大写转小写
"""
from twisted.web import http_headers


"""
    强制headers 小写
"""
http_headers.Headers._caseMappings.update({
    b'x-sgext': b'x-sgext',
    b'x-social-attr':b'x-social-attr',
    b'x-sign':b'x-sign',
    b'x-sid':b'x-sid',
    b'x-uid':b'x-uid',
    b'x-nettypeb':b'x-nettypeb',
    b'x-pv':b'x-pv',
    b'x-nq':b'x-nq',
    b'x-region-channel':b'x-region-channel',
    b'x-features':b'x-features',
    b'x-app-edition':b'x-app-edition',
    b'x-app-conf-v':b'x-app-conf-v',
    b'x-mini-wua':b'x-mini-wua',
    b'x-biz-type':b'x-biz-type',
    b'x-t':b'x-t',
    b'x-bx-version':b'x-bx-version',
    b'f-refer':b'f-refer',
    b'x-extdata':b'x-extdata',
    b'x-ttid':b'x-ttid',
    b'x-app-ver':b'x-app-ver',
    b'x-c-traceid':b'x-c-traceid',
    b'x-biz-info':b'x-biz-info',
    b'x-location':b'x-location',
    b'a-orange-dq':b'a-orange-dq',
    b'x-regid':b'x-regid',
    b'x-umt':b'x-umt',
    b'x-utdid':b'x-utdid',
    b'c-launch-info':b'c-launch-info',
    b'x-appkey':b'x-appkey',
    b'x-falco-id':b'x-falco-id',
    b'x-page-url':b'x-page-url',
    b'x-page-name':b'x-page-name',
    b'x-devid':b'x-devid',
    b'user-agent':b'user-agent',
    b'content-type':b'content-type',
    b'x-accept-stream':b'x-accept-stream',
    b'x-disastergrd':b'x-disastergrd',
    b'cro-privacy-recommend-switch':b'cro-privacy-recommend-switch',
    b'cache-control':b'cache-control',
    b'x-nettype': b'x-nettype',
})