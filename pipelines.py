# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from TaobaoApp.models import tables
from TaobaoApp.items import TaobaoListItem, GoodsItem


class TaobaoappPipeline:
    exists_goods = []       # 已经存在列表中的商品
    exists_sku = []         # 已经存在详情中的商品

    def __init__(self, *args, **kwargs):
        super(TaobaoappPipeline, self).__init__(*args, **kwargs)
        # 获取已经存在的数据
        list_goods = tables.db.query(tables.GoodsList).all()
        if len(list_goods) > 0:
            self.exists_goods = [goods.t_id for goods in list_goods]

        # 获取已经存在的商品详情
        list_sku = tables.db.query(tables.SkuContent).all()
        if len(list_sku) > 0:
            self.exists_sku = [sku.t_id for sku in list_sku]

    def process_item(self, item, spider):
        if isinstance(item, TaobaoListItem):
            """ 商品列表数据处理 """
            for goods in item['goods_list']:
                if goods['t_id'] not in self.exists_goods:
                    tables.db.add(tables.GoodsList(**goods))
                    self.exists_goods.append(goods['t_id'])
                else:
                    print(f'已经存在列表中:{goods['t_id']}, {goods['title']}')
            tables.db.commit()
        elif isinstance(item, GoodsItem):
            """商品详情数据处理"""
            sku = item['goods_content']
            if sku['t_id'] not in self.exists_sku:
                tables.db.add(tables.SkuContent(**sku))
                self.exists_sku.append(sku['t_id'])
            else:
                print('已经存在', sku['title'])
            tables.db.commit()
