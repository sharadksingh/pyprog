###############################################################################
'''
   Program Name: death_report_monthly.py
   Birth Report Data Sending to teph.bsl@gmail.com every month   
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
filename1 = r"death_report_monthly_"+timestamp1+".csv"  # In same directory as script



################################################
# Connect to Oracle and Prepare the CSV File
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()


#select yearly_no, dely_date, hospno, hospyr, adm_date, patient_name, pat_age,  
#baby1_gender, baby1_live, baby1_birth_time||nvl(baby1_ampm, '') b1_birth_time ,baby1_wt,
#baby2_gender, baby2_live, baby2_birth_time||nvl(baby2_ampm, '') b2_birth_time ,baby2_wt,
#baby3_gender, baby3_live, baby3_birth_time||nvl(baby3_ampm, '') b3_birth_time ,baby3_wt,
#address, religion
#from LABOUR_ROOM_STATS_2020
#where dely_date between '01-JUN-2020' and '30-JUN-2020'
#order by yearly_no




#cur.execute("select hospno, hospyr, pat_name, to_char(admdate,'dd/mm/rr'), staff_no from ward_admission_vw where admdate=trunc(sysdate)-1 and category=94 order by 1")
#cur.execute("select staff_no minno, to_char(admdate,'dd/mm/rr') admdate, (hospno||'/'||hospyr) hospno, pat_name, pat_sex, to_char(pat_age) pat_age,
#            pat_local_add, pat_admit_unit, pat_adm_doc, nvl(pat_provdiag,'XX') from ward_admission_vw where category='94' and admdate=trunc(sysdate)-1 order by 1")
#cur.execute("select to_char(yearly_no) yearly_no, to_char(dely_date,'DD/MM/RRRR') dely_date, to_char((hospno||'-'||hospyr)) hospno, to_char(adm_date,'DD/MM/RRRR') adm_date,patient_name, to_char(pat_age) pat_age, baby1_gender, baby1_live, baby1_birth_time||nvl(baby1_ampm, 'X') b1_birth_time,to_char(baby1_wt) baby1_wt, nvl(baby2_gender,'X') baby2_gender, nvl(baby2_live,'X'), baby2_birth_time||nvl(baby2_ampm, 'X') b2_birth_time, to_char(baby2_wt) baby2_wt, nvl(baby3_gender,'X'), nvl(baby3_live,'X'), baby3_birth_time||nvl(baby3_ampm, 'X') b3_birth_time, to_char(baby3_wt) baby3_wt,address, religion from LABOUR_ROOM_STATS_2020 where dely_date between '01-JUN-2020' and '30-JUN-2020' order by 1")


cur.execute("select name, hospno, age, gender, dept, unit, adm_date, adm_time, death_date, death_time from ward_stat_death_view where death_dt between trunc(add_months(sysdate,-1),'MM') and trunc(last_day(add_months(sysdate,-1))) order by 1")
            
file = open(filename1, "w")
file.write('NAME'+ ',' + 'HOSPNO' + ',' + 'AGE' + ',' + 'GENDER' + ',' + 'DEPT' + ',' + 'UNIT' + ',' + 'ADM-DATE' + ',' + 'ADM-TIME' + ',' + 'DEATH-DT' + ',' + 'DEATH-TM' + '\n')
for row in cur:
#        file.write(str(row[0])+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] +  + '\n')
        file.write(str(row[0])+ ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4]) + ',' + str(row[5]) + ',' + str(row[6]) + ',' + str(row[7]) + ',' + str(row[8]) + ',' + str(row[9]) + '\n')

file.close()
cur.close()
conn.close()
################################################
# Form the mail data

subject         = "Death Report : BGH:BOKARO:Monthly Death Report Data:"
body            = "Dear Sir, Please Find Attached the Monthly Death Report Data  You can open it in excel. ......Sharad Kumar Singh/For BGH Bokaro"
sender_email    = "citbgh@gmail.com"
receiver_email  = "teph.bsl@gmail.com"
bcc_email       = "singh.sharadk@gmail.com"

username = 'citbgh@gmail.com'
password = 'citbgh@827001'


# Create a multipart message and set headers
message = MIMEMultipart()
message["From"]     = sender_email
message["To"]       = receiver_email
message["Subject"]  = subject
message.attach(MIMEText(body, "plain"))

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
server=smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(sender_email, [receiver_email,bcc_email], text)


# Do the Clean Up Jobs
t = time.localtime()
timestamp = time.strftime('%b-%d-%y_%H%M',t)
dest_fname1 = (r"F:\pyora\bgh\bgh_arch\death_report_monthly.csv."+timestamp )
shutil.copy(filename1, dest_fname1)
os.remove(filename1)

###############################################################################
