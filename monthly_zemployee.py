###################################################
# Program Name: monthly_zemployee.py
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
conn = cx_Oracle.connect('SAPRP1/bslrup03@10.143.106.5:1521/RP1')
cur  = conn.cursor()
#cur.execute("select nvl(zstno,' ') zstno, nvl(zspno,' ') zspno, nvl(zfname,' ') zfname, nvl(zmname,' ') zmname, nvl(zlname,' ') zlname, nvl(zgrade,' ') zgrade, nvl(gradedesc,' ') gradedesc, nvl(zdeptcd,' ') zdeptcd, nvl(replace(zdeptcd1,' '),' ') persdepcd, nvl(zdept,' ') zdept, nvl(zdept1,' ') zdept1,nvl(zdor,' ') zdor, nvl(replace(zmobile,0),' ') zmobile, nvl(replace(zphone1,0), ' ') zphone1, nvl(replace(zphone2,0),' ') zphone2, nvl(zemail,' ') zemail, nvl(zaddl1,' ') zaddl1, nvl(zaddl2,' ') zaddl2, nvl(zaddl3,' ') zaddl3, nvl(zaddr4,' ') zaddr4, ltrim(replace(zacno,'-'),'0') zacno, nvl(zroll,' ') zroll, nvl(dob,' ') dob, nvl(doj,' ') doj, nvl(dobsl,' ') dobsl, nvl(dos,' ') dos, nvl(TO_CHAR(sep_reasoncd),' ') sep_reasoncd  from zempdtl where zroll='Y' order by zstno")
#cur.execute("select nvl(zstno,'') zstno, nvl(zspno,'') zspno, nvl(zfname,'') zfname, nvl(zmname,'') zmname, nvl(zlname,'') zlname, nvl(zgrade,'') zgrade, nvl(gradedesc,'') gradedesc, nvl(zdeptcd,'') zdeptcd, nvl(replace(zdeptcd1,''),'') persdepcd, nvl(zdept,'') zdept, nvl(zdept1,'') zdept1,nvl(zdor,'') zdor, nvl(replace(zmobile,0),'') zmobile, nvl(replace(zphone1,0), '') zphone1, nvl(replace(zphone2,0),'') zphone2, nvl(zemail,'') zemail, nvl(zaddl1,'') zaddl1, nvl(zaddl2,'') zaddl2, nvl(zaddl3,'') zaddl3, nvl(zaddr4,'') zaddr4, ltrim(replace(zacno,'-'),'0') zacno, nvl(zroll,'') zroll, nvl(dob,'') dob, nvl(doj,'') doj, nvl(dobsl,'') dobsl, nvl(dos,'') dos, nvl(TO_CHAR(sep_reasoncd),'') sep_reasoncd  from zempdtl where zroll='Y' order by zstno")
cur.execute("select nvl(zstno,' ') zstno, nvl(zspno,' ') zspno, nvl(zfname,' ') zfname, nvl(zmname,' ') zmname, nvl(zlname,' ') zlname, nvl(zgrade,' ') zgrade, nvl(gradedesc,' ') gradedesc, nvl(replace(zdeptcd,' '),' ') zdeptcd, nvl(replace(zdeptcd1,' '),' ') persdepcd, nvl(zdept,' ') zdept, nvl(zdept1,' ') zdept1,nvl(zdor,' ') zdor, nvl(zmobile,' '), ' ' zphone1, ' ' zphone2, nvl(zemail,' ') zemail, nvl(zaddl1,' ') zaddl1, nvl(zaddl2,' ') zaddl2, nvl(zaddl3,' ') zaddl3, nvl(zaddr4,' ') zaddr4, nvl(zacno,' ') zacno, nvl(zroll,' ') zroll, nvl(dob,' ') dob, nvl(doj,' ') doj, nvl(dobsl,' ') dobsl, nvl(dos,' ') dos, nvl(TO_CHAR(sep_reasoncd),' ') sep_reasoncd  from zempdtl where zroll='Y' order by zstno")

file = open(r"F:\pyora\bgh\zempdtl.txt", "w")
for row in cur:


#          file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26]) + '\n')
        file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7].lstrip("0")) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12].lstrip("0")) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26].lstrip("0").rstrip(" ")) + '|'+'\n')

