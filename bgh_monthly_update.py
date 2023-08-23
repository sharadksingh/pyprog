# Program Name: bgh_Monthly_update.py
# Scheduler   : BGH_BILL_DETAILS_MM
# All tables that are to be updated at the begining of the month goes here 
# Written By: Sharad Kumar Singh on 31.12.2018

import sys
import csv
import cx_Oracle
import os



# Connection to Oracle
con  = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = con.cursor()
ver=con.version.split(".")
cur=con.cursor()
#cur.execute("insert into ward_refund_number(REF_YEAR,REF_MONTH,REF_START_NUMBER,REF_CURR_NUMBER) values (2019, 01, 1, 0")
cur.execute("insert into ward_refund_number(ref_year, ref_month, ref_start_number, ref_curr_number) values(to_char(sysdate,'YYYY'), to_char(sysdate,'MM'), 1, 0)")
#cur.execute("insert into ward_refund_number(ref_year, ref_month, ref_start_number, ref_curr_number) values(2019,01,1,0")
#cur.execute("insert into ward_refund_number(ref_year, ref_month, ref_start_number, ref_curr_number) values()")
con.commit ()
cur.close()


