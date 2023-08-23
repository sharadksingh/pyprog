# Import necessary libraries
import cx_Oracle
import psycopg2

i = 0
# Connect to the Oracle database
# Connection to Oracle
orcl=cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')

# Connect to the PostgreSQL database
pgdb=psycopg2.connect("host=10.143.107.174 port=5444 dbname=hmis_sail user=hmissail password=h1m2i3s4sail")

#"host=10.143.107.174 port=5444 dbname=hmis_sail user=hmissail password=h1m2i3s4sail"

# Create a cursor to perform operations on the Oracle database
orclcursor = orcl.cursor()
# Create a cursor to perform operations on the PostgreSQL database
pgcursor = pgdb.cursor()
# Execute an Oracle query to retrieve the data
#orclcursor.execute("SELECT STR_EMP_NO, NUM_MEM_SL_NO, STR_MID_NO, GNUM_APPELLATION_CODE_1, STR_MEM_FULL_NAME, STR_MEM_SHORT_NAME, FULL_NAME_RECOG_OFF_LANG, SHORT_NAME_RECOG_OFF_LANG, GNUM_GENDER_CODE, GNUM_RELATION_CODE, STR_UID, STR_FATHER_NAME, STR_SPOUSE_NAME, STR_MOTHER_NAME, GNUM_NATIONALITY_CODE, GNUM_MARITAL_STATUS_CODE, DT_MARRIAGE, DT_BIRTH, STR_BIRTH_PLACE, NUM_AGE, NUM_IS_HEAD_OF_FAMILY, STR_IS_DEPENDENT, DT_UPTO_DEPENDENT, GNUM_OCCUPATION_CODE, NUM_ISALIVE, NUM_IS_HANDICAPPED, STR_SAME_ORG, STR_OFF_ADD, STR_PRESENT_ADD, STR_PERMANENT_ADD, GNUM_COUNTRY_CODE, GNUM_STATE_CODE, GNUM_DISTRICT_CODE, GNUM_PINCODE, GNUM_HOSPITAL_CODE, GNUM_PATIENT_CAT_CODE, GDT_CATEGORY_VALIDITY, HRGNUM_PUK, NUM_EMERGENCY_NO, GNUM_BLDGRP_CODE, NUM_CR_GENERATION_MODE, GNUM_DESIG_CODE, GNUM_DEPT_CODE, DT_DATE_OF_JOIN, NUM_MOBILE_NO, STR_PER_EMAIL_ID, NUM_BASIC_PAY, DT_DATE_OF_RETIRE, DT_DATE_SEP, GNUM_JOB_TYPE, GNUM_CURRENT_SERVICE_STATUS, GNUM_USER_STATUS, GNUM_GURANTOR_FLAG, GSTR_IMAGE, GSTR_SIGNATURE_IMAGE, GNUM_CR_GENERATION_FLAG, DT_DATE_SEPRATION, DT_PROC_DATE, GNUM_PROC_STATUS FROM bsor_2000_forhmis where str_mid_no='77310200'")
orclcursor.execute("SELECT STR_EMP_NO, NUM_MEM_SL_NO, STR_MID_NO, GNUM_APPELLATION_CODE_1, STR_MEM_FULL_NAME, STR_MEM_SHORT_NAME, FULL_NAME_RECOG_OFF_LANG, SHORT_NAME_RECOG_OFF_LANG, GNUM_GENDER_CODE, GNUM_RELATION_CODE, STR_UID, STR_FATHER_NAME, STR_SPOUSE_NAME, STR_MOTHER_NAME, GNUM_NATIONALITY_CODE, GNUM_MARITAL_STATUS_CODE, DT_MARRIAGE, DT_BIRTH, STR_BIRTH_PLACE, NUM_AGE, NUM_IS_HEAD_OF_FAMILY, STR_IS_DEPENDENT, DT_UPTO_DEPENDENT, GNUM_OCCUPATION_CODE, NUM_ISALIVE, NUM_IS_HANDICAPPED, STR_SAME_ORG, STR_OFF_ADD, STR_PRESENT_ADD, STR_PERMANENT_ADD, GNUM_COUNTRY_CODE, GNUM_STATE_CODE, GNUM_DISTRICT_CODE, GNUM_PINCODE, GNUM_HOSPITAL_CODE, GNUM_PATIENT_CAT_CODE, GDT_CATEGORY_VALIDITY, HRGNUM_PUK, NUM_EMERGENCY_NO, GNUM_BLDGRP_CODE, NUM_CR_GENERATION_MODE, GNUM_DESIG_CODE, GNUM_DEPT_CODE, DT_DATE_OF_JOIN, NUM_MOBILE_NO, STR_PER_EMAIL_ID, NUM_BASIC_PAY, DT_DATE_OF_RETIRE, DT_DATE_SEP, GNUM_JOB_TYPE, GNUM_CURRENT_SERVICE_STATUS, GNUM_USER_STATUS, GNUM_GURANTOR_FLAG, GSTR_IMAGE, GSTR_SIGNATURE_IMAGE, GNUM_CR_GENERATION_FLAG, DT_DATE_SEPRATION, DT_PROC_DATE, GNUM_PROC_STATUS FROM bsor_2000_forhmis")


# Fetch the result of the Oracle query
oracle_data = orclcursor.fetchall()
#postgr_data = pgcursor.fetchall()
##print(oracle_data == postgr_data)

print("Total rows in Oracle are:  ", len(oracle_data))
#print("Total rows in Postgres are:  ", len(postgr_data))

##print(oracle_data)
##print(postgr_data)

#diff=list(set(oracle_data)-set(postgr_data))

#diff=list(set(postgr_data)-set(oracle_data))

#print('The record not in postgres is',diff)


# executing the sql statement
pgcursor.execute('truncate table hrgt_emp_bsl_interface_sks')
pgdb.commit()
# Loop through the result and insert each row into the PostgreSQL table
##for row in oracle_data:
for row1 in oracle_data:
#     print(str(row[0]))
#     pgcursor.execute("INSERT INTO hrgt_emp_bsl_interface_sks(str_emp_no) VALUES (%s)", '773102')
#     pgcursor.execute("INSERT INTO hrgt_emp_bsl_interface_sks(str_emp_no) VALUES (%s)", row)
#      print(row1)
      try:
            pgcursor.execute("INSERT INTO hrgt_emp_bsl_interface_sks VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", row1)
      except Exception as err:
            i=i+1
            print('Error....', i)

#     pgcursor.execute("INSERT INTO hrgt_emp_bsl_interface_sks(str_emp_no, str_mid_no) VALUES (%s,%s)", row)

# Commit the changes to the PostgreSQL database
pgdb.commit()
# Close the cursors and databases
orclcursor.close()
pgcursor.close()
orcl.close()
pgdb.close()




