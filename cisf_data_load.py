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
cur = con.cursor()
cur.execute("ALTER SESSION SET NLS_DATE_FORMAT ='DD.MM.YYYY'")

with open("FILES_MERGED_UPTO_28122022.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

# skip first line if header row
#    next(csv_reader)
    
    for lines in csv_reader:
        cur.execute("insert into bgh_mid_emplyee_cisf(name, relation, birth_dt, stno, srl, mid_no, dep_stat, sex, idnt_mark, blood, ret_dt, emp_stat, pat_stat, party_code, last_update,mobile_no) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16)",(lines[0], lines[1], lines[2], lines[3], lines[4],lines[5], lines[6], lines[7],lines[8],lines[9],lines[10],lines[11],lines[12],lines[13],lines[14],lines[15]))


con.commit()

cur.close()
