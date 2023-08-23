# test.py

import oracledb
#import os

oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_12_1")

#un = os.environ.get('PYTHON_USERNAME')
#pw = os.environ.get('PYTHON_PASSWORD')
#cs = os.environ.get('PYTHON_CONNECTSTRING')

un = 'bgh'
pw = 'hpv185e'
cs = '10.143.100:36:1521/bgh6'

#con = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/BGH6')



#with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
#with oracledb.connect('bgh/hpv185e@10.143.100.36:1521/BGH6') as connection:
with oracledb.connect(user='bgh', password='hpv185e', dsn='10.143.100.36:1521/BGH6') as connection:

    with connection.cursor() as cursor:
        sql = """select sysdate from dual"""
        for r in cursor.execute(sql):
            print(r)
