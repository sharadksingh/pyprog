# test.py

import oracledb
import os

connection = oracledb.connect(user="hr", password="hpv185e",host="10.143.100.36", port=1521, service_name="bgh6")
with connection.cursor() as cursor:
        sql = """select sysdate from dual"""
        for r in cursor.execute(sql):
            print(r)
