import pymysql

con = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')
cur = con.cursor()
# sql = "SELECT * FROM covering"
sql = "SELECT * FROM covering WHERE 날짜>'2018-01-02'"
cur.execute(sql)
rows = cur.fetchall()

print(type(rows))
for x in rows:
    print(x)
print(len(rows))
print(rows[0])
print(rows[0][0])
print(rows[0][1])
print(rows[0][2])
print(rows[0][3])
print(rows[0][4])
print(rows[0][5])
print(rows[0][6])
print(type(rows[0][5]))

con.close()
