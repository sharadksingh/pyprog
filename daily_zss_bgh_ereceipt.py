# Python Program to Get the differential employee data for SAP/ERP
# daily_zss_bgh_ereceipt.py
# This Program Transfers the ALL POS Collection from BGH to the ERP System.
# This Program has to be executed everyday ... and transfers data of previous date
# Scheduled in the Scheduler to run at 04:00 PM everday

#select to_char(rrn_date,'DD.MM.YYYY') receiving_date, 
#area receive_code, 
#slno remarks1,  
#remarks remarks2, 
#rrn_no_o rrn_no , 
#to_char(rrn_date,'DD.MM.YYYY') rrn_date, 
#total_amt rrn_amount,
#gstn 
#from bgh_pos_daily_date_view where rrn_date=trunc(sysdate)-1 order by rrn_no_o

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
#today = strftime(datetime.datetime.now(),'%d%m%y')

t = time.localtime()
today = time.strftime('%d%m%y',t)
################################################################################################################################################
# Connection to Oracle WARD and Get the Bill Details of the Third Party that has been made last month
f_filename = "bgh_receipt_"+today+".txt"
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()
cur.execute("select to_char(rrn_date,'DD.MM.YYYY') receiving_date,area receive_code,slno remarks1,remarks remarks2,rrn_no_o rrn_no,to_char(rrn_date,'DD.MM.YYYY') rrn_date,total_amt rrn_amount,gstn from bgh_pos_daily_date_view where rrn_date=trunc(sysdate)-1 order by rrn_no_o")

#cur.execute("select to_char(sldate,'DD.MM.YYYY') receiving_date, area receive_code, slno remarks1, to_char(sldate,'DDMMRRRR') remarks, rrn_no_o rrn_no , to_char(rrn_date,'DD.MM.YYYY') rrn_date, total_amt rrn_amount from bgh_pos_daily_date_view where rrn_date=trunc(sysdate)-1 order by rrn_no_o")
#file = open(r"F:\pyora\bgh_receipt_"+today+".txt", "w")
file = open(f_filename, "w")
for row in cur:
         file.write(str(row[0])+ '|' + str(row[1]) + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '\n')
file.close()
cur.close()
conn.close()
###############################################################################################################################################
###############################################################################################################################################
# Now FTP the file to the intermediate Server
ftp = FTP('10.143.100.72')
ftp.login(user='bghrecpt', passwd='bghrecpt')
#ftp.cwd('/bslftp/bghrecpt/')
def placeFile():
#    filename = r"bgh_receipt.txt"
    ftp.storbinary('STOR '+ f_filename, open(f_filename, 'rb'))
    ftp.quit()
placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname3 = (f_filename+timestamp )
shutil.copy(f_filename, dest_fname3)
os.remove(f_filename)

#dest_fname3 = (r"F:\pyora\bgh\bgh_arch\bgh_receipt.txt."+timestamp )
#shutil.copy(r"F:\pyora\bgh_receipt.txt", dest_fname3)
#os.remove(r"F:\pyora\bgh_receipt.txt")
###############################################################################################################################################
