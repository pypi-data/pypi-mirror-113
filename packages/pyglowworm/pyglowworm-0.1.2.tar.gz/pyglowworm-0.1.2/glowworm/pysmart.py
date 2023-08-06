# encoding: utf-8
"""
@file: pysmart.py
@desc:
@author: zhenguo
@time: 2021/7/9
"""

class Base(object):
    pass

class Smart(Base):
    def number_operation(self):
        """
        1 常见算术运算
        x, y = 3, 2
        print(x + y) # = 5
        print(x - y) # = 1
        print(x * y) # = 6
        print(x / y) # = 1.5
        print(x // y) # = 1
        print(x % y) # = 1
        print(-x) # = -3
        print(abs(-x)) # = 3
        print(int(3.9)) # = 3
        print(float(x)) # = 3.0
        print(x ** y) # = 9
        """
        pass

    def relu(self, x):
        """
        2 实现 relu

        x: 输入参数
        return：输出relu值

        在神经网络中，relu作为神经元的激活函数
        测试：
        relu(5) # 5
        relu(-1) # 0
        """
        return max(0, x)

    def base_convert(self):
        """
        3 进制转化
        十进制转换为二进制：

        In [2]: bin(10)
        Out[2]: '0b1010'
        十进制转换为八进制：

        In [3]: oct(9)
        Out[3]: '0o11'
        十进制转换为十六进制：

        In [4]: hex(15)
        Out[4]: '0xf'
        """
        pass



