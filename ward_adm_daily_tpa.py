###############################################################################
'''
   Program Name: ward_adm_daily_tpa
   Output File Generated is: F:\pyora\ward_adm_medtpa_vw.csv
   Table Used: Ward_Admission_vw
   Scheduler: runs from the scheduler ipd_adm_daily 
   This Program sends the admisison data of mediclaim  to the tpa on dail basis
   Written By: Sharad Kumar Singh, AGM, C&IT
   Working Status: Working
   Version: 1.0
   Created on: 26/12/2018
   Last Modified on: 20/FEB/2019
   
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


t1 = time.localtime()
timestamp1 = time.strftime('%b-%d-%y',t1)
filename1 = r"F:\pyora\ward_adm_medtpa_vw_"+timestamp1+".csv"  # In same directory as script



################################################
# Connect to Oracle and Prepare the CSV File
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()
#cur.execute("select hospno, hospyr, pat_name, to_char(admdate,'dd/mm/rr'), staff_no from ward_admission_vw where admdate=trunc(sysdate)-1 and category=94 order by 1")
cur.execute("select staff_no minno, to_char(admdate,'dd/mm/rr') admdate, (hospno||'/'||hospyr) hospno, pat_name, pat_sex, to_char(pat_age) pat_age, pat_local_add, pat_admit_unit, pat_adm_doc, nvl(pat_provdiag,'XX') from ward_admission_vw where category='94' and admdate=trunc(sysdate)-1 order by 1")
file = open(filename1, "w")
file.write('MIN-NO'+ ',' + 'ADM Date' + ',' + 'Hosp No' + ',' + 'Pat Name' + ',' + 'Gender' + ',' + 'Age' + ',' + 'Local Addr' + ',' + 'Adm Unit' + ',' + 'Adm Doc' + ',' + 'Prov Diag.' + '\n')
for row in cur:
    file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + '\n')
file.close()
cur.close()
conn.close()
################################################
# Form the mail data

subject         = "BGH:BOKARO:Daily IPD Data For Mediclaim"
body            = ".....PFA the IPD Admission Data for Mediclaim. You can open it in excel. ......SHARAD KUMAR SINGH/For BGH Bokaro"
sender_email    = "citbgh@gmail.com"
#receiver_email  = "sail_bokaro@mdindia.com"
receiver_email  = "sail_bokaro@mdindia.com"
bcc_email       = "kolkata@mdindia.com"
#bcc_email       = "singh.sharadk@gmail.com, sail-bokaro@mdindia.com, r.chhetri@mdindia.com, kalkata@mdindia.com"


#password = input("Type your password and press enter:")

username = 'citbgh@gmail.com'
password = 'citbgh@827001'


# Create a multipart message and set headers
message = MIMEMultipart()
message["From"]     = sender_email
message["To"]       = receiver_email
message["Subject"]  = subject
#message["Bcc"]      = bcc_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

#filename = r"F:\pyora\ward_adm_medtpa_vw.csv"+timestamp1  # In same directory as script



# Open the  file in binary mode
with open(filename1, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())


# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename1}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
#****************************
#server.starttls()
#    server.login(username,password)
#    server.sendmail(msg['From'], [msg['To']], msg.as_string())

#    server.quit() #bye bye
#    os.remove("F:\pyora\ward_med_tpa.csv")
#    os.remove("F:\pyora\ward_med_tpa.xlsx")   
#    server = smtplib.SMTP('smtp.gmail.com:587')
#*************************************
#server = smtplib.SMTP('smtp.gmail.com:587')
#    server.starttls()
#    server.login(username,password)
#    server.sendmail(msg['From'], [msg['To']], msg.as_string())

server=smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(sender_email, [receiver_email,bcc_email], text)



# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname1 = (r"F:\pyora\bgh\bgh_arch\ward_adm_medtpa_vw.csv."+timestamp )
#shutil.copy(r"F:\pyora\ward_adm_medtpa_vw.csv", dest_fname1)
shutil.copy(filename1, dest_fname1)
#os.remove(r"F:\pyora\ward_adm_medtpa_vw.csv")
os.remove(filename1)

###############################################################################
