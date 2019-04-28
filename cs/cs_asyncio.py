import wat

import asyncio
from sanicdb import SanicDB

## atdo sql fields_deal
# fields = ['id','uid','*']
# def fields_deal(fieldList):
#     """
#     :param list fieldList:
#     :return:
#     """
#     findStart=False
#     if '*' in fieldList:
#         fieldList.remove('*')
#         findStart=True
#     fieldStr = "`"+'`,`'.join(fields)+"`"
#     if findStart:
#         fieldStr +=',*'
#     return fieldStr
# print(fields_deal(fields))
# exit()

## atdo
# whereList = ['and', {'k': 'id', 'v': 26}, {'k': 'uid', 'v': 2}, {'k': 'name', 'v': '你:"','op':'like'}, ['or', {'k': 't1', 'v': 'v1'}, {'k': 't2', 'v': 'v2'}]]
#
# class where:
#     def __init__(self):
#         """
#
#         """
#         self.sqlData = []
#     def parse(self, whereList):
#         """
#         :param list whereList:
#         :return: str
#         """
#         wList = []
#         joinStr = ''
#         for item in whereList:
#             if isinstance(item, str):
#                 joinStr = item
#             elif isinstance(item, dict):
#                 if 'v' in item and 'k' in item:
#                     if 'op' in item:
#                         vStr = '(`{}` {} %s)'.format(item['k'], item['op'])
#                     else:
#                         vStr = '(`{}` = %s)'.format(item['k'])
#                     wList.append(vStr)
#                     self.sqlData.append(item['v'])
#                 elif 'str' in item:
#                     wList.append(item['str'])
#             elif isinstance(item, (list, tuple)):
#                 whereList.append({'str': '(%s)' % self.parse(item)})
#         if len(wList) == 0:
#             return '1=1'
#         if joinStr in ('and', 'or'):
#             joinStr = (' %s ' % joinStr).join(wList)
#         wat.d(joinStr, self.sqlData)
#         return joinStr
#
# where().parse(whereList)
# exit()

async def cs(loop):
    db = SanicDB('127.0.0.1', 'docs', 'root', 'root', loop=loop)
    r = await db.table_get(
        'note_file',
        # fieldList = ['id', 'uid   as   ddd', '*'],
        # fieldList = [],
        whereList = []
        # whereList = [{'k': 'id', 'v': 26},{'k':'uid','v':1}]
    )
    wat.d(r)

# 获取 EventLoop
loop = asyncio.get_event_loop()
# 执行 coroutine
loop.run_until_complete(cs(loop))
loop.close()
