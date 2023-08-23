# This program has the following function:
# 1. A file named MEDDROP of type Excel is received from EDP every month
# 2. This file contains the details for which the recovery has been completed
# 3. This data is loaded in a table named : STOPPED_RECOVERIES
# 4. Then a procedure is run that updates the ADM_EDPGRT table that contains the guarantor details
# The CSV file may be preapred from the excel file of the sbi pos data. The CSV file shall contain only three fields
# RRN_NUMBER, TRANS_DATE, TRANS_AMT
# The CSV is saved from excel as CSV (Comma delimited)
# The CSV file has to be sent to the location F:\pyora\bgh\
# The name of the file shall be MEDDROP.csv
# The Heading line of the CSV has to be deleted
# After loading into the SBI_POS_DATA_XX the csv is moved to f:\pyora\sbi\sbi_arch\SBI_POS_DATA_CSV.csv.arc
# Written By: Sharad Kumar Singh on 17.08.2017
# Furhter Enhancement : The program shall run as a service and as soon as the the CSV file dropped at the location
# shall be loaded into the table. This is possible through polling lets expllore that
#
import csv
import cx_Oracle
import os


f = open("F:\pyora\edp\meddrop.csv", "r")
#reader = csv.reader(open("F:\pyora\edp\meddrop.csv","r"))
reader = csv.reader(f)

lines=[]
for line in reader:
      lines.append(line)
#print(lines)
#Output :
#[['Firstname', 'LastName', 'email', 'Course_name', 'status'], ['Kristina', 'Bohn', 'abc@123.com', 'Guide to Capnography in the Management of the Critically Ill Patient (CE)', 'Registered'], ['Peggy', 'Lutz', 'gef@123.com', 'Guide to Monitoring EtCO2 During Opioid Delivery (CE)', 'In Progress']]
#Code to push the list to Oracle table :
#con = cx_Oracle.connect('username/password@tamans*****vd/Servicename')
# Connection to Oracle
con  = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = con.cursor()
ver=con.version.split(".")
#print(ver)

cur=con.cursor()
#for line in lines:
#cur.execute("INSERT INTO MEDICLAIM_MASTER_ENROLL_NEW('CENTRE_CODE','PLANT_CODE','MINNO_E','NAME_E','MF_E','AGE_E','DOB_E','NOMINEE_E','RLTN_E', 'MINNO_S','NAME_S','MF_S','AGE_S','DOB_S','NOMINEE_S','RLTN_S', 'ADD1', 'ADD2','ADD3','ADD4','PINCODE','DATE_SEP','DATE_ENROL','PH','MOB','MAIL_ID','SAIL_PNO','PLANT_PNO','CHEQ_DD_TYPE','CHEQUE_NO','CHEQUE_DT','CHEQUE_AMT','ENROL_TYPE','PREMIUM_EMP','PREMIUM_SP') values (:1,:2,:3,:4,:5,to_char(:6,):7,:8,:9,:10,:11,:12,to_char(:13),:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35)", line)
#cur.executemany("INSERT INTO MEDICLAIM_MASTER_ENROLL_NEW(CENTRE_CODE,PLANT_CODE,MINNO_E,NAME_E,MF_E,AGE_E,DOB_E,NOMINEE_E,RLTN_E,MINNO_S,NAME_S,MF_S,AGE_S,DOB_S,NOMINEE_S,RLTN_S, ADD1, ADD2,ADD3,ADD4,PINCODE,DATE_SEP,DATE_ENROL,PH,MOB,MAIL_ID,SAIL_PNO,PLANT_PNO,CHEQ_DD_TYPE,CHEQUE_NO,CHEQUE_DT,CHEQUE_AMT,ENROL_TYPE,PREMIUM_EMP,PREMIUM_SP) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35)", lines)
#cur.executemany("INSERT INTO SBI_POS_DATA_XX(RRN_NUMBER, TRANS_DATE, TRANS_AMT, LOAD_DATE, RRN_DATE) values (:6,:9,:11,:11,:12)", lines)
#cur.executemany("INSERT INTO STOPPED_RECOVERIES(RRN_NUMBER, TRANS_DATE, TRANS_AMT, load_date, rrn_date) values (:1,to_date(:2,'DD-MM-YYYY'),:3, trunc(sysdate), to_date(:2,'DD-MM-YYYY'))", lines)

cur.executemany("INSERT INTO STOPPED_RECOVERIES(M05_ID, M05_BILL_YYMM, M05_LOCATION, M05_STAFF, M05_BILL_NO, M05_BILL_AMT, M05_CUM_AMT_RECVRD, M05_BALANCE, M05_INST, M05_CURR_RCVY, M05_NOR, M05_BILLYR, M05_BILLMM, M05_BILLDD, M05_HOSP_NO,M05_DROPMMYY) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16)", lines)
#M05_ID, M05_BILL_YYMM, M05_LOCATION, M05_STAFF, M05_BILL_NO, M05_BILL_AMT, M05_CUM_AMT_RECVRD, M05_BALANCE, M05_INST, M05_CURR_RCVY, M05_NOR, M05_BILLYR, M05_BILLMM, M05_BILLDD, M05_HOSP_NO, PROCESSED_ON, UPDATED_EDPGRT_ON, RECOVERY_COMPLETED_REF, RECOVERY_ACTIVITY

con.commit ()
## Calling the Oracle Stored Procedure UPDATE_COMPLETED_RECOVERIES
l_query = cur.callproc('UPDATE_COMPLETED_RECOVERIES')

cur.close()
f.close()


os.rename("F:\pyora\edp\meddrop.csv", "F:\pyora\edp\edp_arch\meddrop.csv.arc")
