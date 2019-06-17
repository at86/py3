_ = {
  'desc':'节点添加',
  'params':{
    'addtime': {
      'doc':'添加时间',
      'rules': [
        {'default': {'dateTime': 'Y-m-d H:M:S'}},
      ]
    },
    'sx': {
      'doc':'排列顺序',
      'rules': [
        {'default': {'int': 999}},
      ]
    },
    'fid': {
      'doc':'归属的file的id',
      'rules': [
        {'default': {'int': 1}},
      ]
    },
    'pid': {
      'doc':'归属的parent node的id',
      'rules': [
        {'default': {'int': 1}},
      ]
    },
    'name': {
      'doc':'节点的名称',
      'rules': [
        {'default': {'str': '请添加节点标题'}},
      ]
    },
    'type': {
      'doc':'节点类型 3:text; 4:codemirror',
      'rules': [
        {'default': {'int': 3}},
      ]
    },
  }
}
