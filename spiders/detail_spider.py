import re
from typing import Iterable

import scrapy, time, random, json
from scrapy import Request
from TaobaoApp.models import tables
from TaobaoApp.common.detail_content_convert import core_to_json
from TaobaoApp.items import GoodsItem
from TaobaoApp.common.appium_test import AppiumTest


class TaobaoDetailSpider(scrapy.Spider):
    name = "taobao_detail"
    allowed_domains = ["taobao.com"]
    start_urls = ["https://trade-acs.m.taobao.com/gw/mtop.taobao.detail.data.get/1.0/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            'TaobaoApp.w_middlewares.hook_middlewares.HookMiddleWares': 400,
        }
    }
    task_list = []
    exists_list = []
    task_index = 30      # 任务序号
    max_task_index = 0  # 最大任务序号, 根据数据库待抓取条数而定
    r_nums = 400         # 传递参数中str3:r_30    一次一次的叠加


    def __init__(self, *args, **kwargs):
        """
        启动appium操作
        获取列表,组建任务队列
        Parameters
        ----------
        args
        kwargs
        """
        super(TaobaoDetailSpider, self).__init__(*args, *kwargs)
        self.app = AppiumTest()
        # 获取已经存在的商品详情
        sku_list = tables.db.query(tables.SkuContent).all()
        if len(sku_list) > 0:
            self.exists_list = [sku.t_id for sku in sku_list]

        # 获取列表数据, 搭建任务队列
        goods_list = tables.db.query(tables.GoodsList).all()
        if len(goods_list) > 0:
            for goods in goods_list:
                if goods.t_id not in self.exists_list:
                    if len(goods.skuid) > 0 and goods.shopTitle is not None:   # 筛选有skuid和shoptitle的商品
                        self.task_list.append(goods)
        self.max_task_index = len(self.task_list) - 1


    def make_meta(self):
        """
        构建meta参数
        Returns
        -------

        """
        next_task_goods = self.task_list[self.task_index]   # 获取任务队列中的商品
        prefetch_img = next_task_goods.prefetchImg
        meta = {'t_id': next_task_goods.t_id, 'prefetchImg': prefetch_img, 'pvid': next_task_goods.pvid,
                'scm': next_task_goods.scm, 'sku_id': next_task_goods.skuid, 'st3': f'r_{self.r_nums}',
                'shopTitle': next_task_goods.shopTitle, 'shopIcon':next_task_goods.shopIcon}
        # 部分商品没有视频,故要做判断,MiddleWare会据此选择hashMap参数
        if next_task_goods.videoUrl is not None:
            meta['videoUrl'] = next_task_goods.videoUrl
            meta['videoId'] = next_task_goods.videoId
        target_url = next_task_goods.target_url
        spm = re.findall(r'spm=([^&]*)', str(target_url))[0]
        meta['spm'] = spm
        return meta


    def start_requests(self) -> Iterable[Request]:
        """
            构建初始请求 只构建一个,其余队列根据前请求反馈情况而定
        Returns
        -------

        """
        first_meta = self.make_meta()
        yield Request(url=self.start_urls[0],
                      method='GET',
                      callback=self.parse,
                      meta=first_meta)
        self.task_index += 1

    def extract_data(self, core_json):
        """
            提取数据
        Parameters
        ----------
        core_json

        Returns
        -------

        """
        goods_dict = {}
        """商品详情"""
        """商品详情"""
        try:
            base_contents = core_json["data"]["props"]["groupProps"][0]["基本信息"]
        except Exception as e:
            base_contents = core_json["data"]["apiStack"][0]["value"]["global"]["data"]["itemParams"]["groupProps"][0][
                "基本信息"]
        base_contents_list = [key + ':' + val for item in base_contents for key, val in item.items()]
        goods_dict['contents'] = ';'.join(base_contents_list)
        """商品属性"""
        core_item = core_json['data']['item']  # 商品Item信息
        goods_dict['t_id'] = core_item['itemId']  # 商品id 列表中的t_id
        goods_dict['title'] = core_item['title']
        goods_dict['h5_url'] = core_item['h5ItemUrl']  # 可以直接访问的h5地址
        goods_dict['category_id'] = core_item['categoryId']  # 分类id
        try:
            goods_dict['brand_id'] = core_item['brandValueId']  # brand id
        except Exception as e:
            goods_dict['brand_id'] = 0
        images = [item for item in core_item['images']]
        goods_dict['images'] = ';'.join(images)  # 图片地址,用;连接多个
        """价格"""
        """
            ["data"]["apiStack"][0]["value"]["data"]["detail3Atmosphere"]["fields"]["extraPrice"]["priceText"]      priceText/100 priceTitle: 优惠前
            ["data"]["apiStack"][0]["value"]["data"]["detail3Atmosphere"]["fields"]["price"]["priceText"]           priceText       priceTitle:折后
        """
        try:
            try:
                price_item = core_json["data"]["apiStack"][0]["value"]["data"]["detail3Price"]
                goods_dict['price'] = price_item["fields"]["price"]["priceText"]  # 实际折扣后价格
                try:
                    goods_dict['extra_discount'] = price_item["fields"]["extraDiscount"]["infoList"][0]["text"]  # 活动/折扣名称
                except:
                    # 无活动
                    goods_dict['extra_discount'] = ''
                try:
                    goods_dict['extra_price'] = price_item["fields"]["extraPrice"]["priceText"]  # 活动前价格
                except Exception as e:
                    goods_dict['extra_price'] = goods_dict['price']
            except Exception as e:
                price_item = core_json["data"]["apiStack"][0]["value"]["data"]["detail3Atmosphere"]["fields"]
                goods_dict['price'] = price_item['price']['priceText']                      # 活动后价格
                goods_dict['extra_price'] = price_item['extraPrice']['priceText'] / 100     # 活动前价格
        except Exception as e:
            extra_price = core_json["data"]["apiStack"][0]["value"]["global"]["data"]["priceSectionData"]
            try:
                goods_dict['price'] = extra_price["extraPrice"]['priceText']  # 实际折扣后价格
                goods_dict['extra_discount'] = extra_price["extraPrice"]['priceTitle']  # 活动/折扣名称
                goods_dict['extra_price'] = int(extra_price['price']['priceMoney']) / 100  # 活动前价格
            except Exception as e:
                goods_dict['extra_discount'] = extra_price['price']['priceTitle']
                goods_dict['extra_price'] = int(extra_price['price']['priceMoney']) / 100  # 活动前价格
                goods_dict['price'] = goods_dict['extra_price']
        """服务保障"""
        goods_service = \
            core_json["data"]["apiStack"][0]["value"]["data"]["detail3Service"]["fields"]["group"]["items"][0]["values"]
        goods_dict['sale_service'] = ';'.join([val for item in goods_service for key, val in item.items()])  # 多个保障用;连接
        """物流信息"""
        try:
            logistic_service = core_json["data"]["apiStack"][0]["value"]["data"]["detail3LogisticService"]["fields"]
            goods_dict['logistic_time'] = logistic_service['agingDesc']
            goods_dict['logistic_addr'] = logistic_service['deliveryFromAddr']
            goods_dict['logistic_freight'] = logistic_service['freight']
        except Exception as e:
            print('物流信息错误')
        """商家信息"""
        seller = core_json['data']['seller']
        goods_dict['seller_id'] = seller['userId']  # 商家用户id
        goods_dict['shop_id'] = seller['shopId']  # 店铺id
        return goods_dict

    def parse(self, response, *args):
        unpackable = False                              # 能否解析/分析
        result_body = response.body.decode('utf-8')
        try:
            core_json = core_to_json(result_body)       # 转json
            unpackable = True
        except json.decoder.JSONDecodeError as e:       # 转json失败, 上文已经输出result_body
            print('*'*50, e)
            unpackable = False
        except ValueError:
            print('*'*50, 'ValueError:', ValueError)   # 获取内容太短,有可能返回的是h5地址
            if '挤爆' in result_body:
                print('反爬。。。')
                return
            unpackable = False
        if unpackable:
            goods_item = GoodsItem()
            try:
                goods_dict = self.extract_data(core_json)               # 从json中提取数据
                goods_dict['sku_id'] = response.request.meta['sku_id']  # 获取request的参数
                goods_item['goods_content'] = goods_dict
                print(goods_dict['title'], '*'*50)
            except Exception as e:
                print(result_body)                                      # 获取json数据失败,输出result_body内容
                print('*'*50, 'extract_data Error', e)
            yield goods_item

        if self.task_index < self.max_task_index:
            meta = self.make_meta()
            print(self.task_list[self.task_index].title, 'start run request..., current task nums:{}'.format(self.task_index))
            if self.r_nums % 2 == 0:
                print('*'*50, 'appium 操作app', end=' ')
                random_nums = random.randint(0, 10)
                if random_nums % 3 == 0:
                    print('click item')
                    self.app.click_item()
                elif random_nums % 10 == 0:
                    print('click nav')
                    self.app.click_nav()
                else:
                    print('scroll goods list ')
                    self.app.scroll_loop()
            else:
                time.sleep(random.randint(14, 40))

            yield Request(url=self.start_urls[0],
                          method='GET',
                          callback=self.parse,
                          meta=meta, dont_filter=True)
            self.task_index += 1
            self.r_nums += 1




