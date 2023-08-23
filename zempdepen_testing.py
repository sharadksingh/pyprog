###################################################
# Program Name: zempdepen_TESTING.py
###################################################
'''
1.This Program Gets the Data from SAPRP1.ZEMPDEPENDENT and puts it into a text file F:\pyora\bgh\zempdependent.txt
2.Gets the data  from BGH6.REFERRAL_DATA_DEPEN_CURRENT and puts it into a text file F:\pyora\bgh\depencur.txt
3.Finds the difference between the two files that whatever changes is written to a text file called F:\pyora\dependent.txt
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
# Connection to Oracle SAPRP1 and get the data from ZEMPDEPENDENT
conn = cx_Oracle.connect('SAPRP1/bslrup03@10.143.100.51:1527/RP1')
cur  = conn.cursor()
cur.execute("select nvl(medbkno,' ') medbkno, nvl(name,' ') name, nvl(gender,' ') gender, nvl(dob,' ') dob, nvl(relation,' ') relation, nvl(blood,' ') blood, nvl(depstatus,' ') depstatus, nvl(idmark,' ') idmark, nvl(stno,' ') stno, nvl(empname,' ') empname,  nvl(dor,' ') dor, nvl(gradecd,' ') gradecd, nvl(substr(gradedesc,1,20),' ') gradedesc, nvl(deptcd,' ') deptcd, nvl(deptdesc,' ') deptdesc,  nvl(eligibletag,' ') eligibletag from zempdependent order by medbkno")
file = open(r"F:\pyora\bgh\zempdependent.txt", "w")
for row in cur:
#          if row[9] != '00000000':
#              date9=datetime.datetime.strptime(str(row[9]), '%Y%m%d')
#              date9=datetime.datetime.strftime(date9, '%d.%m.%Y')
          file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13].lstrip("0")) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + '\n')
file.close()
cur.close()
conn.close()
##############################################################################################################################################
# Connection to Oracle BGH and Get the current dependent details from the view REFERRAL_DATA_DEPEN_CURRENT
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()
cur.execute("select nvl(medbkno,' ') medbkno, nvl(name,' ') name, nvl(gender,' ') gender, nvl(dob, ' ') dob, nvl(RelationShip,' ') relation, nvl(BloodGrp,' ') blood, nvl(depstatus,' ') depstatus, nvl(idmark,' ') idmark, nvl(stno,' ') stno,  nvl(empname,' ') empname, nvl(dor, ' ') dor, nvl(gradecd,' ') gradecd, nvl(substr(gradedesc,1,20),' ') gradedesc, nvl(DeptCdEdp,' ') deptcd, nvl(DeptNameEdp,' ') deptdesc, 'Y' eligibletag  from REFERRAL_DATA_DEPEN_CURRENT where dor is not null order by medbkno")
file = open(r"F:\pyora\bgh\depencur.txt", "w")
for row in cur:
          file.write(row[0]+ '|' + row[1].lstrip(" ") + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + '\n')
file.close()
cur.close()
conn.close()
##############################################################################################################################################
# Read in the original and new file          
orig = open(r"F:\pyora\bgh\depencur.txt","r")
new  = open(r"F:\pyora\bgh\zempdependent.txt","r")
#in new but not in orig
#bigb = set(new) - set(orig)
#in orig but not in new
bigb = set(orig) - set(new)

# To see results in console if desired
#print(bigb)
# Write to output file    
with open(r"F:\pyora\dependent.txt", "w") as file_out:
    for line in bigb:
        file_out.write(line)
#close the files  
orig.close()    
new.close()    
file_out.close()
###############################################################################################################################################
# Now FTP the file to the intermediate Server
#ftp = FTP('10.143.101.102')
#ftp.login(user='bslcmo', passwd='bslcmo')
#ftp.cwd('/employee/empprod/')

#ftp = FTP('10.143.100.72')
#ftp.login(user='zdepen', passwd='zdepen')
#ftp.cwd('/bslftp/zdepen/')

#def placeFile():

#    filename = r"dependent.txt"
#    ftp.storbinary('STOR '+ filename, open(filename, 'rb'))
#    ftp.quit()

#placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname1 = (r"F:\pyora\bgh\bgh_arch\depencur.txt."+timestamp )
shutil.copy(r"F:\pyora\bgh\depencur.txt", dest_fname1)
os.remove(r"F:\pyora\bgh\depencur.txt")

dest_fname2 = (r"F:\pyora\bgh\bgh_arch\zempdependent.txt."+timestamp )
shutil.copy(r"F:\pyora\bgh\zempdependent.txt", dest_fname2)
os.remove(r"F:\pyora\bgh\zempdependent.txt")

dest_fname3 = (r"F:\pyora\bgh\bgh_arch\dependent.txt."+timestamp )
shutil.copy(r"F:\pyora\dependent.txt", dest_fname3)
os.remove(r"F:\pyora\dependent.txt")
###############################################################################################################################################
