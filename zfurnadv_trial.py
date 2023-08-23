import string, cx_Oracle

## Define Oracle connection - format ("username/password@TNSNAME")
ora_conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
ora_cursor  = ora_conn.cursor()

ora_sap=cx_Oracle.connect('SAPRP1/bslrup03@10.143.106.5:1521/RP1')
sap_cursor=ora_sap.cursor()

ora_cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT ='YYYYMMDD'")
sap_cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT ='YYYYMMDD'")

## Truncate our destination tables
ora_cursor.execute("truncate table zfurnadv_ora")

## Grab our "Source Data"
sap_cursor.execute("""select MANDT,SLNO,SPNO,STAFFNO,GRADE,INSTALMENT,APPLDATE from zfuradv WHERE ROWNUM=1""")

## Transfer our cursor rows into a python list object
ResultSet_Py_List = []  #Create an empty list
for MANDT,SLNO,SPNO,STAFFNO,GRADE,INSTALMENT,APPLDATE in sap_cursor:
    try:   #Then populate it with the cursor results
        ResultSet_Py_List.append((MANDT,SLNO,SPNO,STAFFNO,GRADE,INSTALMENT,APPLDATE))
    except AttributeError:
        pass

## Quick count to see how many rows we're packin'!
print(str(len(ResultSet_Py_List)) + ' Records from Source')
print(str((ResultSet_Py_List)) + ' Records from Source')

## Insert the list contents into Oracle, row by row...
ora_cursor.prepare("""INSERT INTO ZFURNADV_ORA(MANDT,SLNO,SPNO,STAFFNO,GRADE,INSTALMENT,APPLDATE)
VALUES (:MANDT,:SLNO,:SPNO,:STAFFNO,:GRADE,:INSTALMENT,:APPLDATE)""")

ora_cursor.executemany(None, ResultSet_Py_List)
ora_conn.commit() #COMMIT that shit before it gets away!


ora_cursor.execute("select count(*) from ZFURNADV_ORA")
ora_row_count = ora_cursor.fetchone()
print(str(ora_row_count[0]) + ' Records INSERTED into Oracle table')


## All done, Lars. Now lets get a drink.

## We will even be nice and close the connections.
##       Its like tipping your hat to the Database engine.
ora_sap.close()
ora_conn.close()

