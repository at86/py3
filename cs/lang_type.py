import wat

try:
    wat.d('a' < 0)
except Exception as e:
    wat.d(str(e))

wat.d(isinstance(1, int))
wat.d(isinstance('1', str))
wat.d(isinstance(0, bool), isinstance(True, bool))

wat.d(isinstance((1, 2), tuple))
wat.d(isinstance([1, 2], list))
wat.d(isinstance({"a": 1, "b": 2}, dict))

