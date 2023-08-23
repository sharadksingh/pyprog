#3.py Call the stored procedure to send the password mail and also create he csv file to be
# Before doing this complete the following steps:
# 1. Assign the role to the vendor on SRM     and also initialize the password.
# 2. Assign the role to the vendor on CFolder and also initialize the password.

# sent over ftp to the ECC for update in zmveddact table

import csv
import cx_Oracle

import shutil, os
#import openpyxl
import datetime
from datetime import datetime
import smtplib, os, re, sys, glob, string, datetime, time
#from   email.mime.multipart import MIMEMultipart
#from   email.mime.base      import MIMEBase
#from   email.mime.text      import MIMEText
#from   email                import encoders
# for ftp of the file to the intermediate server
from ftplib import FTP
today = datetime.datetime.now()


con = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/BGH6')
cur = con.cursor()
cur.execute("ALTER SESSION SET NLS_DATE_FORMAT ='DD.MM.YYYY'")


# Call the procedure srm_initial_password_email
#l_query = cur.callproc('srm_initial_password_email')
#con.commit()

# Now create the csv file to be sent to ECC through ecc system
#cur.execute("select IP_NO, RPFC_ACC_NO, BOT_ACC_NO, W_NAME, W_GENDER, W_PHY_HAND, W_DOB, W_CATEGORY, FH_CODE, BLOOD_GROUP, MARITAL_STATUS, DISPLACED_STATUS, FH_NAME, MOTHER_NAME, SPOUSE_NAME, IDENT_MARK, T_ADDRESS1, T_ADDRESS2, T_CITY, T_PINCODE, T_CNTRY_CODE, T_TELNO, T_STATE, EMAIL_ID, P_ADDRESS1, P_ADDRESS2, P_CITY, P_PINCODE, P_CNTRY_CODE, P_TELNO, P_STATE, BANK_KEY, BANK_ACCNO, PAN_NO, DOC_VERIFICATION, ID_DOCNO, PRINCIPAL_EMP, M_USER, ENT_DATE, M_CTRL_NO, ID_PROOF, UPD_DATE, AADHAAR_NO from BGH.CLC_WORKER_MASTER_UPDATED_VIEW where length(trim(ip_no))=10 and trunc(m_upddate) is not null and trunc(m_entdate)!=trunc(m_upddate)  and trunc(m_upddate)=trunc(sysdate)-1")
#cur.execute("select V_CODE,V_NAME,V_EMAIL,V_MOBILE,V_SLNO,SEND,RECD_FROM_PUR,MAIL_SENT_DATE,MAIL_RECD_DATE,PASS_SENT_DATE,MAIL_BOUNCE_DT,INIT_PASS,NEWV_CODE,NEWV_SLNO,RESEND_INITAIL_MAIL from BGH.srm_mail_VW where recd_from_pur is not null and mail_sent_date is not null and mail_recd_date is not null and pass_sent_date = to_char(trunc(sysdate),'dd.mm.rrrr') and init_pass is not null and send is null")  

sql = """select V_CODE,V_NAME,V_EMAIL,V_MOBILE,V_SLNO,SEND,RECD_FROM_PUR,MAIL_SENT_DATE,MAIL_RECD_DATE,PASS_SENT_DATE,MAIL_BOUNCE_DT,
         INIT_PASS,NEWV_CODE,NEWV_SLNO,RESEND_INITAIL_MAIL from BGH.srm_mail_VW where recd_from_pur is not null and
         mail_sent_date is not null and mail_recd_date is not null and
         pass_sent_date = to_char(trunc(sysdate),'dd.mm.rrrr') and
         init_pass is not null and send is null""" 


#and pass_sent_date = to_char(trunc(sysdate),'dd.mm.rrrr') and init_pass is not null and send!='Y'

cur.execute(sql)
file = open(r"d:\pyora\zmvendact.txt", "w")
for row in cur:
         file.write(str(row[0])+ '|' + str(row[1]) + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '\n')
         cur.execute("update srm_mail set send='Y' where v_code=" + 'V' + str(row[0]))  
file.close()
cur.close()
con.commit()
con.close()
###############################################################################################################################################
###############################################################################################################################################
# Now FTP the file to the intermediate Server
ftp = FTP('10.143.100.72')
ftp.login(user='clc', passwd='clc123')
#ftp.cwd('/bslftp/clc/')
def placeFile():
    filename = r"zmvendact.txt"
    ftp.storbinary('STOR '+ filename, open(filename, 'rb'))
    ftp.quit()
placeFile()
###############################################################################################################################################

# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname3 = (r"d:\pyora\bgh\bgh_arch\zmvendact.txt."+timestamp )
shutil.copy(r"d:\pyora\zmvendact.txt", dest_fname3)
os.remove(r"d:\pyora\zmvendact.txt")
###############################################################################################################################################
