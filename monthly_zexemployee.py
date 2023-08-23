###################################################
# Program Name: MONTHLY_ZEXEMPLOYEE.py
###################################################
'''
## This Program was executed on 30.04.2019 at 17:20 PM ... SO next month in the montyh of may 2019 .. the logic can be modified accordingly
## This Program was executed on 01.06.2019 at 11:10 PM ... SO next month in the montyh of Jun 2019 .. the logic can be modified accordingly
## This needs to be scheduled every month for updation of the employees getting status N
## To BE SCHEDULED DAILY ALONG WITH THE monthly_zemployee program
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
# Connection to Oracle BGH and Get the current EMPLOYEE SEPARATING TODAY OR SEPARATED THIS MONTH EMPLOYEE FROM EX_EMPLOYEE_FOR_ERP
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()
cur.execute("select STAFFNO, PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, EMPGRADEDESC, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, DEPTNAMEPERS, RETIREMENTDT, MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, BANKACNO, ROLLSTATUS, BIRTHDT, SAILJOINDT, BSLJOINDT, SEPERATIONDT, SEPRESSNCD from ex_employee_for_erp order by staffno")
file = open(r"F:\pyora\employee.txt", "w")
for row in cur:
         file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7].lstrip("0")) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12].lstrip(" ")) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26].lstrip("0").rstrip(" ")) + '|'+ '\n')

file.close()
cur.close()
conn.close()
###############################################################################################################################################
###############################################################################################################################################
# Now FTP the file to the intermediate Server
ftp = FTP('10.143.100.72')
ftp.login(user='zemp', passwd='zemp')
ftp.cwd('/bslftp/zemp/')

def placeFile():

    filename = r"employee.txt"
    ftp.storbinary('STOR '+ filename, open(filename, 'rb'))
    ftp.quit()

placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname3 = (r"F:\pyora\bgh\bgh_arch\employee_nor.txt."+timestamp )
shutil.copy(r"F:\pyora\employee.txt", dest_fname3)
os.remove(r"F:\pyora\employee.txt")
###############################################################################################################################################
