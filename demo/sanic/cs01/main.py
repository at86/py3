import os
import sys

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "lib"))

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
    whereValid,orderValid

# import compileall
# compileall.compile_dir(r'C:\python3\Lib\asyncio')

from sanicdb import SanicDB

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
    if not getattr(sys, 'frozen', False):
        traceback.print_exc()
    return json({'tip': exception.msg, 'r': exception.code})
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

# region process's api

def rtnJson(d, r=0, tip='执行成功'):
    # json() is a httpResponse
    return json({'r': r, 'tip': tip, 'd': d}, ensure_ascii=False, indent=2)

def toDict(form):
    d = {}
    for k in form:
        d[k] = form.get(k)
    return d


@app.route('/<requrl>', methods=["POST"])
async def getData(request, requrl):
    """atdo 文档新增 (totest)"""
    rules = {
        "table": [Required, InstanceOf(str)],
        "type": [Required, In(['getOne', 'getList'])],
        "fieldList": [Default(['*']), InstanceOf(list)],
        "whereList": [Default([]), InstanceOf(list)],
        "orderList": [Default([]), InstanceOf(list)],
        "offset": [Default(0), InstanceOf(int)],
        "limit": [Default(0), InstanceOf(int)],
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
                one=v['type'] == 'getOne',
            )
            d[k] = {
                'r': 0,
                'data': row,
            }
        return rtnJson({'data': d, 'requrl': requrl})
    else:
        return rtnJson({'data': errData, 'requrl': requrl}, 1, '校验出错')


@app.route('/ajaxAt/process/nodeAddDo', methods=["POST"])
async def ajaxAt_process_nodeAddDo(request):
    """atdo 文档节点新增 (totest)"""
    d = toDict(request.form)
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
    id = await db.table_insert('note_node', d)
    return rtnJson({'id': id})

@app.route('/ajaxAt/process/nodeEditDo', methods=["POST"])
async def ajaxAt_process_nodeEditDo(request):
    """atdo 文档节点更新"""
    d = toDict(request.form)
    d['uptime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    await db.table_update('note_node', d, [{'k': 'id', 'v': 26}])  # 26
    return rtnJson({'id': 26})

@app.route('/ajaxAt/process/fileAddDo', methods=["POST"])
async def ajaxAt_process_fileAddDo(request):
    """atdo 文档新增 (totest)"""
    d = toDict(request.form)
    d['addtime'] = int(time.time())
    d['uptime'] = int(time.time())
    id = await db.table_insert('note_file', d)
    return rtnJson({'id': id})

@app.route('/ajaxAt/process/fileEditDo', methods=["POST"])
async def ajaxAt_process_fileEditDo(request):
    """atdo 文档更新"""
    d = toDict(request.form)
    d['uptime'] = int(time.time())
    await db.table_update('note_file', d, 'id', 26)  # 26
    return rtnJson({'id': 26})

@app.route('/ajaxAt/process/fileGetDo', methods=["GET"])
async def ajaxAt_process_fileGetDo(request):
    """atdo 文档详情"""
    r = await db.get('select * from note_file where id=%s', 26)  # 26
    return rtnJson(r)

@app.route('/ajaxAt/process/fileListDo', methods=["GET"])
async def ajaxAt_process_fileListDo(request):
    """atdo 文档列表"""
    d = toDict(request.args)
    rules = {
        "limit": [Default(10), Range(1, 1000)],
        "page": [Default(1), GreaterThan(0)],
    }
    vd = validate(rules, d)
    if not vd.valid:
        # atdo json() is a httpResponse
        # raise myException(json(vd.errors), -1)
        raise wat.myException(vd.errors, -1)
    fromNum = (d['page'] - 1) * d['limit']
    rs = await db.query('select id,addtime,uptime,name,type,mode,del from note_file order by del asc, uptime desc limit %s, %s',
                        fromNum, d['limit'])
    # wat.d(rs)
    # r = await db.get('select * from note_file where id=%s', 26)  # 26
    return rtnJson(rs)

@app.route('/ajaxAt/process/fileUpSxDo', methods=["POST"])
async def ajaxAt_process_fileUpSxDo(request):
    """atdo 文档列表 (totest)"""
    d = toDict(request.form)
    upSql = 'case id'
    for k, v in enumerate(d['sx']):
        upSql += ' when %s then %s' % (v, k)
    upSql += ' end'
    upSql = 'update note_file set sx= %s where id in(%s)' % (upSql, ','.join(d['sx']))
    rs = await db.execute(upSql)
    return rtnJson(rs)



# endregion

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
    # debug=True, access_log=True,
    # app.run(host="127.0.0.1", port=8000, auto_reload=True)
    # app.run(debug=True)
