#-*-coding: utf-8-*-
'''
模糊布尔代数类
'''
class FuzzyBool:
    def __init__(self, value = 0.0):
        self.__value = value if 0.0 <= value <= 1.0 else 0.0

    def __invert__(self):
        return FuzzyBool(1.0 - self.__value)

    def __and__(self, other):
        return FuzzyBool(min(self.__value, other.__value))

    def __iand__(self, other):
        self.__value = min(self.__value, other.__value)
        return self

    def __repr__(self):
        return ("{0}({1})".format(self.__class__.__name__, self.__value))

    def __str__(self):
        return str(self.__value)

    def __bool__(self):
        return self.__value > 0.5

    def __int__(self):
        return round(self.__value)

    def __float__(self):
        return self.__value

    def __lt__(self, other):
        return self.__value < other.__value

    def __eq__(self, other):
        return self.__value == other.__value

    def __hash__(self):
        return hash(id(self))

    '''
    默认情况下，自定义类的实例支持操作符==（总是返回False），并且是可哈希运算的（因此可以用作字典的键，也可以
    添加到集合中），但是如果我们重载了__eq__方法以便提供正确的相等性测试功能，实例就不再是可哈希运算的，不过
    这可以通过重载__hash__方法来弥补
    '''

    def __format__(self, format_spec):
        return format(self.__value, format_spec)

    '''
    静态方法，可以不需要传入self参数
    '''
    @staticmethod
    def conjunction(*fuzzies):
        return FuzzyBool(min([float(x) for x in fuzzies]))

    @staticmethod
    def disconjunction(*fuzzies):
        return FuzzyBool(max([float(x) for x in fuzzies]))

    '''
    此处的静态方法被放置在一个类中，但是通过查看Python内置模块的源码可以发现，所有的可直接调用的静态方法都直接
    放置在模块内而不是类内部
    '''