file.close()
cur.close()
conn.close()
##############################################################################################################################################
# Connection to Oracle BGH and Get the current EMPLOYEE ON ROLL EMPLOYEE FROM employee_for_erp
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()
#cur.execute("select STAFFNO, PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, EMPGRADEDESC, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, DEPTNAMEPERS, RETIREMENTDT, MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, BANKACNO, ROLLSTATUS, BIRTHDT, SAILJOINDT, BSLJOINDT, SEPERATIONDT, SEPRESSNCD from employee_for_erp order by staffno")
cur.execute("select STAFFNO, PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, EMPGRADEDESC, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, DEPTNAMEPERS, RETIREMENTDT, MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, BANKACNO, ROLLSTATUS, BIRTHDT, SAILJOINDT, BSLJOINDT, SEPERATIONDT, SEPRESSNCD from employee_for_erp order by staffno")
file = open(r"F:\pyora\bgh\employee_or.txt", "w")
#file.write('STAFFNO' + '|' + 'PERSNO' + '|' + 'FIRSTNAME' + '|' + 'MIDDLENAME' + '|' + 'LASTNAME' + '|' + 'EMPGRADE' + '|' + 'EMPGRADEDESC' + '|' + 'DEPTCDEDP' + '|' + 'DEPTCDPERS' + '|' + 'DEPTNAMEEDP' + '|' + 'DEPTNAMEPERS' + '|'+ 'RETIREMENTDT' + '|' + 'MOBILENO' + '|' + 'PHONENO1' + '|' + 'PHONENO2' + '|' + 'EMAILID' + '|' + 'ADDRESS1' + '|' + 'ADDRESS2' + '|' + 'ADDRESS3' + '|' + 'ADDRESS4' + '|' + 'BANKACNO' + '|' + 'ROLLSTATUS' + '|' + 'BIRTHDT' + '|' + 'SAILJOINDT' + '|' + 'BSLJOINDT' + '|'+ 'SEPERATIONDT' + '|' + 'SEPRESSNCD' + '\n')
for row in cur:
#         file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + row[26] + '\n')
         file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7].lstrip("0")) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12].lstrip(" ")) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26].lstrip("0").rstrip(" ")) + '|'+ '\n')

file.close()
cur.close()
conn.close()
##############################################################################################################################################
# Read in the original and new file          
orig = open(r"F:\pyora\bgh\employee_or.txt","r")
new  = open(r"F:\pyora\bgh\zempdtl.txt","r")
#in new but not in orig
#bigb = set(new) - set(orig)
#in orig but not in new
bigb = set(orig) - set(new)

# To see results in console if desired
#print(bigb)
# Write to output file    
with open(r"F:\pyora\employee.txt", "w") as file_out:
    for line in bigb:
        file_out.write(line)
#close the files  
orig.close()    
new.close()    
file_out.close()
###############################################################################################################################################
# Now FTP the file to the intermediate Server

##ftp = FTP('10.143.101.102')
##ftp.login(user='bslcmo', passwd='bslcmo')
##ftp.cwd('/employee/empprod/')

ftp = FTP('10.143.100.72')
ftp.login(user='zemp', passwd='zemp')
#ftp.cwd('/bslftp/zemp/')

def placeFile():

    filename = r"employee.txt"
    ftp.storbinary('STOR '+ filename, open(filename, 'rb'))
    ftp.quit()

placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname1 = (r"F:\pyora\bgh\bgh_arch\zempdtl.txt."+timestamp )
shutil.copy(r"F:\pyora\bgh\zempdtl.txt", dest_fname1)
os.remove(r"F:\pyora\bgh\zempdtl.txt")

dest_fname2 = (r"F:\pyora\bgh\bgh_arch\employee_or.txt."+timestamp )
shutil.copy(r"F:\pyora\bgh\employee_or.txt", dest_fname2)
os.remove(r"F:\pyora\bgh\employee_or.txt")

dest_fname3 = (r"F:\pyora\bgh\bgh_arch\employee.txt."+timestamp )
shutil.copy(r"F:\pyora\employee.txt", dest_fname3)
os.remove(r"F:\pyora\employee.txt")
###############################################################################################################################################
