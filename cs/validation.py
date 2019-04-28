import wat

from validator import Default, Required, Not, Truthy, Blank, Range, Equals, \
    In, validate, GreaterThan, TypeofInt, InstanceOf, Contains, If, Then

# print(isinstance("sd",(int,str)))

# rules = {
#     "limit": [Required, Equals(123)],  # foo must be exactly equal to 123
#     "page": [Required, TypeofInt, Truthy()],  # bar must be equivalent to True
#     "baz": [GreaterThan(0), In(["spam", "eggs", "bacon"])],  # baz must be one of these options
#     "qux": [Not(Range(1, 100))],  # qux must not be a number between 1 and 100 inclusive
#     "ddd": [TypeofInt, Default(333), Not(Range(1, 100))],
# }
#
# # then this following dict would pass:
# passes = {
#     "limit": 123,
#     "page": -2,
#     "foo": 3,
#     "baz": 3,
#     "qux": 1
# }
# wat.d(validate(rules, passes))
# wat.d(passes)

r = {
    "where": [Default([]), InstanceOf(list)],
}
d = {
    'where': ['and', {'k': 'id', 'v': 2},[{'f': 'id', 'v': 2},{'f': 'id', 'v': 2,'str':'22'}]]
}
wat.d(validate(r, d))

class whereValid():
    def __init__(self):
        self.valid = True
    def doit(self, whereItem):
        for k, vItem in enumerate(whereItem):
            if isinstance(vItem, dict):
                if 'f' in vItem and 'v' in vItem:
                    if 'str' not in vItem:
                        pass
                    else:
                        self.valid = False
                        vItem['err'] = 'has f,v should not has str'
                elif 'str' in vItem:
                    pass
                else:
                    self.valid = False
                    vItem['err'] = 'there should be f,v or str'
            elif isinstance(vItem, list):
                self.doit(vItem)

wv = whereValid()
wv.doit(d['where'])
if not wv.valid:
    wat.d(d)
