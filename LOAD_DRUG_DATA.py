import psycopg2
conn = psycopg2.connect("host=10.143.106.163 port=5444 dbname=hmis_sail user=hmissail password=h1m2i3s4sail")
cur = conn.cursor()
with open('ISSUE_NOTE_30122022.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'pharma_issue_slip_data', sep=',')


conn.commit()



## DRUG_DATA_SUBSTORE_STOCK_28SEP2022






