# Program Name: monthly_sap_data.py
'''

DONT USE THIS PROGRAM ... A MORE EFFICIENT PROGRAM TO FIND THE DIFFERENTIAL HAS BEEN CRAETED MINTHLY_ZEMPDEPENDENT.PY

This Program generates on roll employee data every moth and transfers to the erp system
This is scheduled to run through the windows scheduler on 1st of every month
'''

# Python Program to Get the differential employee data for SAP/ERP
import cx_Oracle
import shutil, os
import csv
import openpyxl
import datetime
import smtplib, os, re, sys, glob, string, datetime, time
from   email.mime.multipart import MIMEMultipart
from   email.mime.base      import MIMEBase
from   email.mime.text      import MIMEText
from   email                import encoders
# for ftp of the file to the intermediate server
from ftplib import FTP
today = datetime.datetime.now()
# Connection to Oracle SAPRP1 and get the data from ZEMPDTL for ZROLL=Y
conn = cx_Oracle.connect('SAPRP1/bslrup03@10.143.106.5:1527/RP1')
cur  = conn.cursor()
#cur.execute("select a.staffno, (b.f_name||' '||b.l_employee) emp_name,b.dept, b.grade_pay, (a.hospno||'/'||a.hospyear) hospno,c.pat_name from bpscl_edpgrt a,bpscl_emp_grnt b,ward_admission_vw  c,emp_dep_code d where a.admdate >= trunc(last_day(sysdate)-1, 'mm') and a.admdate <= last_day(trunc(sysdate)-1) and a.staffno = b.staff_no and  a.hospno = c.hospno and a.hospyear= c.hospyr  order by a.staffno")
#cur.execute("select nvl(zstno,' ') zstno, nvl(zspno,' ') zspno, nvl(zfname,' ') zfname, nvl(zmname,' ') zmname, nvl(zlname,' ') zlname, nvl(zgrade,' ') zgrade, nvl(zdeptcd,' ') zdeptcd, nvl(replace(zdeptcd,' '),' ') edpdepcd, nvl(zdept,' ') zdept, nvl(zdor,' ') zdor, nvl(replace(zmobile,0),' ') zmobile, nvl(replace(zphone1,0), ' ') zphone1, nvl(replace(zphone2,0),' ') zphone2, nvl(zemail,' ') zemail, nvl(zaddl1,' ') zaddl1, nvl(zaddl2,' ') zaddl2, nvl(zaddl3,' ') zaddl3, nvl(zaddr4,' ') zaddr4, ltrim(replace(zacno,'-'),'0') zacno, nvl(zroll,' ') zroll, nvl(crdate,'') crdate,  nvl(zdeptcd1,' ') zdeptcd1, nvl(zdept1,' ') zdept1, nvl(dob,' ') dob, nvl(doj,' ') doj, nvl(dos,' ') dos, nvl(TO_CHAR(sep_reasoncd),' ') sep_reasoncd, nvl(dobsl,' ') dobsl, nvl(gradedesc,' ') gradedesc , nvl(zhod,' ') zhod from zempdtl where zroll='Y'")
cur.execute("select nvl(zstno,' ') zstno, nvl(zspno,' ') zspno, nvl(zfname,' ') zfname, nvl(zmname,' ') zmname, nvl(zlname,' ') zlname, nvl(zgrade,' ') zgrade, nvl(zdeptcd,' ') zdeptcd, nvl(replace(zdeptcd,' '),' ') edpdepcd, nvl(zdept,' ') zdept, nvl(zdor,' ') zdor, nvl(replace(zmobile,0),' ') zmobile, nvl(replace(zphone1,0), ' ') zphone1, nvl(replace(zphone2,0),' ') zphone2, nvl(zemail,' ') zemail, nvl(zaddl1,' ') zaddl1, nvl(zaddl2,' ') zaddl2, nvl(zaddl3,' ') zaddl3, nvl(zaddr4,' ') zaddr4, ltrim(replace(zacno,'-'),'0') zacno, nvl(zroll,' ') zroll, nvl(crdate,'') crdate,  nvl(zdeptcd1,' ') zdeptcd1, nvl(zdept1,' ') zdept1, nvl(dob,' ') dob, nvl(doj,' ') doj, nvl(dos,' ') dos, nvl(TO_CHAR(sep_reasoncd),' ') sep_reasoncd, nvl(dobsl,' ') dobsl, nvl(gradedesc,' ') gradedesc  from zempdtl where zroll='Y'")
#cur.execute("select STAFFNO, PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, EMPGRADEDESC, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, DEPTNAMEPERS, RETIREMENTDT, MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, BANKACNO, ROLLSTATUS, BIRTHDT, SAILJOINDT, BSLJOINDT, SEPERATIONDT, SEPRESSNCD from ex_employee_for_erp")
file = open(r"F:\pyora\bgh\zempdtl.txt", "w")
#STAFFNO, PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, EMPGRADEDESC, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, DEPTNAMEPERS, RETIREMENTDT, MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, BANKACNO, ROLLSTATUS, BIRTHDT, SAILJOINDT, BSLJOINDT, SEPERATIONDT, SEPRESSNCD
#file.write('STAFFNO' + '|' + 'PERSNO' + '|' + 'FIRSTNAME' + '|' + 'MIDDLENAME' + '|' + 'LASTNAME' + '|' + 'EMPGRADE' + '|' + 'EMPGRADEDESC' + '|' + 'DEPTCDEDP' + '|' + 'DEPTCDPERS' + '|' + 'DEPTNAMEEDP' + '|' + 'DEPTNAMEPERS' + '|'+ 'RETIREMENTDT' + '|' + 'MOBILENO' + '|' + 'PHONENO1' + '|' + 'PHONENO2' + '|' + 'EMAILID' + '|' + 'ADDRESS1' + '|' + 'ADDRESS2' + '|' + 'ADDRESS3' + '|' + 'ADDRESS4' + '|' + 'BANKACNO' + '|' + 'ROLLSTATUS' + '|' + 'BIRTHDT' + '|' + 'SAILJOINDT' + '|' + 'BSLJOINDT' + '|'+ 'SEPERATIONDT' + '|' + 'SEPRESSNCD' + '\n')
#file.write('STAFF-NO'+ '|' + 'EMP NAME' + '|' + 'DEPTT' + '|' + 'SECTION' + '|' + 'HOSPNO' + '|' + 'PAT NAME' +  '|' + '\n')
for row in cur:
#         file.write(row[0]+ ',' + row[1] + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' + str(row[9]) + ',' + str(row[10]) + ',' + str(row[11]) + ',' + str(row[12]) + ',' + str(row[13]) + ',' + str(row[14]) + ',' + str(row[15]) + ',' + str(row[16]) + ',' + str(row[17]) + ',' + str(row[18]) + ',' + str(row[19]) + ',' + str(row[20]) + ',' + str(row[21]) + ',' + str(row[22]) + ',' + str(row[23]) + ',' + str(row[24]) + ',' + str(row[25]) + ',' + str(row[26]) + ','+ str(row[27]) + ',' + str(row[28]) + ',' + str(row[29]) + '\n')
#         file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + row[3] + '|' + '\n')
          file.write(row[0]+ ',' + row[1] + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' + str(row[9]) + ',' + str(row[10]) + ',' + str(row[11]) + ',' + str(row[12]) + ',' + str(row[13]) + ',' + str(row[14]) + ',' + str(row[15]) + ',' + str(row[16]) + ',' + str(row[17]) + ',' + str(row[18]) + ',' + str(row[19]) + ',' + str(row[20]) + ',' + str(row[21]) + ',' + str(row[22]) + ',' + str(row[23]) + ',' + str(row[24]) + ',' + str(row[25]) + ',' + str(row[26]) + ','+ str(row[27]) + ',' + str(row[28])  + '\n')
file.close()
cur.close()
conn.close()
##############################################################################################################################################
# Upload the File Into the table REFERRAL_DATA_EMP_SAP
reader = csv.reader(open(r"F:\pyora\bgh\zempdtl.txt","r"))
lines=[]
for line in reader:
      lines.append(line)
con  = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = con.cursor()
cur.execute('TRUNCATE TABLE REFERRAL_DATA_EMP_SAP');
#STAFFNO,  PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, RETIREMENTDT, MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4,BANKACNO, ROLLSTATUS, CRDATE, ZDEPTCD1, DEPTNAMEPERS, BIRTHDT, SAILJOINDT, SEPERATIONDT, SEPRESSNCD, BSLJOINDT, EMPGRADEDESC)
cur.executemany("INSERT INTO REFERRAL_DATA_EMP_SAP(STAFFNO, PERSNO, FIRSTNAME, MIDDLENAME, LASTNAME, EMPGRADE, DEPTCDEDP, DEPTCDPERS, DEPTNAMEEDP, RETIREMENTDT,MOBILENO, PHONENO1, PHONENO2, EMAILID, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, BANKACNO, ROLLSTATUS, CRDATE, ZDEPTCD1,DEPTNAMEPERS, BIRTHDT, SAILJOINDT,SEPERATIONDT, SEPRESSNCD, BSLJOINDT, EMPGRADEDESC ) values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29)",lines)
con.commit ()
cur.close()
file.close()
###############################################################################################################################################
# Now for the text file for sending to the intermediate server
# Connection to Oracle BGH
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()
file = open(r"F:\pyora\employee.txt", "w")
cur.execute("select a.stno staffNo,c.pno_sail PersNo,a.ffname FirstName,' ' MiddleName,a.lname  LastName,a.gradep EmpGrade,a.desdescp EmpGradeDesc,substr(a.edpdeptt,1,3) DeptCdEdp,a.deptt    DeptCdPers,b.dep_name  DeptNameEdp,b.dep_name DeptNamePers,to_char(a.ret_dt,'DD.MM.YYYY') RetirementDt,nvl(a.mob,' ') MobileNo,' ' PhoneNo1,' ' PhoneNo2,nvl(a.email,' ') EmailId,d.sector Address1,d.nh Address2,d.qtr_type Address3,d.qtrno Address4,' ' BankAcNo,a.roll_stat RollStatus,to_char(a.birth_dt,'DD.MM.YYYY') BirthDt,to_char(a.aptt_dt,'DD.MM.YYYY') SailJoinDt,to_char(a.bsl_dt,'DD.MM.YYYY') BslJoinDt,nvl(to_char(sep_dt,'DD.MM.YYYY'),' ') SeperationDt, a.sepdes||'|'SepRessnCd from emp_master a, deptt_code_dic b, emp_mast_corp1 c, emp_pay_detail d where  a.deptt=b.deptt and a.stno=c.pno_unit and a.stno=d.stno(+)and a.stno in ((select staffno from (select staffno, persno, trim(firstname) firstname, middlename, trim(lastname), empgrade, deptcdedp, rollstatus  from EMPLOYEE_FOR_ERP minus select staffno, persno, trim(firstname) firstname, middlename, trim(lastname), empgrade, substr(deptcdedp,4) deptcdedp, rollstatus from REFERRAL_DATA_EMP_sap)))")
#STAFFNO|PERSNO|FIRSTNAME|MIDDLENAME|LASTNAME|EMPGRADE|EMPGRADEDESC|DEPTCDEDP|DEPTCDPERS|DEPTNAMEEDP|DEPTNAMEPERS|RETIREMENTDT|MOBILENO|PHONENO1|PHONENO2|EMAILID|ADDRESS1|ADDRESS2|ADDRESS3|ADDRESS4|BANKACNO|ROLLSTATUS|BIRTHDT|SAILJOINDT|BSLJOINDT|SEPERATIONDT|SEPRESSNCD
file.write('STAFFNO' + '|' + 'PERSNO' + '|' + 'FIRSTNAME' + '|' + 'MIDDLENAME' + '|' + 'LASTNAME' + '|' + 'EMPGRADE' + '|' + 'EMPGRADEDESC' + '|' + 'DEPTCDEDP' + '|' + 'DEPTCDPERS' + '|' + 'DEPTNAMEEDP' + '|' + 'DEPTNAMEPERS' + '|'+ 'RETIREMENTDT' + '|' + 'MOBILENO' + '|' + 'PHONENO1' + '|' + 'PHONENO2' + '|' + 'EMAILID' + '|' + 'ADDRESS1' + '|' + 'ADDRESS2' + '|' + 'ADDRESS3' + '|' + 'ADDRESS4' + '|' + 'BANKACNO' + '|' + 'ROLLSTATUS' + '|' + 'BIRTHDT' + '|' + 'SAILJOINDT' + '|' + 'BSLJOINDT' + '|'+ 'SEPERATIONDT' + '|' + 'SEPRESSNCD' + '\n')
for row in cur:
#         file.write(row[0]+ ',' + row[1] + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' + str(row[9]) + ',' + str(row[10]) + ',' + str(row[11]) + ',' + str(row[12]) + ',' + str(row[13]) + ',' + str(row[14]) + ',' + str(row[15]) + ',' + str(row[16]) + ',' + str(row[17]) + ',' + str(row[18]) + ',' + str(row[19]) + ',' + str(row[20]) + ',' + str(row[21]) + ',' + str(row[22]) + ',' + str(row[23]) + ',' + str(row[24]) + ',' + str(row[25]) + ',' + str(row[26]) + ','+ str(row[27]) + ',' + str(row[28]) + ',' + str(row[29]) + '\n')
#         file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + row[3] + '|' + '\n')
          file.write(row[0]+ '|' + row[1] + '|' + str(row[2]) + '|' + str(row[3]) + '|' + str(row[4]) + '|' + str(row[5]) + '|' + str(row[6]) + '|' + str(row[7]) + '|' + str(row[8]) + '|' + str(row[9]) + '|' + str(row[10]) + '|' + str(row[11]) + '|' + str(row[12]) + '|' + str(row[13]) + '|' + str(row[14]) + '|' + str(row[15]) + '|' + str(row[16]) + '|' + str(row[17]) + '|' + str(row[18]) + '|' + str(row[19]) + '|' + str(row[20]) + '|' + str(row[21]) + '|' + str(row[22]) + '|' + str(row[23]) + '|' + str(row[24]) + '|' + str(row[25]) + '|' + str(row[26]) +  '\n')
file.close()
cur.close()
conn.close()
###############################################################################################################################################
# Now FTP the file to the intermediate Server
ftp = FTP('10.143.101.102')
ftp.login(user='bslcmo', passwd='bslcmo')
ftp.cwd('/employee/empprod/')

def placeFile():

    filename = r"employee.txt"
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

placeFile()
###############################################################################################################################################
# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname1 = (r"F:\pyora\bgh\bgh_arch\employee.txt."+timestamp )
shutil.copy(r"F:\pyora\employee.txt", dest_fname1)
os.remove(r"F:\pyora\employee.txt")

dest_fname2 = (r"F:\pyora\bgh\bgh_arch\zempdtl.txt."+timestamp )
shutil.copy(r"F:\pyora\bgh\zempdtl.txt", dest_fname2)
#os.remove(r"F:\pyora\bgh\zempdtl.txt")
###############################################################################################################################################
