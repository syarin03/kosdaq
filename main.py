import pymysql

con = pymysql.connect(host='10.10.21.116', user='stock_admin', password='admin1234', db='stock', charset='utf8')
cur = con.cursor()
sql = "SELECT * FROM covering"
cur.execute(sql)
rows = cur.fetchall()
print(rows)
con.close()
