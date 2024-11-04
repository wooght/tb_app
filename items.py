# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoappItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TaobaoListItem(scrapy.Item):
    """
        淘宝商品列表Item
    """
    goods_list = scrapy.Field()

class GoodsItem(scrapy.Item):
    """
        淘宝商品Item
    """
    goods_content = scrapy.Field()