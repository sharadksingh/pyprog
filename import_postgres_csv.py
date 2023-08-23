import psycopg2
#conn = psycopg2.connect("host=localhost dbname=postgres user=public")
conn = psycopg2.connect("dbname=postgres user=postgres password=sk940678")
cur = conn.cursor()
with open('mediclaim_data_2022.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'sail_emp_excel_data', sep=',')

conn.commit()
