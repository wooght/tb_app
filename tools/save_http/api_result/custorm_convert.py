# -- coding: utf-8 -
"""
@project    :TaobaoApp
@file       :custorm_convert.py
@Author     :wooght
@Date       :2024/9/30 21:35
@Content    :
"""


class Stack:
    d = list()
    h_opposite = {'h2': 'h1', 'f2': 'f1', 'y': 'y'}  # 成对的,相对的

    def pop(self, i=-1):
        if i > 0:
            return self.d.pop(i)
        else:
            return self.d.pop()

    def append(self, v):
        self.d.append(v)

    def remove(self):
        self.d.pop()
        return self.d.pop()

    def last(self):
        return self.d[-1]

    def is_twins(self):
        """
            判断默认引号是否成对
        """
        return True if self.d[-1] == self.d[-2] else False

    def is_opposite(self):
        """
            判断默认两个是否成对
        """
        return True if self.h_opposite[self.d[-1]] == self.d[-2] else False


with open('goods_content.txt', 'r', encoding='utf-8') as f:
    file_txt = f.read()
result_list = [s for s in file_txt.split('\n')]
length_txt = []
for s in result_list:
    if len(s) > 1000:
        length_txt.append(s.replace('data:', ''))
result_txt = length_txt[0]
# target_symbol = ['"', '\\"', '\\\\"', '\\\\\\"']
target_symbol = {'"': 'y', '{': 'h1', '[': 'f1', '}': 'h2', ']': 'f2'}
end_symbol = ['f2', 'h2', 'y']
result_txt = result_txt.replace('\\', '')
result_txt = result_txt.replace("'", '"')
result_txt = result_txt.replace('"{', '{')
result_txt = result_txt.replace(' ', '')
l = len(result_txt)
i = 0
keys = target_symbol.keys()
stack = Stack()
words = ''
while i < l:
    current_val = result_txt[i]  # 当前字符
    if current_val in keys:
        current_symbol = target_symbol[current_val]  # 当前字符索引
        stack.append(current_symbol)
        if current_symbol in end_symbol:
            if stack.is_opposite():
                if current_symbol == 'y':

                else:
                    stack.remove()

        words = ''
    else:
        words += current_val
    i += 1

print(stack.d)
print(words)
