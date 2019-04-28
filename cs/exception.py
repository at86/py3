import wat

# """
# atdo Exception
# """
class myException(Exception):
    def __init__(self, msg, num):
        self.msg = msg
        self.num = num
try:
    raise myException('aaaa', 3)
except myException as e:
    print('------')
    wat.d(e.msg, e.num)
