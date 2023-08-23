import cx_Oracle
import os
import platform
import sys

print(sys.version)
#print(os.environ['ORACLE_HOME'])
print(os.environ['path'])


LOCATION = r"c:\oracle\instantclient_12_1"
print("ARCH:", platform.architecture())
print("FILES AT LOCATION:")
for name in os.listdir(LOCATION):
    print(name)

#os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"]


con = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/BGH6')
print (con.version)

con.close()

