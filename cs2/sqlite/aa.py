# from pysqlcipher import dbapi2 as sqlite
import sqlite3 as sqlite
import os

os.remove('test.db')

conn = sqlite.connect('test.db')

c = conn.cursor()

# c.execute("PRAGMA key='test'")
c.execute('''create table stocks (date text, trans text, symbol text, qty real, price real)''')
print c.execute('''select count(*) as num from stocks''').fetchone()[0]

c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
print 1
c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
print 1
c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")
print 1
print c.execute('''select count(*) as num from stocks''').fetchone()[0]

conn.commit()
c.close()
