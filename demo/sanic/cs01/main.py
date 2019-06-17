import os
import sys
import demjson

# sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

import wat

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler
from sanic.log import logger

from sanic.response import text
from sanic.response import file
from sanic.response import raw
from sanic.response import json

import traceback

import sqlite3
import time
import asyncio

from validator import Default, Required, Not, Truthy, \
    Blank, Range, Equals, In, GreaterThan, validate, InstanceOf, \
    whereValid, orderValid

# import compileall
# compileall.compile_dir(r'C:\python3\Lib\asyncio')

from sanicdb import SanicDB

# atdo 190522
# from websockets import WebSocketCommonProtocol
# from websockets import State
from sanic.websocket import ConnectionClosed

# 上面的 ConnectionClosed 实际是 from websockets.exceptions import ConnectionClosed

# app = Sanic()
app = Sanic('test', log_config=None)
# app.config.KEEP_ALIVE = False
db = SanicDB('127.0.0.1', 'docs2', 'root', 'root', sanic=app)

# region excepton deal
# atdo ok 1
async def server_error_handler(request, exception):
    """
    :param sanic.request.Request request:
    :param myException exception:
    :return:
    """
    wat.d('3333  server_error_handler')
    if not getattr(sys, 'frozen', False):
        traceback.print_exc(limit=1, )

    if hasattr(exception, 'msg') and hasattr(exception, 'code'):
        return json({'tip': exception.msg, 'r': exception.code})
    else:
        return json({'tip': str(exception), 'r': -1})
app.error_handler.add(Exception, server_error_handler)

# atdo ok 2
# class CustomErrorHandler(ErrorHandler):
#     def default(self, request, exception):
#         """
#         :param sanic.request.Request request:
#         :param myException exception:
#         :return:
#         """
#         return json({'msg': exception.msg, 'code': exception.code})
# app.error_handler = CustomErrorHandler()
# endregion

# region process's api

def rtnJson(d, r=0, tip='执行成功'):
    # json() is a httpResponse
    return json({'r': r, 'tip': tip, 'd': d}, ensure_ascii=False, indent=2)

def toDict(form):
    d = {}
    for k in form:
        d[k] = form.get(k)
    return d

# atdo ws
@app.websocket('/wsreq')
async def feed(request, ws):
    try:
        while True:
            # if ws.state == WebSocketCommonProtocol.State.CLOSING:
            # print(ws.open,ws.state)
            # if not ws.open:
            # 偶尔不是关闭
            # print(ws.state)
            # if ws.state == State.CLOSING:
            #     return
            data = await ws.recv()
            print('recv: ' + data)
            print('send back: ' + data)
            await ws.send(data*1000)
    except ConnectionClosed as ex:
        print('closed.........')
    except Exception as e:
        print('exception: ' + e.__str__())

# atdo requrl is variable
@app.route('/getdata/<requrl>', methods=["POST"])
async def getData(request, requrl):
    """atdo 文档新增 (totest)"""
    rules = {
        "table": [Required, InstanceOf(str)],
        "getOne": [Default(True), In([False, True])],
        "fieldList": [Default(['*']), InstanceOf(list)],
        "whereList": [Default([]), InstanceOf(list)],
        "orderList": [Default([]), InstanceOf(list)],
        "offset": [Default(0), InstanceOf(int), GreaterThan(0, True)],
        "limit": [Default(0), InstanceOf(int), GreaterThan(0, True)],
    }
    d = request.json

    errData = {}
    valid = True
    for k in d:
        v = d[k]  # not use `for k, v in enumerate(d):` becase: RuntimeError: dictionary changed size during iteration
        if not isinstance(v, dict):
            wat.sqlErrDeal(errData, k, 'err', {k: ['should be object']})
            valid = False
            continue

        vd = validate(rules, v)
        if not vd.valid:
            wat.sqlErrDeal(errData, k, 'err', vd.errors)
            valid = False
            continue
        if len(v['whereList']) > 0:
            wv = whereValid()
            wv.doit(v['whereList'])
            if not wv.valid:
                wat.sqlErrDeal(errData, k, 'err', wv.errors)
                valid = False
                continue
        if len(v['orderList']) > 0:
            wv = orderValid()
            wv.doit(v['orderList'])
            if not wv.valid:
                wat.sqlErrDeal(errData, k, 'err', wv.errors)
                valid = False
                continue

    if valid:
        for k in d:
            v = d[k]
            row = await db.table_get(
                v['table'],
                fieldList=v['fieldList'],
                whereList=v['whereList'],
                orderList=v['orderList'],
                offset=v['offset'],
                limit=v['limit'],
                getOne=v['getOne'],
            )
            d[k] = {
                'r': 0,
                'data': row,
            }
        return rtnJson({'data': d, 'requrl': requrl})
    else:
        return rtnJson({'data': errData, 'requrl': requrl}, 1, '校验出错')

