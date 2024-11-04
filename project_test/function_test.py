# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :function_test.py
@Author     :wooght
@Date       :2024/9/19 18:28
@Content    :函数测试
"""

import re
import json

target_url = '''//item.taobao.com/item.htm?id=818830480021&skuId=5520158404193&skuPriceType=1&scm=1007.52183.406103.0002&pvid=b52c7a26-1561-444a-af55-ab7b6663dd6a&spm=a2141.1.guessitemtab_null.13&locate=guessitem-item&prefetchImgRatio=1%3A1&prefetchImg=https://img.alicdn.com/imgextra/i2/1092054358/O1CN01aAHifY1i411jdTxL8_!!1092054358.jpg&rmdChannelCode=guessULike&utparam=%7B%22x_sid%22%3A%22%22%2C%22x_qzt_ad%22%3A%220%22%2C%22card_subtype%22%3A%22auction%22%2C%22up_pvid%22%3A%22b52c7a26-1561-444a-af55-ab7b6663dd6a%22%2C%22x_sid_cpm%22%3A%22%22%2C%22x_object_type%22%3A%22item%22%2C%22pic_id%22%3A%22O1CN01aAHifY1i411jdTxL8_%21%211092054358%22%2C%22content_id%22%3A%22473835129812%22%2C%22x_ad_bucketid_cpm%22%3A%22%22%2C%22page_num%22%3A2%2C%22sessionid%22%3A%22%22%2C%22hybrid_score%22%3A0.5065540075302124%2C%22card_type%22%3A%22auction%22%2C%22tpp_buckets%22%3A%22%7E9%7EU2wTiccwIayq1UJm2V5fMM9_9hHWdHahNz3KhhxFaRuoT1FtKj2dJB6OdoJ1D2GroH1FfW9deHF1JmrRGd-i41zB9XmvRZ9BsndDrK2Se11F2XcVr31EwgPi2dN_s1_r8exw7xlbdyD2JvbdLU1R3cdP1Nax9ddWCz96fO2whHtgdV2H9Virex1RhS6jdw2K1QgjdGPcXopdH1WaNm2fXxBmqdA3T6VppdzN51ZbsdN-WgsdNBlL3ee_2Kr-52eH2P2D93eM2ZuX96eJ1N52Qi5eHOTl5eFCJm5ey1ZSu7eL1W11z67eyX2C87ex1WnBr8eJ_1K7aeR2RbA5beYw1Ve9eIY9wgpeO1C6wdaeGZbwqbeX1F4w6beO_9ZpeeMG4_vbe-2_x0ceTHd-7deZ1N1F95f_2xcHudeHG1W3eeY1OfNmfeQ2A2JtfeP2M1V1meEM7wugeWX5UhheZ1Q6K8iex_6RpleZ1CZqpeN2O1XcjeL2V6BqjeTW1XsjeE1zaSnkeRSdK4leEQ2JeleJRbJjmeQ2N4Q6neNz1FoneEJ1UtmeDx-tmeM2F1B2nex2D7B9ne_2GYj0fY1FxgneI2w1wineS1P1GfpeQ2M2DiteX2_1K7oeT1FT9oey1y1MapeK2QMkoeI1S1_roeF1B3-a3fEV8LnreF1y6C5reEZ2Jqvew2xgWf1fx2Fbw2te-2B4wmreT1F2-sreMF4RfseL2P02ZpteX2_51H60fX2ViCcteY2L3La6fY2Y1GmueEOcF4ueF2WK3ueD2RW5ueRyX5ueRYgGtueBIk1Sd0fI1O1Ci0fw1JoOr4fw3ScVi1fPhO2Eq1fz-mAm2fA2SfN03fN2wdQo4fZ2FU83fxO8Rp3fG1VnIl4fXQcK45fxQlJs5fz2%7EJ691w-iecA%22%2C%22pvid%22%3A%22b52c7a26-1561-444a-af55-ab7b6663dd6a%22%2C%22x_item_ids%22%3A818830480021%2C%22auction_score%22%3A0.5065540075302124%2C%22deviceModel%22%3A%22phone%22%2C%22new_mt%22%3A%22I_x2i_slim%22%2C%22pic_type%22%3A%22content%22%2C%22x_sytab%22%3A%221001%22%2C%22glc%22%3A%221%22%2C%22x_object_id%22%3A%22818830480021%22%7D&itemid=818830480021&item_id=818830480021'''
sku_id_pattern = r'tpp_buckets%22%3A%22%7E9%7E(.*)%22%2C%22pvid'
print(re.findall(sku_id_pattern, target_url)[0])
prefetchImg_pattern = r'prefetchImg=([^&]*)'
print(re.findall(prefetchImg_pattern, target_url)[0])