# coding:utf8

#
# aa=None
#
# def d():
#     aa=23
#
# def e():
#     print aa
#
# d()
#
# e()


s='1234你好　'
print s.__len__()
print s.decode('utf-8').__len__()
print s.decode('utf-8').encode('gbk').__len__()