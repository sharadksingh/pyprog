###################################################
# Program Name: ZCLC_WORKER_MASTER.py
###################################################
'''
## This Program will get executed on 10 th of every month to transferbill data of third party of previous month to SAP 
'''

# Python Program to Get the differential employee data for SAP/ERP
import cx_Oracle
import shutil, os
import csv
import openpyxl
import datetime
from datetime import datetime
import smtplib, os, re, sys, glob, string, datetime, time
from   email.mime.multipart import MIMEMultipart
from   email.mime.base      import MIMEBase
from   email.mime.text      import MIMEText
from   email                import encoders
# for ftp of the file to the intermediate server
from ftplib import FTP
today = datetime.datetime.now()
################################################################################################################################################
# Connection to Oracle WARD and Get the Bill Details of the Third Party that has been made last month
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()
#cur.execute("select sap_code,company_name,customer_name2,emp_name,emp_design,emp_deptt,emp_staffno,patient_name,ref_letter_no,ref_letter_dt,hospno,hospyr,add1,add2,add3,city,pin,adm_date,disch_date,total_charges,rebate,tc_after_rebate,service_charge_perc,servc_charge,total_bill_amt,igst,cgst,sgst,tax_invoice_value,total_adv_received,net_bill_amt from wardbill_opd_zbghbildtl where to_char(hbilldt,'MMYYYY')>='01-APR-2019' and to_char(hbilldt,'MMYYYY')<='30-JUN-2019' order by sap_code, hospno||hospyr")
cur.execute("select IP_NO, RPFC_ACC_NO, BOT_ACC_NO, W_NAME, W_GENDER, W_PHY_HAND, W_DOB, W_CATEGORY, FH_CODE, BLOOD_GROUP, MARITAL_STATUS, DISPLACED_STATUS, FH_NAME, MOTHER_NAME, SPOUSE_NAME, IDENT_MARK, T_ADDRESS1, T_ADDRESS2, T_CITY, T_PINCODE, T_CNTRY_CODE, T_TELNO, T_STATE, EMAIL_ID, P_ADDRESS1, P_ADDRESS2, P_CITY, P_PINCODE, P_CNTRY_CODE, P_TELNO, P_STATE, BANK_KEY, BANK_ACCNO, PAN_NO, DOC_VERIFICATION, ID_DOCNO, PRINCIPAL_EMP, M_USER, ENT_DATE, M_CTRL_NO, ID_PROOF, UPD_DATE, AADHAAR_NO from BGH.CLC_WORKER_MASTER_VIEW where length(trim(ip_no))=10 and trunc(m_entdate)='12-OCT-2022' order by ip_no")
#cur.execute("select IP_NO, RPFC_ACC_NO, BOT_ACC_NO, W_NAME, W_GENDER, W_PHY_HAND, W_DOB, W_CATEGORY, FH_CODE, BLOOD_GROUP, MARITAL_STATUS, DISPLACED_STATUS, FH_NAME, MOTHER_NAME, SPOUSE_NAME, IDENT_MARK, T_ADDRESS1, T_ADDRESS2, T_CITY, T_PINCODE, T_CNTRY_CODE, T_TELNO, T_STATE, EMAIL_ID, P_ADDRESS1, P_ADDRESS2, P_CITY, P_PINCODE, P_CNTRY_CODE, P_TELNO, P_STATE, BANK_KEY, BANK_ACCNO, PAN_NO, DOC_VERIFICATION, ID_DOCNO, PRINCIPAL_EMP, M_USER, ENT_DATE, M_CTRL_NO, ID_PROOF, UPD_DATE, AADHAAR_NO from BGH.CLC_WORKER_MASTER_VIEW where length(trim(ip_no))=10 and ip_no in('6016539900','6016539910') order by ip_no")

file = open(r"F:\pyora\zclc_worker_master.txt", "w")
for row in cur:
         file.write(str(row[0])+ '|' + str(row[1]) + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26]) + '|'+ str(row[27]) + '|'+ str(row[28]) + '|'+ str(row[29]) + '|'+ str(row[30])+ '|'+ str(row[31]) + '|'+ str(row[32]) + '|' + str(row[33]) + '|' + str(row[34]) + '|' + str(row[35]) + '|'+ str(row[36]) + '|' + str(row[37]) + '|' + str(row[38]) + '|' + str(row[39]) + '|' + str(row[40]) + '|' + str(row[41]) + '|' + str(row[42]) + '|' + '\n')
file.close()
cur.close()
conn.close()
###############################################################################################################################################
###############################################################################################################################################
# Now FTP the file to the intermediate Server
ftp = FTP('10.143.100.72')
ftp.login(user='clc', passwd='clc123')
#ftp.cwd('/bslftp/clc/')

def placeFile():

    filename = r"zclc_worker_master.txt"
    ftp.storbinary('STOR '+ filename, open(filename, 'rb'))
    ftp.quit()

placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname3 = (r"F:\pyora\bgh\bgh_arch\zclc_worker_master.txt."+timestamp )
shutil.copy(r"F:\pyora\zclc_worker_master.txt", dest_fname3)
os.remove(r"F:\pyora\zclc_worker_master.txt")
###############################################################################################################################################
