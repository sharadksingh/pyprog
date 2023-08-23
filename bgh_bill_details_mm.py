###############################################################################
'''
   Program Name: BGH_BILL_DETAILS_MM.PY
   Output File Generated is: F:\pyora\ward_adm_medtpa_vw.csv
   Table Used: Ward_Admission_vw
   Scheduler: runs from the scheduler BGH_BILL_DETAILS_MM
   This Program sends the BILL DETAILS data of mediclaim  to the tpa on Monthly Basis
   Written By: Sharad Kumar Singh, AGM, C&IT
   Working Status: Working
   Version: 1.0
   Created on: 27/12/2018
   Last Modified on: ....
   
'''
###############################################################################
import email, smtplib, ssl

from    email import encoders
from    email.mime.base import MIMEBase
from    email.mime.multipart import MIMEMultipart
from    email.mime.text import MIMEText
import  cx_Oracle
import  datetime
import  time
import  shutil, os
from    datetime import datetime

################################################
# Connect to Oracle and Prepare the CSV File
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()
# Get The data from Oracle and Save it to bill_details_tpamonthly.csv
cur.execute("select a.hospno, a.hospyr, a.hospcg, to_char(a.hcatno) hcatno, b.name, to_char(a.hadmdt,'DD/MM/RR') hadmdt,to_char(a.hdisdt,'DD/MM/RR')disdt,a.hpatid,a.hbillno,to_char(a.hbilldt,'DD/MM/RR') billdt, a.hfinyr, to_char(a.bill_grand_total) bill_amount, to_char((a.bill_adm_advance+a.bill_paid_advance)) total_advance,to_char(a.bilttl)final_abill_amount from wardbill_rgstrpat a,wardbill_catedic  b where a.hospcg='E' and a.hfinyr='18-19' and to_char(a.hbilldt,'MMRRRR')=to_char(trunc(sysdate)-1, 'MMRRRR') and a.hcatno=b.code  order by hospcg, hospno")
file = open(r"F:\pyora\bill_details_tpamonthly.csv", "w")
file.write('HOSP-NO'+ ',' + 'HOSPYR' + ',' + 'CATG' + ',' + 'CATNO' + ',' + 'CAT-Name' + ',' + 'Adm-Dt' + ',' + 'Dis-Dt' + ',' + 'Pat' + ',' + 'Bill-No' + ',' + 'Bill-Dt' + ',' + 'Fin-Yr' + ',' + 'Bill-Tot-Amt' + ',' + 'Tot-Adv' + ',' + 'Final-Amt' + ',' + '\n')
for row in cur:
      file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + ',' + row[10]+ ',' + row[11] + ',' + row[12] + ',' + row[13] + ',' + '\n')
file.close()
cur.close()
conn.close()
################################################
# Form the mail data

subject         = "BGH:BOKARO: Monthly Provisional Bills  For Mediclaim"
body            = ".....PFA the Monthly Provisional Mediclaim Bill data. You can open it in excel. ......SHARAD KUMAR SINGH/For BGH Bokaro"
sender_email    = "citbgh@gmail.com"
receiver_email  = "ssarkar@mdindia.com"
bcc_email       = "singh.sharadk@gmail.com, sail-bokaro@mdindia.com, r.chhetri@mdindia.com, kalkata@mdindia.com"


#password = input("Type your password and press enter:")

username = 'citbgh@gmail.com'
password = 'citbgh@827001'


# Create a multipart message and set headers
message = MIMEMultipart()
message["From"]     = sender_email
message["To"]       = receiver_email
message["Subject"]  = subject
message["Bcc"]      = bcc_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = r"F:\pyora\bill_details_tpamonthly.csv"  # In same directory as script

# Open the  file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())


# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, [receiver_email,bcc_email], text)


#s.sendmail(me, [you,cc], msg.as_string())

# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname1 = (r"F:\pyora\bgh\bgh_archbill_details_tpamonthly.csv."+timestamp )
shutil.copy(r"F:\pyora\bill_details_tpamonthly.csv", dest_fname1)
os.remove(r"F:\pyora\bill_details_tpamonthly.csv")

###############################################################################
