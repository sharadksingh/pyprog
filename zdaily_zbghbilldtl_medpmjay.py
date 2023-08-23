###################################################
# Program Name: ZDAILY_ZBGHBILLDTL_MEDPMJAY.py
# For MEDICLAIM and PMJAY
# Bill Detail Transfer to SAP
# To be Scheduled Daily at Some Time
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
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()
cur.execute("select sap_code,company_name,customer_name2,emp_name,emp_design,emp_deptt,emp_staffno,patient_name,ref_letter_no,ref_letter_dt,hospno,hospyr,add1,add2,add3,city,pin,adm_date,disch_date,total_charges,rebate,tc_after_rebate,service_charge_perc,servc_charge,total_bill_amt,igst,cgst,sgst,tax_invoice_value,total_adv_received,net_bill_amt,hbillno lotno,to_char(hbilldt,'DD.MM.YYYY') lotdt, state_code, gstno from  WARDBILL_ZBGHBILDTL_MEDPMJAY where billdt is not null and billdt between '01-APR-2020' and '31-AUG-2020' order by sap_code, hospno||hospyr")
file = open(r"F:\pyora\wardbill_billdtl.txt", "w")
for row in cur:
         file.write(str(row[0])+ '|' + str(row[1]) + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26]) + '|'+ str(row[27]) + '|'+ str(row[28]) + '|'+ str(row[29]) + '|'+ str(row[30])+ '|' + str(row[31]) + '|' + str(row[32])+ '|' + str(row[33])+ '|' + str(row[34]) + '\n')
file.close()
cur.close()
conn.close()
###############################################################################################################################################
###############################################################################################################################################
# Now FTP the file to the intermediate Server
ftp = FTP('10.143.100.72')
ftp.login(user='bghrdcr', passwd='bghrdcr')
ftp.cwd('/bslftp/bghrdcr/')

def placeFile():

    filename = r"wardbill_billdtl.txt"
    ftp.storbinary('STOR '+ filename, open(filename, 'rb'))
    ftp.quit()

placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname3 = (r"F:\pyora\bgh\bgh_arch\wardbill_billdtl.txt."+timestamp )
shutil.copy(r"F:\pyora\wardbill_billdtl.txt", dest_fname3)
os.remove(r"F:\pyora\wardbill_billdtl.txt")
###############################################################################################################################################
