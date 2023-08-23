###################################################
# Program Name: monthly_zcmocustomer.py
###################################################
'''
1.This Program Gets the Data from SAPRP1.ZEMPDTL for ZROLL='Y'and puts it into a text file F:\pyora\bgh\zemployee.txt
2.Gets the data  from BGH6.EMP_MASTER for roll_stat='Y' and puts it into a text file F:\pyora\bgh\employee_or.txt
3.Finds the difference between the two files that whatever changes is written to a text file called F:\pyora\employee.txt
4.The file F:\pyora\depemdent.txt is then transferred to the intermediate server 
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
##############################################################################################################################################
# Connection to Oracle SAPRP1 and get the data from ZEMPDTL
#conn = cx_Oracle.connect('SAPRD1/bslrup01@10.143.3.10:1527/RD1')
#cur  = conn.cursor()

#cur.execute("select nvl(PARTY_CODE,' ') party_code, nvl(OLD_PARTY_CODE, ' ') OLD_PARTY_CODE, nvl(TITLE,' ') TITLE, nvl(PARTY_NAME,' ') PARTY_NAME, nvl(NAME2,' ') NAME2, nvl(NAME3,' ') NAME3, nvl(ADDRESS,' ') ADDRESS, nvl(ADDRESS2,' ') ADDRESS2,nvl(ADDRESS3,' ') ADDRESS3,nvl(DISTRICT,' ') DISTRICT,nvl(CITY,' ') CITY, nvl(STATE,' ') STATE, nvl(COUNTRY,' ') COUNTRY, nvl(ZIPNO,' ') ZIPNO,  nvl(TEL_NUMBER1,' ') TEL_NUMBER1,nvl(FAX_NUMBER1,' ') FAX_NUMBER1,  nvl(CONTACT_PERSON,' ')  CONTACT_PERSON,nvl(SMTP_ADDR,' ') SMTP_ADDR, nvl(SEARCH_TERM1,' ') SEARCH_TERM1,nvl(SEARCH_TERM2,' ') SEARCH_TERM2,  nvl(CUSTOMER_TYPE_CODE,' ') CUSTOMER_TYPE_CODE,nvl(TYPE_OF_INDUSTRY,' ') TYPE_OF_INDUSTRY,  nvl(NATURE_OF_INDUSTRY,' ')  NATURE_OF_INDUSTRY,nvl(ORGANISATION_TYPE,' ') ORGANISATION_TYPE,nvl(PARTY_TYPE,' ') PARTY_TYPE,nvl(TIN_NUMBER,' ')  TIN_NUMBER,nvl(PAN_NUMBER,' ') PAN_NUMBER,  nvl(ECC_CODE_ALPHA_NUMERIC, ' ') ECC_CODE_ALPHA_NUMERIC,nvl(CST_REG_NO,' ') CST_REG_NO,nvl(CREATED_ON,' ') CREATED_ON,nvl(UPD_ON,' ') UPD_ON,  nvl(VAT_REG_NO,' ') VAT_REG_NO,nvl(UPD_BY,' ') UPD_BY, nvl(DEFUNCT,' ') DEFUNCT,  nvl(MOB_NUMBER,' ') MOB_NUMBER,  nvl(GSTNO,' ') GSTNO,nvl(GST_STATUS, ' ') GST_STATUS from ZCMOCUSTOMER order by party_code")
#file = open(r"F:\pyora\bgh\zcmocustomer.txt", "w")

#for row in cur:

#          if row[3] != '00000000':
#              date1=datetime.datetime.strptime(str(row[3]), '%Y%m%d')
#              date1=datetime.datetime.strftime(date1, '%d.%m.%Y')
     
#          if row[10] != '00000000':
#              date2=datetime.datetime.strptime(str(row[10]), '%Y%m%d')
#              date2=datetime.datetime.strftime(date2, '%d.%m.%Y')

#        file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26]) + '|' + str(row[27]) + '|' + str(row[28]) + '|' + str(row[29]) + '|' + str(row[30]) + '|' + str(row[31]) + '|' + str(row[32]) + '|' + str(row[33]) + '|' + str(row[34]) + '|' + str(row[35]) + '|' + str(row[36]) + '\n')
#file.close()
#cur.close()
#conn.close()
##############################################################################################################################################
# Connection to Oracle BGH and Get the current EMPLOYEE ON ROLL EMPLOYEE FROM employee_for_erp
conn = cx_Oracle.connect('cmo/cmo1234@10.143.100.205:1521/XE')
cur  = conn.cursor()
#cur.execute("select nvl(PARTY_CODE,' ') party_code, nvl(OLD_PARTY_CODE, ' ') OLD_PARTY_CODE, nvl(TITLE,' ') TITLE, nvl(PARTY_NAME,' ') PARTY_NAME, nvl(NAME2,' ') NAME2, nvl(NAME3,' ') NAME3, nvl(ADDRESS,' ') ADDRESS, nvl(ADDRESS2,' ') ADDRESS2,nvl(ADDRESS3,' ') ADDRESS3,nvl(DISTRICT,' ') DISTRICT,nvl(CITY,' ') CITY, nvl(STATE,' ') STATE, nvl(COUNTRY,' ') COUNTRY, nvl(ZIPNO,' ') ZIPNO,  nvl(TEL_NUMBER1,' ') TEL_NUMBER1,nvl(FAX_NUMBER1,' ') FAX_NUMBER1,  nvl(CONTACT_PERSON,' ')  CONTACT_PERSON,nvl(SMTP_ADDR,' ') SMTP_ADDR, nvl(SEARCH_TERM1,' ') SEARCH_TERM1,nvl(SEARCH_TERM2,' ') SEARCH_TERM2,  nvl(CUSTOMER_TYPE_CODE,' ') CUSTOMER_TYPE_CODE,nvl(TYPE_OF_INDUSTRY,' ') TYPE_OF_INDUSTRY,  nvl(NATURE_OF_INDUSTRY,' ')  NATURE_OF_INDUSTRY,nvl(ORGANISATION_TYPE,' ') ORGANISATION_TYPE,nvl(PARTY_TYPE,' ') PARTY_TYPE,nvl(TIN_NUMBER,' ')  TIN_NUMBER,nvl(PAN_NUMBER,' ') PAN_NUMBER,  nvl(ECC_CODE_ALPHA_NUMERIC, ' ') ECC_CODE_ALPHA_NUMERIC,nvl(CST_REG_NO,' ') CST_REG_NO,nvl(CREATED_ON,'') CREATED_ON,nvl(UPD_ON,'') UPD_ON,  nvl(VAT_REG_NO,' ') VAT_REG_NO,nvl(UPD_BY,' ') UPD_BY, nvl(DEFUNCT,' ') DEFUNCT,  nvl(MOB_NUMBER,' ') MOB_NUMBER,  nvl(GSTNO,' ') GSTNO,nvl(GST_STATUS, ' ') GST_STATUS, nvl(SEGMENT, ' ') SEGMENT from sap_party_master where trunc(created_on)=trunc(sysdate)-1 or trunc(upd_on)=trunc(sysdate)-1 order by party_code")
cur.execute("select nvl(PARTY_CODE,' ') party_code, nvl(OLD_PARTY_CODE, ' ') OLD_PARTY_CODE, nvl(TITLE,' ') TITLE, nvl(PARTY_NAME,' ') PARTY_NAME, nvl(NAME2,' ') NAME2, nvl(NAME3,' ') NAME3, nvl(ADDRESS,' ') ADDRESS, nvl(ADDRESS2,' ') ADDRESS2,nvl(ADDRESS3,' ') ADDRESS3,nvl(DISTRICT,' ') DISTRICT,nvl(CITY,' ') CITY, nvl(STATE,' ') STATE, nvl(COUNTRY,' ') COUNTRY, nvl(ZIPNO,' ') ZIPNO,  nvl(TEL_NUMBER1,' ') TEL_NUMBER1,nvl(FAX_NUMBER1,' ') FAX_NUMBER1,  nvl(CONTACT_PERSON,' ')  CONTACT_PERSON,nvl(SMTP_ADDR,' ') SMTP_ADDR, nvl(SEARCH_TERM1,' ') SEARCH_TERM1,nvl(SEARCH_TERM2,' ') SEARCH_TERM2,  nvl(CUSTOMER_TYPE_CODE,' ') CUSTOMER_TYPE_CODE,nvl(TYPE_OF_INDUSTRY,' ') TYPE_OF_INDUSTRY,  nvl(NATURE_OF_INDUSTRY,' ')  NATURE_OF_INDUSTRY,nvl(ORGANISATION_TYPE,' ') ORGANISATION_TYPE,nvl(PARTY_TYPE,' ') PARTY_TYPE,nvl(TIN_NUMBER,' ')  TIN_NUMBER,nvl(PAN_NUMBER,' ') PAN_NUMBER,  nvl(ECC_CODE_ALPHA_NUMERIC, ' ') ECC_CODE_ALPHA_NUMERIC,nvl(CST_REG_NO,' ') CST_REG_NO,nvl(CREATED_ON,trunc(sysdate)) CREATED_ON,nvl(UPD_ON,trunc(sysdate)) UPD_ON,  nvl(VAT_REG_NO,' ') VAT_REG_NO,nvl(UPD_BY,' ') UPD_BY, nvl(DEFUNCT,' ') DEFUNCT,  nvl(MOB_NUMBER,' ') MOB_NUMBER,  nvl(GSTNO,' ') GSTNO,nvl(GST_STATUS, ' ') GST_STATUS, nvl(SEGMENT, ' ') SEGMENT, nvl(req_id,'') REQ_ID, nvl(REQ_BRN_PLANT, ' ') REQ_BRN_PLANT,  nvl(TDS, '0') TDS from sap_party_master where trunc(created_on)=trunc(sysdate)-1or trunc(upd_on)=trunc(sysdate)-1 order by party_code")

file = open(r"F:\pyora\sap_party_master.txt", "w")

for row in cur:
#         file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + row[26] + '\n')
          file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26]) + '|' + str(row[27]) + '|' + str(row[28]) + '|' + str(row[29]) + '|' + str(row[30]) + '|' + str(row[31]) + '|' + str(row[32]) + '|' + str(row[33]) + '|' + str(row[34]) + '|' + str(row[35]) + '|' + str(row[36]) + '|' + str(row[37]) + '|'+ str(row[38])+ '|' + str(row[39]) + '|' + str(row[40]) + '\n')
file.close()
cur.close()
conn.close()
##############################################################################################################################################
# Read in the original and new file          
#orig = open(r"F:\pyora\bgh\zcmocustomer.txt","r")
#new  = open(r"F:\pyora\bgh\sap_party_master.txt","r")
#in new but not in orig
#in orig but not in new
#bigb = set(orig) - set(new)

# To see results in console if desired
# Write to output file    

#with open(r"F:\pyora\cmocustomer.txt", "w") as file_out:
#    for line in bigb:
#        file_out.write(line)
#close the files  
#orig.close()    
#new.close()    
#file_out.close()
###############################################################################################################################################
# Now FTP the file to the intermediate Server

###ftp = FTP('10.143.101.102')
###ftp.login(user='bslcmo', passwd='bslcmo')
###ftp.cwd('/employee/empprod/')

ftp = FTP('10.143.100.72')
ftp.login(user='cmocust', passwd='cmocust')
ftp.cwd('/bslftp/cmocust/')

def placeFile():

#    filename = r"cmocustomer.txt"
     filename = r"sap_party_master.txt"
     ftp.storbinary('STOR '+ filename, open(filename, 'rb'))
     ftp.quit()

placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)

#dest_fname1 = (r"F:\pyora\bgh\bgh_arch\zcmocustomer.txt."+timestamp )
#shutil.copy(r"F:\pyora\bgh\zcmocustomer.txt", dest_fname1)
#os.remove(r"F:\pyora\bgh\zcmocustomer.txt")

dest_fname2 = (r"F:\pyora\bgh\bgh_arch\sap_party_master.txt."+timestamp )
shutil.copy(r"F:\pyora\sap_party_master.txt", dest_fname2)
os.remove(r"F:\pyora\sap_party_master.txt")

#dest_fname3 = (r"F:\pyora\bgh\bgh_arch\cmocustomer.txt."+timestamp )
#shutil.copy(r"F:\pyora\cmocustomer.txt", dest_fname3)
#os.remove(r"F:\pyora\cmocustomer.txt")
###############################################################################################################################################
