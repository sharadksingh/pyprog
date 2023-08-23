#1.py Load the csv data of the vendors to which the initial activation mail has to be sent.
#Further Improvement can be done by askling the input a) file-name b) the date of data
import csv
import cx_Oracle

#db = cx_Oracle.connect('bgh/hpv185e@bgh6:1521/BGH6')
#db = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/BGH6')
#cursor = db.cursor()

#reader = csv.reader(open(r"D:\VENDOR_ACTIVATION\1.csv","r"))
#lines = []
#for lines in reader:
#    lines.append(lines)

#cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT ='DD.MM.YYYY'")
#cursor.executemany("INSERT INTO SRM_EMAIL(v_code,v_name,v_email,v_mobile) values(:1,:2,:8,:6)", lines)
#db.commit()




# 1.py
import cx_Oracle
import csv

con = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/BGH6')
#### NOT REQUIRED con = cx_Oracle.connect('hrs/comp1ex@128.233.5.121:1521/rac')

cur = con.cursor()
cur.execute("ALTER SESSION SET NLS_DATE_FORMAT ='DD-MM-YYYY'")

with open("qtr_30082022.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

# skip first line if header row
#    next(csv_reader)
    
#    for lines in csv_reader:
#        cur.execute(
#           "insert into bgh_mid_employee(name, relation, birth_dt, stno, srl, mid_no, dep_stat, sex, idnt_mark, blood, ret_dt, emp_stat, pat_stat, party_code) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14)",(lines[0], lines[1], lines[2], lines[3], lines[4],lines[5], lines[6], lines[7],lines[8],lines[9],lines[10],lines[11],lines[12],lines[13]))
    for lines in csv_reader:
        cur.execute("insert into emp_qtr_retention(ORDER_NO, ORDER_DT, STNO, APPLICANT_NAME, QTR_NO, SEP_REASON, RETENTION_REASON, SEP_DATE, GRACE_FROM, GRACE_TO, RETENTION_FROM, RETENTION_TO, SURETY_STNO, SURETY_NAME, SURETY_DEPTT, OPTR_STNO, ENTRY_DATE, AUTH_LETTER_SUBMITTED, FINANCE_STATUS, FINANCE_REMARKS, FINANCE_OPTR, FINANCE_ENTRY_DATE, REJECT_RETENTION_REMARKS, AUTH_REJECT_REASON, APPLICATION_STATUS, DEPOSIT, ADV_RENT)values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27)",(lines[0], lines[1], lines[2], lines[3], lines[4],lines[5], lines[6], lines[7],lines[8],lines[9],lines[10],lines[11],lines[12],lines[13], lines[14],lines[15],lines[16],lines[17],lines[18],lines[19],lines[20],lines[21],lines[22],lines[23],lines[24],lines[25],lines[26]))


con.commit()

cur.close()
