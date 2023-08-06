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
import pkgutil

_basic_dict = dict()
# 依次扫描glowworm下所有除main的模块
for importer, modname, ispkg in pkgutil.iter_modules(path=['glowworm']):
    if ispkg:
        continue
    # print(modname)
    # 将包下的所有模块，逐个导入，并调用其中的函数
    if modname.startswith('__') or modname == 'main':
        continue
    sp = __name__ + '.' + modname
    try:
        for name, class_ in getmembers(sys.modules[sp], isclass):
            if class_.__base__ != pysmart.Base:
                continue
            smart_dict = class_.__dict__
            _basic_dict = {**{smart_dict[f].__doc__: smart_dict[f] for f in smart_dict
                              if isfunction(smart_dict[f])}, **_basic_dict}
    except KeyError as key_err:
        print('warn: 模块{}中没有类或没有继承Base类'.format(modname))
        continue

# 不要移动main这行代码
import glowworm.main

find = main.find_by_input_key
