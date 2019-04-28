# encoding=utf-8

# from flask import Flask
import sqlite3

# def get_data(id):
def get_data():
    conn = sqlite3.connect('./cs_sqlite.db')

    # id=int(id)

    query_sql = 'select * from stocks'

    ##进行查询
    tem=[]

    # query = conn.execute(query_sql  % id)
    query = conn.execute(query_sql)
    for i in query:
        tem.append(i)
        break
    conn.close()
    return tem

# d = get_data()
# print d
