# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :tables.py
@Author     :wooght
@Date       :2024/9/24 16:52
@Content    :
"""

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date, Time, Text, DateTime, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker
from TaobaoApp.common.SecretCode import Wst
import redis
import re

#
# REDIS_HOST = '192.168.101.101'
# REDIS_PORT = '6379'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'

# host 服务器地址,port端口, db数据库序号,socket_connect_timeout连接超时时间
pool = redis.ConnectionPool(host=MYSQL_HOST, port=6379, db=0, socket_connect_timeout=2)
r = redis.Redis(connection_pool=pool)  # 连接,指定连接池

"""
    定义表
"""
Base = declarative_base()

class GoodsList(Base):
    """
        商品列表 表
    """
    __tablename__ = 'goods_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    t_id = Column(BigInteger)          # 淘宝 itemID
    title = Column(String(64))      # 标题 main_title
    price = Column(Float)           # 价格 final_price
    pvid = Column(String(64))       # pvid
    skuid = Column(String(32))      # skuid
    scm = Column(String(32))        # scm
    target_url = Column(Text)       # 详情url
    payment_nums = Column(String)   # 付款人数
    add_datetime = Column(DateTime) # 添加时间
    prefetchImg = Column(String)    # prefetchImg地址
    shopTitle = Column(String(32))  # 店铺title
    shopIcon = Column(String(128))  # 店铺Logo
    videoUrl = Column(Text)         # 视频地址
    videoId = Column(Integer)       # 视频ID
    sessionid = Column(String(64))  # session id
    hybrid_score = Column(String(128))
    tpp_buckets = Column(Text)

class SkuContent(Base):
    """
        商品详情 表
    """
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, autoincrement=True)
    t_id = Column(BigInteger)                       # 淘宝itemid ,t_id
    sku_id = Column(BigInteger)                     # sku id
    brand_id = Column(BigInteger)                      #
    category_id = Column(Integer)                   # 分类ID
    seller_id = Column(BigInteger)                  # 商家ID
    shop_id = Column(BigInteger)                    # 店家ID
    bc_type = Column(String(16))                #
    title = Column(String(64))                  # 标题/名称
    h5_url = Column(String(64))                 # 商品详情地址
    images = Column(Text)                # 地址, 保存的时候;隔开
    contents = Column(Text)              # 详细信息,json格式保存
    extra_price = Column(Float)                 # 活动前价格
    extra_discount = Column(String(32))         # 折扣名称
    price = Column(Float)                       # 到手价格

    sales_desc = Column(String(32))     # 销量描述 类似: 已售200+

    sale_service = Column(String(128))       # 销售保障 ;隔开
    logistic_time = Column(String(64))      # 发货时间
    logistic_addr = Column(String(64))      # 发货地址
    logistic_freight = Column(String(64))   # 包邮与否


"""
    连接数据库
"""
host = MYSQL_HOST
port = MYSQL_PORT
database = 'taobao_app'
user = 'root'
password = Wst.decryption('.u/fe<qzO|~TrC;13E=z2vpQI#]X_?>[_.F!,T`!B')

engine = create_engine(
    f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8',
    echo=False,         # 打印SQL语句,生成环境关闭
    max_overflow=0,     # 超过连接池大小外最多创建的连接
    pool_size=5,        # 连接池大小
    pool_timeout=10,    # 连接超时时间
    pool_recycle=-1     # 多久后对连接池中的线程进行一次连接回收(重置)
)

Base.metadata.create_all(engine)        # 根据类创建数据库表
# 表结构定义结束/导入结束后 执行connection来执行数据库操作
Session = sessionmaker(bind=engine)  # 根据连接engine绑定会话
db = Session()  # 开启一个会话

def end():
    print('数据库commit')
    db.commit()
    db.close()

# if __name__ == '__main__':
#     exists_goods = db.query(Goods).filter(Goods.store_id == 1).all()
#     goods_tmp = {}
#     for goods in exists_goods:
#         goods_tmp[goods.bar_code] = goods
#     print(goods_tmp.keys())

if __name__ == '__main__':
    exists_list = db.query(GoodsList).all()
    # 从数据中提取skuid, prefetchImg 并保存到新的字段
    if len(exists_list) > 0:
        sku_id_pattern = r'skuId=(\d+)'
        prefetchImg_pattern = r'prefetchImg=([^&]*)'
        for goods in exists_list:
            # current_id = goods.id
            # if 'skuId' in goods.target_url:
            #     print(goods.title)
            #     skuid = re.findall(sku_id_pattern, str(goods.target_url))[0]
            #     db.query(GoodsList).filter(GoodsList.id==current_id).update({
            #         'skuid':skuid
            #     })
            # else:
            #     print(goods.target_url)
            # if 'prefetchImg' in goods.target_url:
            #     prefetchImg = re.findall(prefetchImg_pattern, str(goods.target_url))[0]
            #     db.query(GoodsList).filter(GoodsList.id == current_id).update({
            #         'prefetchImg': prefetchImg
            #     })
            spm = re.findall(r'spm=([^&]*)', str(goods.target_url))[0]
            print(spm)

        db.commit()

    # sqlalchemy 将返回结果转换为dict
    # exists_goods = [goods.__dict__ for goods in exists_list]
    # for item in exists_goods:
    #     print(item['t_id'])