import wat

class where:
    """
    whereList = ['and', {'f': 'id', 'v': 26}, {'f': 'uid', 'v': 2}, {'f': 'name', 'v': '你:"','op':'like'}, ['or', {'f': 't1', 'v': 'v1'}, {'f': 't2', 'v': 'v2'}]]
    where().parse(whereList)
    """
    def __init__(self, sqlData=[]):
        self.sqlData = sqlData
    def parse(self, whereList):
        """
        :param list whereList:
        :return: str
        """
        wList = []
        joinStr = ''
        for item in whereList:
            if isinstance(item, str):
                joinStr = item
            elif isinstance(item, dict):
                if 'v' in item and 'f' in item:
                    if 'op' in item:
                        vStr = '(`{}` {} %s)'.format(item['f'], item['op'])
                    else:
                        vStr = '(`{}` = %s)'.format(item['f'])
                    wList.append(vStr)
                    self.sqlData.append(item['v'])
                elif 'str' in item:
                    wList.append(item['str'])
            elif isinstance(item, list):
                # whereList.append({'str': '(%s)' % self.parse(item)})
                s = self.parse(item)
                if s != '':
                    whereList.append({'str': '(%s)' % s})
        if len(wList) == 0:
            # return '1=1'
            return ''
        if joinStr in ('and', 'or'):
            joinStr = (' %s ' % joinStr).join(wList)
        elif len(wList) > 1:
            joinStr = (' and ').join(wList)
        else:
            joinStr = wList[0]
        # wat.d(joinStr, self.sqlData)
        return joinStr

whereList = ['and',
             {'f': 'id', 'v': 26},
             {'f': 'uid', 'v': 2},
             {'f': 'name', 'v': '你:"', 'op': 'like'},
             ['or',
              {'f': 't1', 'v': 'v1'},
              {'f': 't2', 'v': 'v2'}
              ]
             ]
whereList = [[], []]
wat.d(where().parse(whereList))

orderList = [{'f': 'id', 'v': 'asc'}, {'f': 'uid', 'v': 'desc'}]
class order:
    """
    atdo [{'f':'id','v':'asc'},{'f':'uid','v':'desc'}]
    """
    def __init__(self):
        self.orders = []
    def parse(self, orderList):
        if len(orderList) == 0:
            return ''
        for item in orderList:
            self.orders.append("`%s` %s" % (item['f'], item['v']))
        return 'order by %s' % ', '.join(self.orders)
# wat.d(order().parse(orderList))