# region 节点：新增；更新；
@app.route('/ajaxAt/process/nodeAddDo', methods=["POST"])
async def ajaxAt_process_nodeAddDo(request):
    """atdo 文档节点新增 (totest)"""
    d = request.json
    rules = {
        "addtime": [Default(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))],
        "sx": [Default(999)],
        "fid": [Default(1)],
        "pid": [Default(1)],
        "name": [Default("请添加节点标题")],
        "type": [Default(3)],
    }
    vd = validate(rules, d)
    if not vd.valid:
        raise wat.myException(vd.errors, -1)
    fid = await db.table_insert('note_node', d)
    return rtnJson({'id': fid})

@app.route('/ajaxAt/process/nodeEditDo', methods=["POST"])
async def ajaxAt_process_nodeEditDo(request):
    """atdo 文档节点更新"""
    d = request.json
    d['uptime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    await db.table_update('note_node', d, [{'f': 'id', 'v': d['id']}])
    return rtnJson({'id': d['id']})
# endregion

# region 文件：新增；更新；获取；列表；排序；
@app.route('/ajaxAt/process/fileAddDo', methods=["POST"])
async def ajaxAt_process_fileAddDo(request):
    d = toDict(request.form)
    d['addtime'] = int(time.time())
    d['uptime'] = int(time.time())
    fid = await db.table_insert('note_file', d)
    return rtnJson({'id': fid})

@app.route('/ajaxAt/process/fileEditDo', methods=["POST"])
async def ajaxAt_process_fileEditDo(request):
    d = request.json
    d['uptime'] = int(time.time())
    await db.table_update('note_file', d, [{'f': 'id', 'v': d['id']}])  # 26
    return rtnJson({'id': 26})

@app.route('/ajaxAt/process/fileGetDo', methods=["POST"])
async def ajaxAt_process_fileGetDo(request):
    d = request.json
    r = await db.get('select * from note_file where id=%s', d['id'])  # 26
    return rtnJson(r)

@app.route('/ajaxAt/process/fileListDo', methods=["POST"])
async def ajaxAt_process_fileListDo(request):
    d = request.json
    rules = {
        "limit": [Default(10), Range(1, 1000)],
        "page": [Default(1), GreaterThan(0)],
    }
    vd = validate(rules, d)
    if not vd.valid:
        raise wat.myException(vd.errors, -1)
    fromNum = (d['page'] - 1) * d['limit']
    sql = 'select id,addtime,uptime,name,type,mode,del from note_file order by del asc, uptime desc limit %s, %s'
    rs = await db.query(sql, fromNum, d['limit'])
    return rtnJson(rs)

@app.route('/ajaxAt/process/fileUpSxDo', methods=["POST"])
async def ajaxAt_process_fileUpSxDo(request):
    """文档排序"""
    d = request.json
    upSql = ['case id']
    for k, v in enumerate(d['sx']):
        upSql.append('when %s then %s' % (v, k))
    upSql.append('end')
    upSql = " ".join(upSql)
    upSql = 'update note_file set sx= %s where id in(%s)' % (upSql, ','.join(d['sx']))
    rs = await db.execute(upSql)
    return rtnJson(rs)
# endregion

# endregion

# region test code

@app.route('/mysql')
async def index(request):
    sql = 'select sleep(5)'
    print(time.time())
    return json(await db.query(sql), ensure_ascii=False)

@app.route("/sleep")
async def test(request):
    lst = [time.time()]
    # time.sleep(3) #同步
    await asyncio.sleep(2)  # 异步
    lst.append(time.time())
    return json(lst, ensure_ascii=False)


@app.route("/")
async def test(request):
    return text('Hello World!')
    # return json({"hello": "world"})

@app.route("/favicon.ico")
async def test(request):
    return text('')

@app.route("/i.html")
async def test(request):
    return await file("./i.html")

@app.route("/raw")
async def test(request):
    return raw(b"it is raw data")

# region sqlite
async def get_data():
    conn = sqlite3.connect('./cs_sqlite.db')
    query_sql = 'select * from stocks'
    ##进行查询
    tem = []
    # query = conn.execute(query_sql  % id)
    query = conn.execute(query_sql)
    for i in query:
        tem.append(i)
        break
    conn.close()
    return tem

@app.route("/json")
async def test(request):
    d = await get_data()
    return json(d, ensure_ascii=False)
# endregion

# endregion

def run():
    app.static('/static', './static')
    app.run(host="127.0.0.1", port=8000)

if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=8000)
    run()

    # debug=True, access_log=True,
    # app.run(host="127.0.0.1", port=8000, auto_reload=True)
    # app.run(debug=True)
