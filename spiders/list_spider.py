"""
    列表页爬虫
    判断redis中是否有detail task
    没有则爬取列表页内容
    然后提取列表页内容,将task写入redis中
"""
from typing import Iterable, Any
from typing_extensions import Self

import scrapy
from scrapy import Request, FormRequest, signals, Spider
from scrapy.crawler import Crawler
import json, os, time, random, re
from TaobaoApp.items import TaobaoListItem
import TaobaoApp.common.headers_up
from scrapy.exceptions import DontCloseSpider
from TaobaoApp.models import tables as tb

class TaobaoListSpider(scrapy.Spider):
    """
        列表页爬虫
    """
    name = "taobao_list"
    allowed_domains = ["taobao.com"]
    start_urls = ["https://guide-acs.m.taobao.com/gw/mtop.taobao.wireless.home.category/1.0/"]
    start_page = 6      # 起始页面
    pindao = 'pindao_0002'
    page_total = 0      # 总页面数
    is_last_page = 'n'    # 是否最后一页

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'TaobaoApp.w_middlewares.hook_middlewares.HookMiddleWares': 400,
        }
    }

    def __init__(self, crawler, *args, **kwargs):
        super(TaobaoListSpider, self).__init__(*args, **kwargs)
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        """
        构造带crawler的spider实例, 信号绑定
        :param crawler:  爬虫引擎
        :param args:
        :param kwargs:
        :return:
        """
        spider = cls(crawler)
        crawler.signals.connect(spider.idle, signal=signals.spider_idle)                    # spider_idle 空闲信号绑定
        crawler.signals.connect(spider.parse_err, signal=signals.spider_error)              # spider错误信号绑定
        crawler.signals.connect(spider.request_scheduled, signal=signals.request_scheduled) # request_scheduled 请求排入队列信号
        crawler.signals.connect(spider.w_close, signal=signals.spider_closed)               # 绑定关闭信号
        return spider

    def idle(self):
        print('空闲判断')
        task_list = tb.r.llen('taobao_detail')
        if task_list > 0:
            print('detail task 进行中....')
        else:
            if self.start_page < int(self.page_total) and self.is_last_page == 'n':
                print(f'访问第{self.start_page}页。。。。。。')
                time.sleep(random.randint(8,20))
                meta = {'page_num': self.start_page, 'st3': 'r_31', 'pindao': self.pindao}
                self.start_page += 1
                new_request = FormRequest(url=self.start_urls[0], dont_filter=True,
                                  method='POST',
                                  body='',
                                  callback=self.parse,
                                  meta=meta)
                self.crawler.engine.crawl(new_request)
        raise DontCloseSpider

    def w_close(self):
        print('列表爬取结束')
        return None

    def parse_err(self, failure):
        '''
        错误处理,如timeout
        :param failure:
        :return:
        '''
        print(f'{failure.__class__.__name__}:', failure.request.url)


    def request_scheduled(self, request):
        """
        新请求加入队列通知
        :param request:
        :return:
        """
        print(f'新请求secheduled, 第{self.start_page}个,ID:{request.meta['page_num']}')


    def start_requests(self):
        meta = {'page_num': self.start_page, 'st3':'r_31', 'pindao':self.pindao}
        self.start_page += 1
        yield FormRequest(url=self.start_urls[0],
                      method='POST',
                      body='',              # 默认为空, 在MiddleWare中进行填充
                      callback=self.parse,
                      meta=meta)

    def parse(self, response, *args):
        json_txt = response.body.decode('utf-8')
        json_txt = json_txt.replace('\\', '')
        json_txt = json_txt.replace('"{', '{')
        json_txt = json_txt.replace('}"', '}')
        # json_txt = json_txt.replace('},"ret":["SUCCESS::调用成功"],"v":"1.0"', '')
        # 输出原始数据
        # print(json_txt)

        try:
            result_json = json.loads(json_txt)
        except Exception as e:
            print(e.__str__())
            print('本次Request 结束')
            # print(json_txt)
            return None
        # pprint.pprint(result_json)
        # for key, val in result_json.items():
        #     print(key)                # 共4个字段 api,data,ret, v
        # 获取data->containers(容器)内容
        # recommend_multi_channel->pageParams   页面参数

        if 'main_title' not in json_txt:
            print('找不到main_title')
        else:
            # 总页面数量
            self.page_total = result_json["data"]["containers"]["recommend_multi_channel"]["base"]["pageParams"]["pageTotal"]
            # 是否最后一页
            self.is_last_page = result_json["data"]["containers"]["recommend_multi_channel"]["base"]["pageParams"][
                "isLastPage"]

            goods_item = result_json['data']['containers']['recommend_multi_channel']['base']['sections']
            items = TaobaoListItem()
            items['goods_list'] = []
            sku_id_pattern = r'skuId=(\d+)'                 # 从target_url 中匹配skuId字段
            prefetchImg_pattern = r'prefetchImg=([^&]*)'    # 从target_url 中匹配 prefetchImg字段
            session_id_pattern = r'sessionid%22%3A%22([^%]+)%22'    # 匹配session id
            hybrid_score_pattern = r'hybrid_score%22%3A([\d\.]+)%2C'    # 匹配hybrid_score
            tpp_buckets_pattern = r'tpp_buckets%22%3A%22%7E9%7E(.*)%22%2C%22pvid'

            for item in goods_item:
                current_goods = {}
                try:
                    current_goods['title'] = item["item"]["0"]["smartContent"]["main_title"]["v"]               # 标题
                except Exception as e:
                    print(e)
                    # print(item)
                    continue
                try:
                    current_goods['t_id'] = int(item['item']['0']['clickParam']['itemId'])                      # 淘宝id
                    current_goods['payment_nums'] = item["item"]["0"]["smartContent"]["price"]["bottom_tip"]    # 付款人数
                    current_goods['price'] = float(item['args']['final_price'])                                 # 价格
                    current_goods['pvid'] = item["args"]["pvid"]                                                # pvid
                    current_goods['scm'] = item["args"]["scm"]                                                  # scm
                    current_goods['target_url'] = item["item"]["0"]["targetUrl"]                                # 详情url

                    """从target_url中匹配skuId, prefetchImg"""
                    if 'skuId' in current_goods['target_url']:
                        current_goods['skuid'] = re.findall(sku_id_pattern, current_goods['target_url'])[0]
                    else:
                        print('no skuid:', current_goods['title'])
                        continue
                    if 'prefetchImg' in current_goods['target_url']:
                        current_goods['prefetchImg'] = re.findall(prefetchImg_pattern, current_goods['target_url'])[0]
                    else:
                        print('no prefetchImg in target_url')
                        continue
                    if 'sessionid' in current_goods['target_url']:
                        try:
                            # 获取sessionid 供推荐点击使用
                            current_goods['sessionid'] = re.findall(session_id_pattern, current_goods['target_url'])[0]
                            current_goods['hybrid_score'] = re.findall(hybrid_score_pattern, current_goods['target_url'])[0]
                            current_goods['tpp_buckets'] = re.findall(tpp_buckets_pattern, current_goods['target_url'])[0]
                        except Exception as e:
                            print(e)
                            print('获取session id失败')
                            continue
                    else:
                        print('no session id and no tpp_buckets')
                        continue
                    try:
                        """shop/视频 相关数据"""
                        """["item"]["0"]["ext"]["targetParams"]["openImmediatelyData"]"""
                        target_params = item["item"]["0"]["ext"]["targetParams"]["openImmediatelyData"]
                        target_keys = ['shopTitle', 'shopIcon', 'videoUrl', 'videoId']
                        for key in target_keys:
                            if key in target_params.keys():
                                current_goods[key] = target_params[key]
                    except Exception as e:
                        print(e, '没有视频数据')

                    current_goods['add_datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())    # 当前时间
                    print(current_goods['title'], current_goods['t_id'], current_goods['price'])
                    items['goods_list'].append(current_goods)
                    # 添加到redis
                    tb.r.lpush('taobao_detail', json.dumps(current_goods))
                except KeyError as e:
                    print(e)
                    continue

            # 进入pipelines 进行数据库保存
            yield items
            # if self.start_page < int(self.page_total) and self.is_last_page == 'n':
            #     print(f'访问第{self.start_page}页。。。。。。')
            #     time.sleep(random.randint(8,20))
            #     meta = {'page_num': self.start_page, 'st3': 'r_31', 'pindao': self.pindao}
            #     self.start_page += 1
            #     yield FormRequest(url=self.start_urls[0], dont_filter=True,
            #                       method='POST',
            #                       body='',
            #                       callback=self.parse,
            #                       meta=meta)
            task_list = tb.r.llen('taobao_detail')
            if task_list > 0:
                print('detail task 进行中....')
            else:
                if self.start_page < int(self.page_total) and self.is_last_page == 'n':
                    print(f'访问第{self.start_page}页。。。。。。')
                    time.sleep(random.randint(8,20))
                    meta = {'page_num': self.start_page, 'st3': 'r_31', 'pindao': self.pindao}
                    self.start_page += 1
                    yield FormRequest(url=self.start_urls[0], dont_filter=True,
                                      method='POST',
                                      body='',
                                      callback=self.parse,
                                      meta=meta)


if __name__ == '__main__':
    os.system(f'scrapy crawl {TaobaoListSpider.name}')

"""
https':b'',//trade-acs.m.taobao.com/gw/mtop.taobao.detail.data.get/1.0/?data=%7B%22detail_v%22%3A%223.3.2%22%2C%22exParams%22%3A%22%7B%5C%22appReqFrom%5C%22%3A%5C%22detail%5C%22%2C%5C%22container_type%5C%22%3A%5C%22xdetail%5C%22%2C%5C%22countryCode%5C%22%3A%5C%22CN%5C%22%2C%5C%22cpuCore%5C%22%3A%5C%224%5C%22%2C%5C%22cpuMaxHz%5C%22%3A%5C%22null%5C%22%2C%5C%22deviceLevel%5C%22%3A%5C%22medium%5C%22%2C%5C%22dinamic_v3%5C%22%3A%5C%22true%5C%22%2C%5C%22dynamicJsonData%5C%22%3A%5C%22true%5C%22%2C%5C%22finalUltron%5C%22%3A%5C%22true%5C%22%2C%5C%22id%5C%22%3A%5C%22706070532779%5C%22%2C%5C%22industryMainPicDegrade%5C%22%3A%5C%22false%5C%22%2C%5C%22isPadDevice%5C%22%3A%5C%22false%5C%22%2C%5C%22item_id%5C%22%3A%5C%22706070532779%5C%22%2C%5C%22itemid%5C%22%3A%5C%22706070532779%5C%22%2C%5C%22latitude%5C%22%3A%5C%2239.633542%5C%22%2C%5C%22liveAutoPlay%5C%22%3A%5C%22true%5C%22%2C%5C%22locate%5C%22%3A%5C%22guessitem-item%5C%22%2C%5C%22longitude%5C%22%3A%5C%22115.109334%5C%22%2C%5C%22newStruct%5C%22%3A%5C%22true%5C%22%2C%5C%22nick%5C%22%3A%5C%22tb793426967%5C%22%2C%5C%22openFrom%5C%22%3A%5C%22pagedetail%5C%22%2C%5C%22originalHost%5C%22%3A%5C%22item.taobao.com%5C%22%2C%5C%22osVersion%5C%22%3A%5C%2232%5C%22%2C%5C%22phoneType%5C%22%3A%5C%222206122SC%5C%22%2C%5C%22prefetchImg%5C%22%3A%5C%22%2F%2Fimg.alicdn.com%2Fbao%2Fuploaded%2Fi1%2F1745959548%2FO1CN012CoWRC2KP2SB52o4m_%21%211745959548.jpg%5C%22%2C%5C%22prefetchImgRatio%5C%22%3A%5C%221%3A1%5C%22%2C%5C%22preload_v%5C%22%3A%5C%22industry%5C%22%2C%5C%22pvid%5C%22%3A%5C%22ba60f752-4658-4e5e-8b95-6d9f57ef7ed4%5C%22%2C%5C%22rmdChannelCode%5C%22%3A%5C%22guessULike%5C%22%2C%5C%22scm%5C%22%3A%5C%221007.52183.392693.0002%5C%22%2C%5C%22screenHeight%5C%22%3A%5C%221280%5C%22%2C%5C%22screenWidth%5C%22%3A%5C%22720%5C%22%2C%5C%22skuId%5C%22%3A%5C%225044312052943%5C%22%2C%5C%22skuPriceType%5C%22%3A%5C%221%5C%22%2C%5C%22soVersion%5C%22%3A%5C%222.0%5C%22%2C%5C%22spm%5C%22%3A%5C%22a2141.1.guessitemtab_null.5%5C%22%2C%5C%22spm-cnt%5C%22%3A%5C%22a2141.7631564%5C%22%2C%5C%22supportIndustryMainPic%5C%22%3A%5C%22true%5C%22%2C%5C%22ultron2%5C%22%3A%5C%22true%5C%22%2C%5C%22utdid%5C%22%3A%5C%22Zs7Pnkn0r40DAKSy%2FCBlF7cx%5C%22%2C%5C%22videoAutoPlay%5C%22%3A%5C%22true%5C%22%7D%22%2C%22id%22%3A%22706070532779%22%7D
"""