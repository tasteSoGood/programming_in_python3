'''
Python面向对象中，私有化是一个问题，它没有Java和C++中的private限定词，但Python使用的是特殊的命名法来给出私有成员

比如有一个类成员student

self.student 表示公有成员，相当于Java中的public
self._student 表示能被子类继承之后访问，并且能作为类方法在外部调用，但不能作为单独的变量导入
self.__student 表示私有成员，无法在外部直接访问
'''
import math

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        return math.hypot(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Point({0.x!r}, {0.y!r})".format(self)

    def __str__(self):
        return "({0.x!r}, {0.y!r})".format(self)

class Circle(Point):
    def __init__(self, radius, x = 0, y = 0):
        super().__init__(x, y)
        self.__radius = radius
    
    # @property修饰词说明这个函数是可以作为属性调用的，当然，一旦作为属性以后，这个函数就是“只读”的了，不能再传入参数或者作为函数调用
    # 将函数作为属性的好处是显然的，当作为一个正常属性的时候，如果属性1依赖属性2，当属性2发生了变化，属性1不会变化，而作为函数，在任何
    # 场合的调用都会进行一次计算，可以做到实时更新
    @property
    def edge_distance_from_origin(self):
        return abs(self.distance_from_origin() - self.radius)

    @property
    def area(self):
        return math.pi * (self.__radius ** 2)

    def circumference(self):
        return 2 * math.pi * self.__radius

    def __eq__(self, other):
        return self.__radius == other._radius and super().__eq__(other)

    def __repr__(self):
        return 'Circle({0.__radius!r}, {0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return repr(self)

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, radius):
        '''
        assert关键字的作用是，判断一个条件的正误，正确则继续执行，错误则终止程序并抛出一个错误。
        该错误可以有一个说明，也就是逗号后面的那部分
        这一语句在逻辑上相当于

        if not condition:
            raise ...

        >>> assert 1 == 0, "This is a false condition."
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        AssertionError: This is a false condition.
        '''
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius

    '''
    从面向对象的角度来说，上面这个类中的__radius变量是属于私有的，不应该被外界访问，或者应该对访问加以限制
    @property属性可以将一个函数修饰为只读的属性，当然，我们在内部可以直接修改__radius属性，这不存在问题，但
    如果想在外部修改__radius属性就会出现问题

    >>> c = Shape.Circle(5)
    >>> c.radius
    5
    >>> c.radius = 6
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: can't set attribute
    
    上面的情况是在没有定义@radius.setter函数的情况下产生的，Python的面向对象机制会阻止外界修改这个变量，而且
    如果在外部直接访问__radius变量会报错

    >>> c.__radius
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Circle' object has no attribute '__radius'

    @radius.setter修饰器的作用就是向外界提供一个修改__radius变量的接口

    >>> c = Shape.Circle(5)
    >>> c.radius
    5
    >>> c.radius = 6
    >>> c.radius
    6

    这是符合面向对象中的数据屏蔽概念的
    '''
