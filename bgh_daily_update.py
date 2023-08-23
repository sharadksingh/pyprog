# Program Name: bgh_daily_update
# Scheduler   : IPD_ADM_DAILY
# 5. The Procedure name is : update_adm_edpgrt
# Written By: Sharad Kumar Singh on 30.08.2017

import sys
import csv
import cx_Oracle
import os



# Connection to Oracle
con  = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = con.cursor()
ver=con.version.split(".")
cur=con.cursor()
#cur.execute("insert into emp_master_aug (select * from emp_master where roll_stat='Y' and stno not in (select stno  from emp_master_aug))")
#cur.execute("insert into emp_pay_detail_aug (select * from emp_pay_detail where stno not in (select stno  from emp_pay_detail_aug))")
#cur.execute("insert into emp_dep_code_aug (select * from emp_dep_code where deptt not in (select deptt  from emp_dep_code_aug))")
# ALl the above three updation has been included in the stored procedure MERGE_EMP_MASTERA_AUG below
l_query = cur.callproc('MERGE_EMP_MASTER_AUG');
# Update the receovery ADM_EDPGRT 
cur.execute("update adm_edpgrt set recovery_completed='Y' where balance < inst and hepaid is null and sent_recovery='Y' and recovery_completed is null and inst is not null")
con.commit ()
cur.close()
