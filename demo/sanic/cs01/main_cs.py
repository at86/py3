import wat
import requests
from validator import Default, Required, \
    Not, Truthy, Blank, Range, Equals, In, \
    GreaterThan, validate, InstanceOf

headers = {'Content-Type': 'application/json'}

url = 'http://127.0.0.1:8000/sss'
d = {
    # 'k0': 3,
    'k1': {
        # =====================
        # 'table': 1,
        # 'type': 3,
        # 'fieldList': 23,
        # =====================
        'table': 'note_file',
        'type': 'getList',
        'fieldList': ['id', 'name'],

        # 'whereList': [{'f': 'id', 'v': 26}],
        # 'whereList': [{'f': 'id', 'v': 26},{'ff': 'name', 'op': 'like', 'v': '%js%'},[{'f': 'id', 'v': 26},{'f': 'name', 'v': '%js%','str':'23'}]],
        'orderList': [{'f': 'id', 'v': 'desc'}],
        'offset': 3,
        'limit': 3,
    },
    'a1': {
        'table': 'note_file',
        'type': 'getOne',
        'fieldList': ['id', 'uid as ddd'],
        # 'orderList': [1, 3],
        'orderList': [{'f': 'id', 'v': 'desc'}],
    },
}
response = requests.post(url, data=wat.json(d), headers=headers)
print(response.text)

# url = 'http://127.0.0.1:8000/ajaxAt/process/nodeEditDo'
# response = requests.post(url, headers=headers)
# print(response.text)
