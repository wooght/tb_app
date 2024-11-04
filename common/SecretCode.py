# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :SecretCode.py
@Author     :wooght
@Date       :2024/9/24 16:54
@Content    :
"""
import base64
import random


class SecretCode:
    contrast_str = "0123456789-_=+*/|[]{}<>,.?!@#$%^&`~;:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    contrast_len = len(contrast_str)

    def encryption(self, plain_str):
        key_str = self.build_key()
        plain_str = base64.b64encode(plain_str.encode('utf-8')).decode('utf-8')
        plain_array = list(self.get_array(plain_str))
        secret_array = list(self.shift_key(plain_array, 101))
        secret_str = self.key_to_str(secret_array)
        secret_text = key_str+secret_str[::-1]
        return secret_text

    def decryption(self, secret_text):
        self.key_num = int(self.contrast_str.find(secret_text[0]))
        secret_str = secret_text[self.key_num+1:]
        secret_array = list(self.get_array(secret_str[::-1]))
        plain_array = list(self.shift_key(secret_array, -21))
        plain_str = self.key_to_str(plain_array)
        return base64.b64decode(plain_str).decode('utf-8')

    def build_key(self):
        """
        创建秘钥
        Returns
        -------
        key_str     秘钥
        """
        self.key_num = random.randint(1,self.contrast_len)
        key_str = ''.join({i:random.choice(self.contrast_str) for i in range(self.key_num)}.values())
        return str(self.contrast_str[self.key_num])+key_str

    def get_array(self, plain_str):
        """
        获取明文key值序列
        """
        for char in plain_str:
            yield self.contrast_str.find(char)

    def shift_key(self, nums_list, status):
        """
        对key进行移位
        Parameters
        ----------
        nums_list   key的列表
        status      移位方向

        Returns
        -------
        r_list      key的列表
        """
        if status < 0: self.key_num *= -1
        for k in nums_list:
            k = k + self.key_num
            # 溢出判断
            if k < 0:
                k += self.contrast_len
            elif k >= self.contrast_len:
                k -= self.contrast_len
            yield k

    def key_to_str(self, key_list):
        return ''.join([self.contrast_str[i] for i in key_list])


Wst = SecretCode()
if __name__ == '__main__':
    secret_code = Wst.encryption("17716870009")     # 6d$+4Mu6n85B/8j     8kkz=YAii=2HV961V8p-7D[-l
    print('secret code:',secret_code)
    print("plain:",Wst.decryption(secret_code))