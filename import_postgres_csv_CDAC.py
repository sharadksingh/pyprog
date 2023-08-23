import psycopg2
conn = psycopg2.connect("host=10.143.106.163 port=5444 dbname=hmis_sail user=hmissail password=h1m2i3s4sail")
cur = conn.cursor()
with open('10700576.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f) # Skip the header row.
    cur.copy_from(f, 'hrgt_emp_dependent_interface', sep='|')


conn.commit()






