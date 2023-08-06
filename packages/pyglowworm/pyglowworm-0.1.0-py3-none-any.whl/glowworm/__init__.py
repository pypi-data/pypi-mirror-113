# encoding: utf-8
"""
@file: __init__.py.py
@desc:
@author: zhenguo
@time: 2021/7/9
"""
from inspect import isfunction, isclass, getmembers
import glowworm.pysmart
import glowworm.extend
import os
import sys

# 依次扫描glowworm下所有除main的模块
for m in os.listdir(__name__):  # glowworm包
    # 将包下的所有模块，逐个导入，并调用其中的函数
    if m.startswith('__') or m == 'main.py':
        continue
    sp = __name__ + '.' + m.split('.')[0]
    try:
        for name, class_ in getmembers(sys.modules[sp], isclass):
            if class_.__base__ != pysmart.Base:
                continue
            smart_dict = class_.__dict__
            _basic_dict = {smart_dict[f].__doc__: smart_dict[f] for f in smart_dict
                           if isfunction(smart_dict[f])}
    except KeyError as key_err:
        print('warn: 模块{}中没有类或没有继承Base类'.format(m))
        continue

# 不要移动main这行代码
import glowworm.main

find = main.find_by_input_key
