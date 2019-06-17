"""
Python数据验证库(一) validators - 简书 https://www.jianshu.com/p/2babed54b496
Python数据验证库（二）validator - 简书 https://www.jianshu.com/p/eee56214af9c
Python数据验证库（三）voluptuous - 简书 https://www.jianshu.com/p/0a5047a04ffd
"""


from validator import Default, Required, Not, Truthy, \
    Blank, Range, Equals, In, validate, InstanceOf, \
    GreaterThan, LessThan, \
    whereValid, orderValid

import wat
import time

d = {
    "a1": {
        "a1-1": 1,
        "a1-4": {
            "a1-4-1":4
        },
    },
    'a2':3
}
rules = {
    "addtime": [Default(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))],
    "sx": [Default(999)],
    "fid": [Default(1)],
    "pid": [Default(1)],
    "name": [Default("请添加节点标题")],
    "type": [Default(3)],
    "a1": [
        {"a1-1": [GreaterThan(2)]},
        {"a1-2": [Default(4)]},
        {"a1-3": [
            Default({}),
            {"a1-3-1": [
                Default(3),
            ]},
        ]},
        {'a1-4':[
            {'a1-4-1':GreaterThan(5)}
        ]},
    ],
    'a2':[GreaterThan(5),InstanceOf(float)],
}
vd = validate(rules, d)
wat.d(vd, d)



# 嵌套验证
validator = {
    "foo": [Required, Equals(1)],
    "bar": [Required, {
        "baz": [Required, Equals(2)],
        "qux": [Required, {
            "quux": [Required, Equals(3)]
        }]
    }
            ]
}
test_case = {
    "foo": 1,
    "bar": {
        "baz": 2,
        "qux": {
            "quux": 3
        }
    }
}
vd = validate(validator, test_case)
wat.d(vd, test_case)
