# Python Program to Download Oracle Data to CSV files
import cx_Oracle
import os
import smtplib, os, re, sys, glob, string, datetime
from   email.mime.multipart import MIMEMultipart
from   email.mime.base      import MIMEBase
from   email.mime.text import MIMEText
from   email import encoders

# Connection to Oracle
conn = cx_Oracle.connect('ward/hpv185e@10.143.55.53:1521/bghward')
cur  = conn.cursor()

#
#cur.execute("select hospno, hospyr, pat_name, to_char(admdate,'dd/mm/rr') from ward_admission_vw where admdate=trunc(sysdate)-1 order by 1")
#cur.execute("select staff_no minno, to_char(admdate,'dd/mm/rr') admdate, (hospno||'/'||hospyr) hospno, pat_name, pat_sex, to_char(pat_age) pat_age, pat_local_add, pat_admit_unit, pat_provdiag, pat_adm_doc from ward_admission_vw where category='94' and admdate=trunc(sysdate)-1 order by 1")

cur.execute("select staff_no minno, to_char(admdate,'dd/mm/rr') admdate, (hospno||'/'||hospyr) hospno, pat_name, pat_sex, to_char(pat_age) pat_age, pat_local_add, pat_admit_unit, pat_adm_doc, nvl(pat_provdiag,'XX') from ward_admission_vw where category='94' and admdate=trunc(sysdate)-1 order by 1")


file = open("F:\pyora\ward_med_tpa.csv", "w")

file.write('MIN-NO'+ ',' + 'ADM Date' + ',' + 'Hosp No' + ',' + 'Pat Name' + ',' + 'Gender' + ',' + 'Age' + ',' + 'Local Addr' + ',' + 'Adm Unit' + ',' + 'Adm Doc' + ',' + 'Prov Diag.' + '\n')
for row in cur:
#     file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + '\n')
      file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + '\n')

file.close()
cur.close()
conn.close()
##############################################################################################################################################

##### SEND MAIL WITH ATTACHMENT USING PYTHON
attachmentname = 'F:\pyora\ward_med_tpa.csv' #path to an attachment, if you wish
username = 'singh.sharadk@gmail.com'
password = 'mayerton940678'

fromaddr   = 'singh.sharadk@gmail.com>' #must be a vaild 'from' addy in your GApps account
toaddr     = 'mdindiabokaro@gmail.com'
#toaddr    = 'mdindiabokaro@gmail.com'
ccaddr     = 'singh.sharadk@gmail.com'
#toaddr     = [toaddr] + ccaddr 

replyto    = fromaddr #unless you want a different reply-to
msgsubject = 'SAIL:BOKARO:BGH:Daily Mediclaom Patient Admission Data!'

htmlmsgtext = """Dear Sir/Madam<br/>
                  PFA the IPD Admission Data of Mediclaim Patients at SAIL. Bokaro General Hospital in CSV format. You can open it in excel.
                  Best Regards
                  Sharad/8986872752</br>
                <b>Done!</a>"""

#ok, here goes nothing
try:

    msgtext = htmlmsgtext.replace('<b>','').replace('</b>','').replace('<br>',"\r").replace('</br>',"\r").replace('<br/>',"\r").replace('</a>','')
    msgtext = re.sub('<.*?>','',msgtext)

    #pain the ass mimey stuff
    msg = MIMEMultipart()
    msg.preamble = 'This is a multi-part message in MIME format.\n'
    msg.epilogue = ''

    body = MIMEMultipart('alternative')
    body.attach(MIMEText(msgtext))
    body.attach(MIMEText(htmlmsgtext, 'html'))
    msg.attach(body)

    if 'attachmentname' in globals(): #DO WE HAZ ATTACHMENT?
        f = attachmentname
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(f,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    msg.add_header('From', fromaddr)
    msg.add_header('To', toaddr)
#    msg['Cc']=  cc
    ##msg.add_header('Cc', ccaddy)    #doesn't work apparently
    ##msg.add_header('Bcc', bccaddy)  #doesn't work apparently
    msg.add_header('Subject', msgsubject)
    msg.add_header('Reply-To', replyto)

    # The actual email sendy bits
    server = smtplib.SMTP('smtp.gmail.com:587')
#   server = smtplib.SMTP('10.143.2.106:25')
        
    server.set_debuglevel(True) #commenting this out, changing to False will make the script give NO output at all upon successful completion
#    server.set_debuglevel(False) #commenting this out, changing to False will make the script give NO output at all upon successful completion

    server.starttls()
    server.login(username,password)
    server.sendmail(msg['From'], [msg['To']], msg.as_string())

    server.quit() #bye bye
    os.remove("F:\pyora\ward_med_tpa.csv")
except:
    print ('Email NOT sent to %s successfully. %s ERR: %s %s %s ', str(toaddr), 'tete', str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2]) )
    #just in case

############################################################################################################################################
