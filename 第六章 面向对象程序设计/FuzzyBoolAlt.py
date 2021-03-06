#-*-coding: utf-8-*-
'''
对模糊布尔运算类的另外一种实现

相比较于之前的完全从0开始的FuzzyBool，这里采用继承float类来实现，但是这里需要禁用
父类中的一些方法，而不是单纯的继承和重载
'''
class FuzzyBool(float):
    def __new__(cls, value = 0.0):
        return super().__new__(cls, value if 0.0 <= value <= 1.0 else 0.0)

    def __invert(self):
        return FuzzyBool(1.0 - float(self))

    def __and__(self, other):
        return FuzzyBool(min(self, other))

    def __iand__(self, other):
        return FuzzyBool(min(self, other))

    def __repr__(self):
        return ("{0}({1})".format(self.__class__.__name__, self.__value))

    def __bool__(self):
        return self > 0.5

    def __int__(self):
        return round(self)

    '''
    第一种禁用方法
    '''
#    def __add__(self, other):
#        # 对于模糊布尔运算而言，加法是没有意义的，所以这里需要显示地禁止加法的使用
#        raise TypeError("unsupported operand type(s) for +:"
#                        "'{0}' and '{1}'".format(self.__class__.__name__, other.__class__.__name__))
#
#    def __neg__(self):
#        raise TypeError("bad operand type for unary -: '{0}'".format(self.__class__.__name__))

    '''
    第二种禁用方法
    这种方法其实是第一种方法的封装，在python中，内置的exec()函数可以用来将动态地执行从给定对象传递来的代码，这样就可以对一组相似的语句进行复用了
    '''
    # 单值操作的禁用
    for name, operator in (("__neg__", "-"), ("__index__", "index()")):
        expression = """def {0}(self): raise TypeError("bad operand type for unary {1}: '{{self}}'".format(self = self.__class__.__name__))""".format(name, operator)
        exec(expression)
        
    # 双值操作的禁用
    for name, operator in (("__add__", "+"), ("__mul__", "*")):
        expression = """def {0}(self, other): raise TypeError("unsupported operand type(s) for {1}: '{{self}}' and '{{other}}'".format(self = self.__class__.__name__, other = other.__class__.__name__))""".format(name, operator)
        exec(expression)

# 此处没有采用FuzzyBool.py中的类内部静态方法的实现，而是直接将函数是现在模块内部
def conjunction(*fuzzies):
    return FuzzyBool(min(fuzzies)) # 这里的实现方法不同，是因为FuzzyBool继承自float,不需要再次转换

def disconjunction(*fuzzies):
    return FuzzyBool(max(fuzzies))

if __name__ == '__main__':
    a, b = FuzzyBool(0.1), FuzzyBool(0.2)
    print(a + b)
