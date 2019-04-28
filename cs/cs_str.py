import wat

s1 = "锄禾日当午abcd"
wat.d(s1[2:3])
wat.d(s1[3:])
wat.d(len(s1))

wat.d('%s is %%s' % 'abc')
wat.d('{} is %s' .format('abc') )
wat.d('{a} is %s' .format(a='abc') )
