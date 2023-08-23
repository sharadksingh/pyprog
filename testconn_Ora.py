import cx_Oracle

con = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/BGH6')
cur = con.cursor()
print(con)
