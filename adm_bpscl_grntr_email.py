###############################################################################
'''
   Program Name: adm_bpscl_grntr_email.py
   Output File Generated is: F:\pyora\adm_bpscl_guarantor_list.csv
   Table Used: adm_edpgrt, emp_master, ward_admission_vw, emp_dep_code
   Scheduler: runs from the scheduler BGH_BILL_DETAILS_MM
   This Program sends the BPSCL Guatantor Data on Monthly basis 
   Written By: Sharad Kumar Singh, AGM, C&IT
   Working Status: Working
   Version: 1.0
   Created on: 27/12/2018
   Last Modified on: ....   
'''
###############################################################################
import      email, smtplib, ssl
from        email import encoders
from        email.mime.base import MIMEBase
from        email.mime.multipart import MIMEMultipart
from        email.mime.text import MIMEText
import      cx_Oracle
import      datetime
import      time
import      shutil, os
from        datetime import datetime
###############################################################################
# Connect to Oracle and Prepare the CSV File
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()

cur.execute("select a.staffno, (b.f_name||' '||b.l_employee) emp_name,b.dept, b.grade_pay, (a.hospno||'/'||a.hospyear) hospno,c.pat_name from bpscl_edpgrt a,bpscl_emp_grnt b,ward_admission_vw  c,emp_dep_code d where a.admdate >= trunc(last_day(sysdate)-1, 'mm') and a.admdate <= last_day(trunc(sysdate)-1) and a.staffno = b.staff_no and  a.hospno = c.hospno and a.hospyear= c.hospyr  order by a.staffno")
file = open(r"F:\pyora\adm_bpscl_guarantor_list.csv", "w")
file.write('STAFF-NO'+ ',' + 'EMP NAME' + ',' + 'DEPTT' + ',' + 'SECTION' + ',' + 'HOSPNO' + ',' + 'PAT NAME' +  ',' + '\n')
for row in cur:
      file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + '\n')

file.close()
cur.close()
conn.close()
################################################################################
# Form the mail data

subject         = "SAIL:BOKARO:BGH:BSL EmployeeGuarantor List for the Month <Do Not Reply To this E-Mail id>!"
body            = "PFA the BSls Guarnator List for the Month..... Sharad Kumar Singh/8986872752"
sender_email    = "citbgh@gmail.com"
receiver_email  = "sunilsharmakumar82@gmail.com"
bcc_email       = "singh.sharadk@gmail.com, bks43035@yahoo.com"

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

filename = r"F:\pyora\adm_bpscl_guarantor_list.csv"  # In same directory as script

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
dest_fname1 = (r"F:\pyora\bgh\bgh_arch\adm_bpscl_guarantor_list.csv."+timestamp )
shutil.copy(r"F:\pyora\adm_bpscl_guarantor_list.csv", dest_fname1)
os.remove(r"F:\pyora\adm_bpscl_guarantor_list.csv")
###############################################################################
