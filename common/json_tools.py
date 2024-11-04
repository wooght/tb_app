# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :json_tools.py
@Author     :wooght
@Date       :2024/9/18 16:46
@Content    :
"""
import re, json
# 斜杠模型  slash:斜杠
slash_models = {'7': '\\'*7+'"', '3': '\\'*3+'"', '1': '\\'+'"', '0': '"'}

class JsonTools:
    @staticmethod
    def get_url_params(url):
        """
        获取get地址中的参数
        :param url:
        :return:
        """
        url_native = url.replace('\\', '')
        url_native = url_native.replace('"{', '{')
        url_native = url_native.replace('}"', '}')
        return json.loads(url_native)

    @staticmethod
    def get_key_words(p):
        """
        返回字典keys列表, 多级按照:连接
        :param p:
        :return:
        """
        if isinstance(p, dict):
            key_words = []
            for key, value in p.items():
                if isinstance(value, dict):
                    key_list = JsonTools.get_key_words(value)
                    if isinstance(key_list, list):
                        for k in key_list:
                            key_words.append(key + ':' + k)
                else:
                    key_words.append(key)
            return key_words
        else:
            return None

    @staticmethod
    def get_multi_dict(p, l):
        """
        根据键值栈 获取多级(不定级)dict的值
        """
        if len(l) > 1:
            c = p
            for k in l:
                c = c[k]
            return c
        else:
            return None

    @staticmethod
    def get_params_diff(p1, p2):
        """
        参数对比,返回不同参数的key
        :param p1:
        :param p2:
        :return:{':'联动key:不同值}
        """
        # 获取keys
        key_words = JsonTools.get_key_words(p1)
        key_words_p2 = JsonTools.get_key_words(p2)
        print('p1_key_words:', key_words, '\r\n p2_key_words:', key_words_p2)
        diff_key = {}
        for key in key_words:
            # 双方都有相同keys
            if key in key_words_p2:
                # 深度大于1,进行深度取值
                if ':' in key:
                    p1_multi = JsonTools.get_multi_dict(p1, key.split(':'))
                    p2_multi = JsonTools.get_multi_dict(p2, key.split(':'))
                    if p1_multi != p2_multi:
                        diff_key[key] = f'p1:{key}:{p1_multi}, p2:{key}:{p2_multi}'
                else:
                    if p1[key] != p2[key]:
                        diff_key[key] = f'p1:{key}:{p1[key]}, p2:{key}:{p2[key]}'
            # 没有相同keys
            else:
                if ':' in key:
                    p1_multi = JsonTools.get_multi_dict(p1, key.split(':'))
                    diff_key[key] = f'p1:{key}:{p1_multi}, p2:null'
                else:
                    diff_key[key] = f'p1:{key}:{p1[key]}, p2:null'
        return diff_key

    @staticmethod
    def multi_dict_string(d, current_depth, depth_dict):
        """
        多级字典转字符串 带斜杠判断
        taobao hashMap 字符串斜杠思路:
            除0级外,其余"要加斜杠
            {加斜杠:
                {}里外同级别的,{不加"
                不同级别的,加同外面级别一样的斜杠和"
            斜杠递增模式: 1:/     2: ///      3:///////
        Parameters
        ----------
        d               多级字典
        current_depth   初始深度
        depth_dict      深度字典

        Returns
        -------
        return_str      字符串
        """
        return_str = ''
        if isinstance(d, dict):
            start_bracket = '{'              # 前括号 bracket: 括号
            end_bracket = '},'                # 结束符号
            for key, val in d.items():
                if isinstance(val, dict):
                    child_keys = list(val.keys())
                    if len(child_keys) == 0:
                        key_depth = current_depth
                    else:
                        child_first = child_keys[0]
                        if child_first in depth_dict.keys():
                            key_depth = depth_dict[child_first]
                            if key_depth != current_depth:
                                # 深度改变
                                start_bracket = slash_models[current_depth] + '{'
                                end_bracket = '}' + slash_models[current_depth] + ','
                            else:
                                # {} 里外 \\\ 数相同,则{不需要双引号
                                start_bracket = '{'
                                end_bracket = '},'
                        else:
                            key_depth = current_depth
                            start_bracket = '{'
                            end_bracket = '},'
                    # 递归调用
                    slash = slash_models[current_depth]
                    return_str += slash+key+slash+':'+start_bracket+JsonTools.multi_dict_string(val, key_depth, depth_dict) + end_bracket
                else:
                    # 在深度字典中 则需要判断斜杠的个数
                    if key in depth_dict.keys():
                        slash = slash_models[depth_dict[key]]
                        current_str = slash + key + slash
                        v = ''
                        if not isinstance(val, str):
                            # 布尔值和数字 不需要双引号
                            if isinstance(val, bool):
                                v = 'true' if val else 'false'                      # 转小写
                            elif isinstance(val, int) or isinstance(val, float):    # python False 为-1  True 为1
                                v = str(val)
                        else:
                            v = slash + str(val) + slash
                        return_str += current_str + ':' + v + ','
                    else:
                        return_str += '"'+key+'":"'+str(val)+'",'
            return return_str[:-1]
        else:
            return None

    @staticmethod
    def get_keys_depth(s):
        """
        depth: 深度
        通过/的个数,获取字典深度关系
        Parameters
        ----------
        s

        Returns
        -------
        返回深度关系 {key:depth, key2:depth, ...}
        """
        random_nums = {'7':r'\\\\\\\\\\\\\\"(\w+)\\\\\\\\\\\\\\"\:', '3':r'\\\\\\"(\w+)\\\\\\"\:', '1':r'\\"(\w+)\\"\:'}   # 顶级无/  ,一级一个/ 二级 ///  三级///////
        depth_dict = {}
        for n, r in random_nums.items():
            re_result = re.findall(r, s)
            if len(re_result) > 0:
                for k in re_result:
                    depth_dict[k] = n
        return depth_dict