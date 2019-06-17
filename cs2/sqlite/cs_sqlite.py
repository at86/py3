# encoding=utf8

from pysqlcipher import dbapi2 as sqlite

# import sqlite3

import traceback
import sys
import json
import wat

conn = sqlite.connect('cs_sqlite.db')
# can access by column name
conn.row_factory = sqlite.Row

c = conn.cursor()

# c.execute("PRAGMA key='test'")

c.execute("pragma table_info('stocks')")
# print 'pragma:',c.fetchmany()
print 'table_info:', c.fetchall()
'''
(0, u'date', u'text', 0, None, 0), (1, u'trans', u'text', 0, None, 0)
sqlite> pragma table_info('stocks');
cid      name          type     notnull  dflt_value  pk     
The table named in the table_info pragma can also be a view.
'''

c.execute("pragma index_list('stocks')")
print 'index_list:', c.fetchall()
'''
[(0, u'text', 0, u'c', 0)]
A sequence number assigned to each index for internal tracking purposes.
> The name of the index.
> "1" if the index is UNIQUE and "0" if not.
> "c" if the index was created by a CREATE INDEX statement, 
    "u" if the index was created by a UNIQUE constraint, 
    or "pk" if the index was created by a PRIMARY KEY constraint.
> "1" if the index is a partial index and "0" if not.
'''

# create [unique] index index_name on table_name(indexed_column);
try:
    c.execute("create index text on stocks(date);")
except Exception, e:
    print(e.message)  # index text already exists
    # print "Error '%s' happened on line %d" % (e[0], e[1][1])
    # print sys.exc_info()[0], sys.exc_info()[1]
    # traceback.print_exc()
    # print(traceback.format_exc()) # use this for exception report

c.execute("select count(*) from sqlite_master where type='table' and name = 'stocks'")
if c.fetchone()[0] == 0:
    c.execute('''create table stocks (date text, trans text, symbol text, qty real, price real)''')

c.execute('''delete from stocks''')
c.execute('''insert into stocks values ('2006-01-05',"你好",'RHAT',100,35.14)''')
c.execute('''select * from stocks''')
row = c.fetchone()
print row[0], '   ', row['date']
print row

wat.d(dict(row))
wat.d(json.dumps(dict(row), ensure_ascii=False))

print c.execute('''select count(*) as num from stocks''').fetchone()[0]

c.close()

conn.commit()
conn.close()
