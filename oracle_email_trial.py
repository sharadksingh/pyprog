import cx_Oracle
import datetime
import smtplib
import tempfile
import os

from email.message import Message
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

today = datetime.datetime.now()
username = 'citbgh@gmail.com'
password = 'citbgh@827001'

# fromaddr   = 'citbgh@gmail.com>' #must be a vaild 'from' addy in your GApps account
# toaddr     = 'ssarkar@gmail.com'

msg = MIMEMultipart()
msg['From'] = 'citbgh@gmail.com'
msg['To'] = 'sharadk.singh@sailbsl.in'
msg['Subject'] = 'Monthly employee report %d/%d ' % (today.month, today.year)

db = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cursor = db.cursor()
cursor.execute("select * from bgh_doctdic order by 1")
report = tempfile.NamedTemporaryFile()
report.write(bytes("<table>", 'UTF-8'))
for row in cursor:
  report.write(bytes("<tr>", 'UTF-8'))
  for field in row:
#     report.write(bytes("<td>%s</td>",'UTF-8'), %field))
#     report.write("<td>%s</td>" % field)
      data = "<td>%s</td>" %field
#     report.write(bytes(data, 'UTF-8'))
      report.write(bytes("<td>%s</td>" % field, 'UTF-8'))

      report.write(bytes("</tr>", 'UTF-8'))
      report.write(bytes("</table>", 'UTF-8'))
report.flush()
cursor.close()
db.close()

attachment = MIMEBase('application', 'vnd.ms-excel')
report.file.seek(0)
attachment.set_payload(report.file.read())
encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment;filename=emp_report_%d_%d.xls' % (today.month, today.year))
msg.attach(attachment)

# server = smtplib.SMTP('smtp.gmail.com:587')

emailserver = smtplib.SMTP('smtp.gmail.com:587')

emailserver.starttls()
emailserver.login(username,password)
#    server.sendmail(msg['From'], [msg['To']], msg.as_string())



emailserver.sendmail(msg['From'], msg['To'], msg.as_string())
emailserver.quit()
