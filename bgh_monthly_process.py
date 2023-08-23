# This program has the following function:
# 1. A file named MEDKKSMMYY.txt is received from EDP Every Month
# 2. This file contains the details of the Guarantors updated balance Payment
# 3. This data is loaded in a table named : ADM_EDP_RECOVERIES
# 4. Then a procedure is run that updates the ADM_EDPGRT table that contains the guarantor details
# 5. The Procedure name is : update_adm_edpgrt
# Written By: Sharad Kumar Singh on 30.08.2017
# Furhter Enhancement : The program shall run as a service and as soon as the the CSV file dropped at the location
# shall be loaded into the table. This is possible through polling lets expllore that

import sys
import csv
import cx_Oracle
import os

#a_file = open(data_file)  
#data = a_file.readlines()  
#for a_line in data:  
#  record_type = a_line[:3]  
#  parcel_num = a_line[3:11]  
#  the_rest = a_line[11:]  
#  print record_type, parcel_num, the_rest  

#a_file = open(data_file)  
#data = a_file.readlines()  
#for a_line in data:  
#  record_type = a_line[:3]  
#  parcel_num = a_line[3:11]  
#  the_rest = a_line[11:]  
#  print record_type, parcel_num, the_rest  

# Connection to Oracle
con  = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = con.cursor()
ver=con.version.split(".")
cur=con.cursor()
'''
array=[]
a_file = open("F:\pyora\edp\medkks0817.txt", "r")
data   = a_file.readlines()
for a_line in data:
    staff_no = a_line[0:6]
    hospno   = a_line[6:11]
    hospx    = a_line[11:13]
    hospyr   = a_line[13:15]
    balance  = a_line[15:21]
    balx     = a_line[21:23]
    inst     = a_line[23:27]
    instx    = a_line[27:29]
    billx    = a_line[29:38]
    billno   = a_line[38:43]
    array.append ((staff_no, hospno, hospx, hospyr, balance, balx, inst, instx, billx, billno))
'''
#    print(staff_no, hospno, hospx, hospyr, balance, balx, inst, instx, billx, billno)


#    cur.execute("INSERT INTO ADM_EDP_RECOVERIES(STAFFNO, HOSPNO, HOSPX, HOSPYR, BALANCE, BALX, INST, INSTX, BILLX, BILLNO, DATA_LOAD_ON) VALUES (staff_no,hospno, hospx, hospyr, balance, balx, inst, instx, billx, billno, TRUNC(SYSDATE))")
#    cur.execute(stat,staff_no, hospno, hospx, hospyr, balance, balx, inst, instx, billx, billno)
#cur.executemany("INSERT INTO STOPPED_RECOVERIES(M05_ID, M05_BILL_YYMM, M05_LOCATION, M05_STAFF, M05_BILL_NO, M05_BILL_AMT, M05_CUM_AMT_RECVRD, M05_BALANCE, M05_INST, M05_CURR_RCVY, M05_NOR, M05_BILLYR, M05_BILLMM, M05_BILLDD, M05_HOSP_NO,M05_DROPMMYY) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16)", lines)
#cur.executemany("INSERT INTO ADM_EDP_RECOVERIES(STAFFNO, HOSPNO, HOSPX, HOSPYR, BALANCE, BALX, INST, INSTX, BILLX, BILLNO) VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)",array)
#cur.executemany("INSERT INTO ADM_EDP_RECOVERIES(STAFFNO, HOSPNO, HOSPX, HOSPYR, BALANCE, BALX, INST, INSTX, BILLX, BILLNO, DATA_LOAD_ON) VALUES (:staff_no,:hospno,:hospx,:hospyr,:balance,:balx,:inst,:instx,:billx,:billno,TRUNC(SYSDATE))",array)

# Update the BGH_DOCTDIC so that the Doctor Database is updated
cur.execute("update bgh_doctdic set blocked='Y', REMARKS='RETIRED' where staff in (select stno from emp_master where roll_stat='N') and blocked='N' ")
#    Update On Roll Employee and Dependents
l_query = cur.callproc('bgh_mid_update_new_daily');
#    Update Not On Roll Employees and Spouse
l_query = cur.callproc('bgh_mid_update_nor_daily');

con.commit ()


#a_file.close()

## Calling the Oracle Stored Procedure UPDATE_COMPLETED_RECOVERIES
#l_query = cur.callproc('update_adm_edpgrt')
cur.close()


#os.rename("F:\pyora\edp\medkks0817.txt", "F:\pyora\edp\edp_arch\medkks0817.txt.arc")
