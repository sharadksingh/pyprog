#Program Name: monthly_exemployee_erp.py
'''
This Program generates not on roll employee data every moth and transfers to the erp system
This is scheduled to run through the windows scheduler on 1st of every month
'''
# Python Program to FTP the data of ex employee data to intermediate server
import cx_Oracle
import shutil, os
import csv
import openpyxl
import datetime, time
import smtplib, os, re, sys, glob, string, datetime
from   email.mime.multipart import MIMEMultipart
from   email.mime.base      import MIMEBase
from   email.mime.text      import MIMEText
from   email                import encoders

# for ftp of the file to the intermediate server
from ftplib import FTP
today = datetime.datetime.now()
# Connection to Oracle
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()

cur.execute("select STAFFNO, PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, EMPGRADEDESC, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, DEPTNAMEPERS, RETIREMENTDT, MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, BANKACNO, ROLLSTATUS, BIRTHDT, SAILJOINDT, BSLJOINDT, SEPERATIONDT, SEPRESSNCD from ex_employee_for_erp")
file = open(r"F:\pyora\employee.txt", "w")
file.write('STAFFNO' + '|' + 'PERSNO' + '|' + 'FIRSTNAME' + '|' + 'MIDDLENAME' + '|' + 'LASTNAME' + '|' + 'EMPGRADE' + '|' + 'EMPGRADEDESC' + '|' + 'DEPTCDEDP' + '|' + 'DEPTCDPERS' + '|' + 'DEPTNAMEEDP' + '|' + 'DEPTNAMEPERS' + '|'+ 'RETIREMENTDT' + '|' + 'MOBILENO' + '|' + 'PHONENO1' + '|' + 'PHONENO2' + '|' + 'EMAILID' + '|' + 'ADDRESS1' + '|' + 'ADDRESS2' + '|' + 'ADDRESS3' + '|' + 'ADDRESS4' + '|' + 'BANKACNO' + '|' + 'ROLLSTATUS' + '|' + 'BIRTHDT' + '|' + 'SAILJOINDT' + '|' + 'BSLJOINDT' + '|'+ 'SEPERATIONDT' + '|' + 'SEPRESSNCD' + '\n')
#file.write('STAFF-NO'+ '|' + 'EMP NAME' + '|' + 'DEPTT' + '|' + 'SECTION' + '|' + 'HOSPNO' + '|' + 'PAT NAME' +  '|' + '\n')
for row in cur:
         file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + row[26] + '\n')
file.close()
cur.close()
conn.close()
##############################################################################################################################################
ftp = FTP('10.143.101.102')
ftp.login(user='bslcmo', passwd='bslcmo')
ftp.cwd('/employee/empprod/')

def placeFile():

    filename = r"employee.txt"
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

placeFile()
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname = (r"F:\pyora\bgh\bgh_arch\employee.txt."+timestamp )
shutil.copy(r"F:\pyora\employee.txt", dest_fname)
os.remove(r"F:\pyora\employee.txt")
##############################################################################################################################################
