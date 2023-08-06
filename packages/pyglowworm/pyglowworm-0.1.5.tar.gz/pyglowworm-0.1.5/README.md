文档API案例帮助利器

### 使用帮助文档

导入包，其中最重要的一个API：find方法
```python
from glowworm import find 
```
如果find方法不带有任何参数，默认显示前5个小例子

```
find()      
``` 
输出：

```
未输入查询关键词，默认显示前5个小例子

        Example
        --------
            
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
        

        Example
        --------
            
        2 实现 relu

        x: 输入参数
        return：输出relu值

        在神经网络中，relu作为神经元的激活函数
        测试：
        relu(5) # 5
        relu(-1) # 0
        

        Example
        --------
            
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
        

        Example
        --------
            
        4 整数和ASCII互转
        十进制整数对应的ASCII字符

        In [1]: chr(65)
        Out[1]: 'A'
        查看某个ASCII字符对应的十进制数

        In [1]: ord('A')
        Out[1]: 65
```

输入查询关键词：`互转`        
```
find('互转')  
```
查询得到结果：
``` 
找到 1 个包含"互转"的例子

        Example
        --------
                
        4 整数和ASCII互转
        十进制整数对应的ASCII字符

        In [1]: chr(65)
        Out[1]: 'A'
        查看某个ASCII字符对应的十进制数

        In [1]: ord('A')
        Out[1]: 65
        
```
输入关键词`十进制`

```
find('十进制')  
```

查询得到结果：

```
找到 2 个包含"十进制"的例子

        Example
        --------
                
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
        

        Example
        --------
                
        4 整数和ASCII互转
        十进制整数对应的ASCII字符

        In [1]: chr(65)
        Out[1]: 'A'
        查看某个ASCII字符对应的十进制数

        In [1]: ord('A')
        Out[1]: 65
```

### 最新release
v0.1.5

