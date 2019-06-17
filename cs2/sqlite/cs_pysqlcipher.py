import time
import os

from pysqlcipher import dbapi2 as sqlite
# import sqlite3 as sqlite

# os.remove('cs_pysqlcipher.db')

conn = sqlite.connect('cs_pysqlcipher.db', isolation_level=None) #, isolation_level=None
# can access by column name
conn.row_factory = sqlite.Row

c = conn.cursor()


c.execute("PRAGMA key='test'")
print c.execute('''select count(*) as num from stocks''').fetchone()[0]

# c.execute('''create table stocks (date text, trans text, symbol text, qty real, price real)''')
# c.execute("""insert into stocks values ('2006-01-05','BUY','RHAT',100,35.14)""")

# c.execute("""delete from stocks""")
print 3

for i in range(2):
    print i
    d = time.ctime()
    c = conn.cursor()

    c.execute("PRAGMA key='test'")
    c.execute("insert into stocks values ('%s','2006-01-05','RHAT',100,35.14)"%(d))
    c.close()
print 4

c.execute("""select * from stocks""")
row = c.fetchone()
print row[0], '   ', row['date']
print 5
print row
print c.execute('''select count(*) as num from stocks''').fetchone()[0]
print 6


conn.commit()
c.close()
