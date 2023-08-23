###############################################################################
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cx_Oracle

################################################
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()
cur.execute("select hospno, hospyr, pat_name, to_char(admdate,'dd/mm/rr'), staff_no from ward_admission_vw where admdate=trunc(sysdate)-1 and category=94 order by 1")
file = open("ward_adm_medtpa_vw.csv", "w")
for row in cur:
     file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + '\n')
file.close()
cur.close()
conn.close()
################################################


subject = "BGH:BOKARO:Daily IPD Data For Mediclaim"
body = ".....PFA the IPD Admission Data for Mediclaim. You can open it in excel. ......SHARAD KUMAR SINGH/For BGH Bokaro"
sender_email = "citbgh@gmail.com"
receiver_email = "ssarkar@mdindia.com"
#bcc_email = "sharadk.singh@sailbsl.in"
bcc_email     = "singh.sharadk@gmail.com, sail-bokaro@mdindia.com, r.chettri@mdindia.com, kalkata@mdindia.com"
#bcc        = 'singh.sharadk@gmail.com; sail-bokaro@mdindia.com; r.chettri@mdindia.com; kalkata@mdindia.com'


#password = input("Type your password and press enter:")

username = 'citbgh@gmail.com'
password = 'citbgh@827001'


# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = bcc_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = r"F:\pyora\ward_adm_medtpa_vw.csv"  # In same directory as script

# Open PDF file in binary mode
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


#    s.sendmail(me, [you,cc], msg.as_string())
###############################################################################


