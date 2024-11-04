# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :hook_middlewares.py
@Author     :wooght
@Date       :2024/9/18 16:45
@Content    :进行hook操作
"""

import frida, sys, pprint, json, re, time, random, os
from TaobaoApp.common.json_tools import JsonTools
from TaobaoApp.common.extract_data import ExtractData as Ed
from scrapy.signals import spider_closed
from TaobaoApp.common.ascii_convert import zh_to_ascii

def open_file(name):
    with open(f'TaobaoApp/tools/{name}', 'r', encoding='utf-8') as f:
        return f.read()

class HookMiddleWares(object):
    script = object
    hashmap2 = '''{pageId=http://m.taobao.com/index.htm, pageName=com.taobao.tao.welcome.Welcome}'''
    str = '21646297'
    str2 = 'null'
    z = False
    str3 = 'r_37'
    headers_t = ''          # headers 字符串
    headers = {}            # headers dict
    cookies_t = ''          # cookies 字符串
    cookies = {}            # cookies dict
    hashMap_t = ''          # hashmap中data 字符串
    hashMap_data = {}       # 计算签名,以及get,post 提交内容
    called = False          # 是否hook
    last_launch_time = 0    # 最近缓存时间
    baseCacheTime = 0       # 上一次请求时间
    send_txt = ''           # hook到ryw的 字符串
    targetParams = {'openImmediatelyData':{}}       # 详情页额外参数


    def __init__(self):
        # # 获取预存内容
        # self.cookies = Ed.get_cookies_dict(open_file('save_http/cookie1.txt'))    # cookie 列表,详情cookie相同
        # self.headers_t = open_file('save_http/headers.txt')                         # 列表headers
        # self.headers = Ed.get_headers_dict(self.headers_t)
        # self.hashMap_t = open_file('save_http/hashMap1.txt')                        # 列表hasmMap1
        # self.hashMap_data = Ed.extract_category_params(self.hashMap_t)
        #
        # # self.hashMap_t = open_file('save_http/detail_hashMap.txt')                # 详情hashMap1  不知原因有这种格式???
        # # self.hashMap_data = Ed.extract_category_params(self.hashMap_t)
        #
        # self.hashMap_t = open_file('save_http/detail_hashMap_video.txt')    # 详情待targetParams
        # self.hashMap_data = Ed.extract_category_params(self.hashMap_t)
        #
        # self.headers_t = open_file('save_http/detail_headers.txt')                # 详情 headers
        # self.headers = Ed.get_headers_dict(self.headers_t)

        spider_name = sys.argv[1]      # 获取运行的爬虫名称
        # 加载JS, 运行hook
        self.hook_js = open_file('js/up_sign_params_2.js')
        self.run_hook()
        # 阻塞等待hook 返回参数
        while not self.called:
            time.sleep(1)
        time.sleep(5)
        # 关闭获取原始Headers的frida会话
        self.close_hook()
        # 开启运行hook
        self.hook_js = open_file('js/run_category.js') if spider_name == 'taobao_list' else open_file('js/run_detail.js')
        self.run_hook()


    def process_request(self, request, spider):
        request.cookies = self.cookies
        if spider.name == 'taobao_detail':
            self.update_detail_headers(request.meta)
            for k, v in self.headers.items():
                request.headers[k] = v
            request._set_url(request.url + '?data=' + zh_to_ascii(self.send_txt))       # 重构request url
        else:
            self.update_headers(request.meta)
            for k, v in self.headers.items():
                request.headers[k] = v
            # del request.headers['Content-Encoding']   # 详情页无，列表页有此项
            # del request.headers['Content-Length']

            body = self.send_txt
            # 重构request提交body
            request._set_body('data='+zh_to_ascii(body).replace(' ', '+'))
        request.headers.pop('Referer', None)
        return None


    def update_detail_headers(self, request_form):
        # self.hashMap_t = open_file('save_http/detail_hashMap_video.txt')    # 详情待targetParams
        # self.hashMap_data = Ed.extract_category_params(self.hashMap_t)
        now_time = time.time()
        # 两种长度的时间戳
        time_10 = int(now_time)
        time_13 = int(now_time * 1000)
        self.baseCacheTime = time_13 - random.randint(100, 400)
        self.last_launch_time = time_13 - random.randint(200000,
                                                         1000000) if self.last_launch_time == 0 else self.last_launch_time
        """修改提交数据"""
        self.hashMap_data['exParams']['item_id'] = str(request_form['t_id'])
        self.hashMap_data['exParams']['itemid'] = str(request_form['t_id'])
        self.hashMap_data['exParams']['id'] = str(request_form['t_id'])
        self.hashMap_data['exParams']['prefetchImg'] = request_form['prefetchImg']
        self.hashMap_data['exParams']['pvid'] = request_form['pvid']
        self.hashMap_data['exParams']['skuId'] = request_form['sku_id']
        self.hashMap_data['exParams']['scm'] = request_form['scm']
        self.hashMap_data['exParams']['spm'] = request_form['spm']

        if 'targetParams' in self.hashMap_data['exParams'].keys():
            self.hashMap_data['exParams']['targetParams']['openImmediatelyData']['shopIcon'] = request_form['shopIcon']
            self.hashMap_data['exParams']['targetParams']['openImmediatelyData']['shopTitle'] = request_form['shopTitle']

            # 判断是否有用视频地址
            if 'videoUrl' in request_form.keys():
                self.hashMap_data['exParams']['targetParams']['openImmediatelyData']['videoUrl'] = request_form['videoUrl']
                self.hashMap_data['exParams']['targetParams']['openImmediatelyData']['videoId'] = str(request_form['videoId'])
            else:
                self.hashMap_data['exParams']['targetParams']['openImmediatelyData'].pop('videoUrl', None)
                self.hashMap_data['exParams']['targetParams']['openImmediatelyData'].pop('videoId', None)
        # 将冲突的id修改过来
        self.hashMap_data['wooghtid'] = request_form['t_id']

        # self.script.exports.set_detail_hm()     # 设置 detail的专属hashMap  ??? 没有了, 视频页没有了????
        self.send_txt = JsonTools.multi_dict_string(self.hashMap_data, '0', JsonTools.get_keys_depth(self.hashMap_t))
        self.send_txt = self.send_txt.replace('wooghtid', 'id')     # 因为里面有两个id, get_keys_depth为做区分
        self.send_txt = self.send_txt.replace('spm_cnt', 'spm-cnt') # get_keys_depth 不支持 -
        # hook 获取sign等核心headers内容
        self.get_app_sign('{'+self.send_txt+'}', str(time_10), request_form['st3'])
        # 修改headers x-sign, x-c-traceid 等
        for key, val in self.sign_json.items():
            self.headers[key] = zh_to_ascii(val)
        self.headers['x-falco-id'] = self.falcoid
        self.headers['x-c-traceid'] = self.falcoid
        self.headers['x-t'] = time_10
        self.headers['c-launch-info'] = re.sub(r'(\d,\d,)\d{13},', r'\1___,', self.headers['c-launch-info'])
        self.headers['c-launch-info'] = self.headers['c-launch-info'].replace('___', str(time_13))

        # 额外添加参数
        self.headers['Host'] = 'trade-acs.m.taobao.com'
        self.headers['Connection'] = 'Keep-Alive'
        self.headers['cro-privacy-recommend-switch'] = 'open'
        now_datetime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.headers['a-orange-dq'] = f'appKey=21646297&appVersion=10.39.10&clientAppIndexVersion=11{now_datetime}{random.randint(1,1000)}'
        self.headers['a-orange-dq'] = 'appKey=21646297&appVersion=10.39.10&clientAppIndexVersion=1120241011231501818'


    def update_headers(self, request_form):
        page_num = request_form['page_num']
        now_time = time.time()
        # 两种长度的时间戳
        time_10 = int(now_time)
        time_13 = int(now_time*1000)
        self.baseCacheTime = time_13 - random.randint(100, 400)
        self.last_launch_time = time_13 - random.randint(200000, 1000000) if self.last_launch_time == 0 else self.last_launch_time
        """修改提交参数"""
        # 修改访问时间
        self.hashMap_data['containerParams']['recommend_multi_channel']['clientReqTime'] = time_13
        # 修改访问页码
        self.hashMap_data['containerParams']['recommend_multi_channel']['pageParams']['pageNum'] = page_num
        if page_num == 0:
            self.hashMap_data['containerParams']['recommend_multi_channel']['baseCacheTime'] = 0
        else:
            self.hashMap_data['containerParams']['recommend_multi_channel']['baseCacheTime'] = self.baseCacheTime
        self.hashMap_data['containerParams']['recommend_multi_channel']['bizParams']['guessChannelId'] = request_form['pindao']


        self.send_txt = JsonTools.multi_dict_string(self.hashMap_data, '0', JsonTools.get_keys_depth(self.hashMap_t))
        # hook 获取sign等核心headers内容
        self.get_app_sign('{'+self.send_txt+'}', str(time_10), request_form['st3'])
        # post 传递参数 只能传递一次 type 指定要访问的frida recv 函数
        # self.script.post({'type': 'sign', 'data': '{' + self.send_txt + '}', 'now_time': str(time_10), 'st3': request_form['st3']})  # 传递参数
        # self.called = True
        # while self.called:
        #     time.sleep(0.1)
        """修改headers"""
        # 修改headers x-sign, x-c-traceid 等
        for key, val in self.sign_json.items():
            self.headers[key] = zh_to_ascii(val)
        self.headers['x-falco-id'] = self.falcoid
        self.headers['x-c-traceid'] = self.falcoid
        self.headers['x-t'] = time_10
        self.headers['c-launch-info'] = re.sub(r'(\d,\d,)\d{13},', r'\1___,', self.headers['c-launch-info'])
        self.headers['c-launch-info'] = self.headers['c-launch-info'].replace('___', str(time_13))
        self.headers['x-biz-info'] = f'containerId=recommend_multi_channel_{request_form['pindao']};requestType='

        # 额外添加参数
        self.headers['Host'] = 'guide-acs.m.taobao.com'
        self.headers['Connection'] = 'Keep-Alive'



    def get_app_sign(self, send_txt, now_time, st3):
        """
        执行js进行hook函数操作，获取sign等签名
        Parameters
        ----------
        send_txt    发送字符串
        now_time    现在时间戳
        st3         请求序列 （目前观察可以不变）
        -------

        """
        # script.exports 访问hook js文件函数接口，并得到返回值
        back_data = self.script.exports.get_app_sign(send_txt, now_time, st3)
        # 查看back内容
        # print('*'*50)
        # print(back_data)
        self.sign_json = Ed.get_sign_params(back_data['data'][:-1])
        self.falcoid = back_data['falcoid']
        self.send_txt = back_data['form_data']

    def make_request_time(self):
        now_time = time.time()
        # 两种长度的时间戳
        time_10 = int(now_time)
        time_13 = int(now_time * 1000)
        self.baseCacheTime = time_13 - random.randint(100, 400)
        self.last_launch_time = time_13 - random.randint(200000,
                                                         1000000) if self.last_launch_time == 0 else self.last_launch_time



    def run_hook(self):
        """
            进行hook
            attach 绑定已经启动的app
            spawn 启动app,返回进程ID 然后再通过attach(pid) 绑定app
        """
        # 连接设备,绑定app
        self.process = frida.get_usb_device(-1).attach('淘宝')  # get_usb_device() 得到一个连接中的USB设备, attach() 附加到目标进程
        # 创建hook js文件
        self.script = self.process.create_script(self.hook_js)
        # 指定消息回调
        self.script.on('message', self.on_message)
        # 运行hook
        self.script.load()
        # self.script.exports.apply_function(process)
        # 等待刷新一次列表 获取hashMap
        time.sleep(10)
        # sys.stdin.read()  # 阻塞主线程,等待frida事件处理/返回
        # frida.resume(process.pid)

    def close_hook(self):
        self.process.detach()       # 断开frida会话

    def on_message(self, message, data):
        """
        获取hook js返回内容
        设置本地hashMap_t, headers_t, cookies_t
        """
        if not self.called:
            if message['type'] == 'send':
                result_type = message['payload']['type']
                print(result_type)
                result_d = {}
                if result_type == 'cookies':
                    self.cookies_t = message['payload']['cookies']
                    result_d = Ed.get_cookies_dict(self.cookies_t)
                elif result_type == 'headers':
                    self.headers_t = message['payload']['headers']
                    result_d = Ed.get_headers_dict(self.headers_t)
                elif result_type == 'hashMap_data':
                    self.hashMap_t = message['payload']['hashMap_data'].replace('"id"', '"wooghtid"')     # 将冲突的id替换
                    if 'spm-cnt' in self.hashMap_t:
                        self.hashMap_t = self.hashMap_t.replace('spm-cnt', 'spm_cnt')
                    print('on_message:', self.hashMap_t)
                    result_d = Ed.extract_category_params(self.hashMap_t)
                self.__setattr__(result_type, result_d)
            print(len(self.hashMap_t), len(self.headers_t), len(self.cookies_t))
        if len(self.hashMap_t) > 0 and len(self.headers_t) > 0 and len(self.cookies_t) > 0:
            print('called is true')
            self.called = True


    def process_spider_closed(self):
        print('停止爬虫,关闭frida')
        self.script.unload()        # 取消/卸载js
        self.process.detach()       # 断开连接

    def process_response(self, request, response, spider):
        if '非法' in response.body.decode('utf-8'):
            print(self.send_txt)
        return response

    @classmethod
    def from_crawler(cls, crawler):
        """
            注册中间件
        """
        s = cls()
        crawler.signals.connect(s.process_spider_closed, spider_closed)
        return s