"""
result json 結構:
title:      ["data"]["item"]["title"]
itemId:     ["data"]["item"]["itemId"]
tmurl:      ["data"]["item"]["tmallDescUrl"]
h5url:      ["data"]["item"]["h5ItemUrl"]
taobaourl:  ["data"]["item"]["taobaoDescUrl"]
images:     ["data"]["item"]["images"][0]/[1]/[2]/[3]...
brandid     ["data"]["item"]["brandValueId"]                brandValueId    品牌ID?
categoryId  ["data"]["item"]["categoryId"]
基本信息      ["data"]["props"]["groupProps"][0]["基本信息"] "生成日期":"2022年...."
优惠前价格:  ["data"]["apiStack"][0]["value"]["data"]["detail3Price"]["fields"]["extraPrice"]["priceText"]
活动:       ["data"]["apiStack"][0]["value"]["data"]["detail3Price"]["fields"]["extraDiscount"]["infoList"][0]["text"]
实际价格:     ["data"]["apiStack"][0]["value"]["data"]["detail3Price"]["fields"]["price"]["priceText"] 多个价格/活动在这里
skuId       ["data"]["apiStack"][0]["value"]["data"]["detail3Price"]["events"]["priceClick"][0]["fields"]["exParams"]["content"]["skuMoney"]["skuId"]
价格*100     ["data"]["apiStack"][0]["value"]["data"]["detail3Price"]["events"]["priceClick"][0]["fields"]["exParams"]["content"]["skuMoney"]["cent"]
已售数量     ["data"]["apiStack"][0]["value"]["data"]["detail3Price"]["fields"]["sales"]["text"]
置顶标签:
    销售保障:    ["data"]["apiStack"][0]["value"]["data"]["detail3GoodsTag"]["fields"]["tags"][0]["text"]   退运费险
    加购数量     ["data"]["apiStack"][0]["value"]["data"]["detail3GoodsTag"]["fields"]["tags"][1]["text"]
服务保障:    极速退款:["data"]["apiStack"][0]["value"]["data"]["detail3GoodsTag"]["events"]["click1"][0]["fields"]["exParams"]["content"]["originService"][0]["name"]
            ["data"]["apiStack"][0]["value"]["data"]["detail3Service"]["fields"]["group"]["items"][0]["values"][0]["text"]
            7天无理由:["data"]["apiStack"][0]["value"]["data"]["detail3GoodsTag"]["events"]["click1"][0]["fields"]["exParams"]["content"]["originService"][1]["name"]
            ["data"]["apiStack"][0]["value"]["data"]["detail3Service"]["fields"]["group"]["items"][0]["values"][1]["text"]
            退货运费险:["data"]["apiStack"][0]["value"]["data"]["detail3GoodsTag"]["events"]["click1"][0]["fields"]["exParams"]["content"]["originService"][2]["name"]
            ["data"]["apiStack"][0]["value"]["data"]["detail3Service"]["fields"]["group"]["items"][0]["values"][2]["text"]
物流信息:
    发货时间:   ["data"]["apiStack"][0]["value"]["data"]["detail3LogisticService"]["fields"]["agingDesc"]
    发货地点:   ["data"]["apiStack"][0]["value"]["data"]["detail3LogisticService"]["fields"]["deliveryFromAddr"]
    包邮?:     ["data"]["apiStack"][0]["value"]["data"]["detail3LogisticService"]["fields"]["freight"]
    
卖家信息:       ["data"]["seller"]
    店铺名称:   ["data"]["seller"]["shopName"]
    店铺ID     ["data"]["seller"]["shopId"]
    粉丝       ["data"]["seller"]["fans"]9
    店家ID     ["data"]["seller"]["userId"]
    商品总数:   ["data"]["seller"]["allItemCount"]
    店家级别:   ["data"]["seller"]["certText"]  金牌卖家
    信用级别:   ["data"]["seller"]["creditLevel"]
    互动属性:   ["data"]["seller"]["dataTypeLabels"] 列表: 回头客,月销量,半年好评,收藏等
                                                    outputName  processedValue
                                                        名称      描述
    店铺地址:   ["data"]["seller"]["entranceList"][0]["action"][0]["params"]["url"]
    店铺评价:   ["data"]["seller"]["evaluates"] 列表: title, levelText, score
                                                     名称,    评价级别    打分
                                                     
返回特殊数据:

{"api":"mtop.taobao.detail.data.get","data":{"debug":{"dataFrom":"service"},"feature":{"isOnLine":"true","tcloudToH5":"true"},"trade":{"redirectUrl":"https://web.m.taobao.com/app/detail-project/newexpired/home?1=1&itemId=827161163252&sellerId=3321555335&shopId=495394758&expired=true&wx_navbar_hidden=true&isSuperAct=false&wx_statusbar_hidden=true"}},"ret":["SUCCESS::调用成功"],"v":"1.0"}
"""