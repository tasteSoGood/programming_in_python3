#-*-coding: utf-8-*-
'''
实现一个组合数据类型SortedList
'''

_identity = lambda x: x

class SortedList:
    def __init__(self, sequence = None, key = None):
        self.__key = key or _identity
        '''
        对这句话的理解是，如果key = None, 返回_identity；否则返回key
        要注意，这里的or并不是返回一个布尔值的操作，而是可以返回一个实体的，不过它的判断条件比if语句要弱
        仅当前者为None或False时才返回后者
        '''
        assert hasattr(self.__key, "__call__")
        if sequence is None:
            self.__list = []
        elif isinstance(sequence, SortedList) and sequence.key == self.__key:
            self.__list = sequence.__list[:]
        else:
            self.__list = sorted(list(sequence), key = self.__key)
    
    @property
    def key(self):
        return self.__key

    def add(self, value):
        index = self.__bisect_left(value)
        if index == len(self.__list):
            self.__list.append(value)
        else:
            self.__list.insert(index, value)

    def __bisect_left(self, value):
        # 二分查找
        key = self.__key(value)
        left, right = 0, len(self.__list)
        while left < right:
            middle = (left + right) // 2
            if self.__key(self.__list[middle]) < key:
                left = middle + 1
            else:
                right = middle
        return left
    
    def remove(self, value):
        index = self.__bisect_left(value)
        if index < len(self.__list) and self.__list[index] == value:
            del self.__list[index]
        else:
            raise ValueError("{0}.remove(x): x not in list".format(self.__class__.__name__))

    def remove_every(self, value):
        count = 0
        index = self.__bisect_left(value)
        while index < len(self.__list) and self.__list[index] == value:
            del self.__list[index]
            count += 1
        return count

    def count(self, value):
        count = 0
        index = self.__bisect_left(value)
        while index < len(self.__list) and self.__list[index] == value:
            index, count = index + 1, count + 1
        return count

    def index(self, value):
        index = self.__bisect_left(value)
        if index < len(self.__list) and self.__list[index] == value:
            return index
        raise ValueError("{0}.index(x): x not in list".format(self.__class__.__name__))

    def __delitem__(self, index):
        # 定义del L[i]的行为
        del self.__list[index]

    def __gettiem__(self, index):
        return self.__list[index]

    def __settiem__(self, index):
        # 禁用重写位置的操作
        return TypeError("use add() to insert a value and rely on the list to put it in the right place")

    def __iter__(self):
        return iter(self.__list)

    def __reversed__(self):
        # 提供对内置reversed函数的支持
        return reversed(self.__list)

    def __contains__(self, value):
        index = self.__bisect_left(value)
        return index < len(self.__list) and self.__list[index] == value

    def clear(self):
        self.__list = []
    
    def pop(self, index = -1):
        return self.__list.pop(index)

    def __len__(self):
        return len(self.__list)

    def __str__(self):
        return str(self.__list)

    def copy(self):
        return SortedList(self, self.__key)

    __copy__ = copy # 保证在使用copy.copy()方法的时候也能调用self.copy()函数
    