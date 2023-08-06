# encoding: utf-8
"""
@file: main.py
@desc:
@author: zhenguo
@time: 2021/7/9
"""
from glowworm.pysmart import *
from glowworm import _basic_dict

def find_by_input_key(input_key=None, para_top_number=5):
    """
    支持 input_key 模糊查询，返回所有可能带有 input_key 的键值对
    目前支持依然偏弱，若input_key串过长，可能很难命中，需要提取其关键词并find
    :param para_top_number: 如果不输入input_key，默认返回前5个例子
    :param input_key: 输入key
    :return: 带有 input_key 的键值对
    """
    # input_key无输入
    if not input_key:
        print('未输入查询关键词，默认显示前%d个小例子' % (para_top_number, ))
        i = 0
        for key in _basic_dict:
            s = """
        Example
        --------
            """
            print(s + _basic_dict[key].__doc__)
            i += 1
            if i >= para_top_number:
                break
        return
    # 有输入但类型不满足
    if not isinstance(input_key, str):
        raise TypeError('输入关键词为%s，必须为str' % (str(type(input_key))))

    r = {key: _basic_dict[key] for key in _basic_dict if input_key in key}
    if len(r) == 0:
        print('例子库中未发现包含%s的案例' % (input_key,))
    elif len(r) == 1:
        for only_key in r.keys():
            s = """
        Example
        --------
                """
            print('找到 1 个包含"%s"的例子' % (input_key, ))
            print(s + r[only_key].__doc__)
    else:
        print('找到 %d 个包含"%s"的例子' % (len(r), input_key,))
        for kn in r:
            s = """
        Example
        --------
                """
            print(s + r[kn].__doc__)
