#coding:utf-8

#lambada 面试题

li = [lambda :x for x in range(10)]
print li
print li[0]
res = li[0]()
print(res)
print(li[1]())

for i in li:
    print i()

#输出：9


print '============='
li = [(lambda x=x: x) for x in range(3)]
print li
print li[0]
for i in li:
    print i()
