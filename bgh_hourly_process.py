
# Written By: Sharad Kumar Singh on 30.08.2017
# Furhter Enhancement : The program shall run as a service and as soon as the the CSV file dropped at the location
# shall be loaded into the table. This is possible through polling lets expllore that


import sys
import csv
import cx_Oracle
import os


# Connection to Oracle
con  = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = con.cursor()
ver=con.version.split(".")
cur=con.cursor()

# Update the BGH_DOCTDIC so that the Doctor Database is updated
cur.execute("update bgh_doctdic     set blocked='Y', REMARKS='RETIRED' where staff in (select stno from emp_master where roll_stat='N') and blocked='N' ")
cur.execute("update bgh_doctdic_new set blocked='Y', REMARKS='RETIRED' where staff in (select stno from emp_master where roll_stat='N') and blocked='N' ")

#    Update On Roll Employee and Dependents
l_query = cur.callproc('bgh_mid_update_new_daily');
#    Update Not On Roll Employees and Spouse
l_query = cur.callproc('bgh_mid_update_nor_daily');

con.commit ()


cur.close()


