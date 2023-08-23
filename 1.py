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

with open("e_18022020.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

# skip first line if header row
    next(csv_reader)
    
    for lines in csv_reader:
        cur.execute(
            "insert into srm_mail(v_code,v_name,v_email,v_mobile, recd_from_pur) values (:1, :2, :8, :7, :12)",
            (lines[0], lines[1], lines[7], lines[6],lines[11]))


con.commit()
# Call the procedure srm_initial_activation_email(in_date)
l_query = cur.callproc('srm_initial_activation_email',['20-02-2020'])
con.commit()

cur.close()



# Update the BGH_DOCTDIC so that the Doctor Database is updated
#cur.execute("update bgh_doctdic     set blocked='Y', REMARKS='RETIRED' where staff in (select stno from emp_master where roll_stat='N') and blocked='N' ")
#cur.execute("update bgh_doctdic_new set blocked='Y', REMARKS='RETIRED' where staff in (select stno from emp_master where roll_stat='N') and blocked='N' ")

#    Update On Roll Employee and Dependents
#l_query = cur.callproc('find_schema_stats');
#    Update Not On Roll Employees and Spouse
#l_query = cur.callproc('bgh_mid_update_nor_daily');
#con.commit ()
#cur.close()

