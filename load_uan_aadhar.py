import cx_Oracle
import csv

con = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/BGH6')
cur = con.cursor()
cur.execute("ALTER SESSION SET NLS_DATE_FORMAT ='DD.MM.YYYY'")

with open("Book7_uan_aadhar.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    # skip first line if header row
    next(csv_reader)

    for lines in csv_reader:
        cur.execute("insert into UAN_AADHAR(uan,tp,aadhar,name) values (:1,:2,:3,:4)",(lines[0],lines[1],lines[2],lines[3]))

con.commit()

cur.close()
