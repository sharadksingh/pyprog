#The CSV file may be preapred from the excel file sent by final setlement.
#The first and second row of the CSV file may be removed.
#At the end of the CSV file there are many blak lines or lines containing ,,,,,,,,,,,,,,,,,, these may be removed and theen execute the
#program

import csv
import cx_Oracle


reader = csv.reader(open(r"F:\pyora\ref\referral_data_emp_sap.csv","r"))
lines=[]
for line in reader:
      lines.append(line)
# Connection to Oracle
con  = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = con.cursor()
#ver=con.version.split(".")
#print(ver)
cur=con.cursor()
#for line in lines:
#    cur.execute("INSERT INTO MEDICLAIM_MASTER_ENROLL_NEW('CENTRE_CODE','PLANT_CODE','MINNO_E','NAME_E','MF_E','AGE_E','DOB_E','NOMINEE_E','RLTN_E', 'MINNO_S','NAME_S','MF_S','AGE_S','DOB_S','NOMINEE_S','RLTN_S', 'ADD1', 'ADD2','ADD3','ADD4','PINCODE','DATE_SEP','DATE_ENROL','PH','MOB','MAIL_ID','SAIL_PNO','PLANT_PNO','CHEQ_DD_TYPE','CHEQUE_NO','CHEQUE_DT','CHEQUE_AMT','ENROL_TYPE','PREMIUM_EMP','PREMIUM_SP') values (:1,:2,:3,:4,:5,to_char(:6,):7,:8,:9,:10,:11,:12,to_char(:13),:14,:15,:16,:17,:18,:19,:20,:21,:22,:23,:24,:25,:26,:27,:28,:29,:30,:31,:32,:33,:34,:35)", line)
cur.executemany("INSERT INTO REFERRAL_DATA_EMP_SAP(staffno,persno) values (:1,:2)", lines)
con.commit ()
cur.close()
