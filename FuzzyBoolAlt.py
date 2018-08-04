#-*-coding: utf-8-*-
'''
对模糊布尔运算类的另外一种实现
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

    def __add__(self, other):
        # 对于模糊布尔运算而言，加法是没有意义的，所以这里需要显示地禁止加法的使用
        raise TypeError("unsupported operand type(s) for +:"
                        "'{0}' and '{1}'".format(self.__class__.__name__, other.__class__.__name__))

    def __neg__(self):
        raise TypeError("bad operand type for unary -: '{0}'".format(self.__class__.__name__))


# 此处没有采用FuzzyBool.py中的类内部静态方法的实现，而是直接将函数是现在模块内部
def conjunction(*fuzzies):
    return FuzzyBool(min(fuzzies)) # 这里的实现方法不同，是因为FuzzyBool继承自float,不需要再次转换

def disconjunction(*fuzzies):
    return FuzzyBool(max(fuzzies))
