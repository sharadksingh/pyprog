








######################################################################################################################################
'''
This Program extracts the CLC Worker Master Data from the bgh.clc_worker_master on daily basis
at 06:00 AM and creates a CSV file. The CSV file is then converted to Excel format and sent as
attachment to clcbokaro@gmail.com. A special mail id in this regard has been made
citbgh@gmail.com/citbgh@827001. This is scheduled to run through the windows scheduler
'''

# Python Program to Download Oracle Data to CSV files
import cx_Oracle
import os
import csv
import openpyxl
import smtplib, os, re, sys, glob, string, datetime
from   email.mime.multipart import MIMEMultipart
from   email.mime.base      import MIMEBase
from   email.mime.text import MIMEText
from   email import encoders

# Connection to Oracle
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()

#
#cur.execute("select hospno, hospyr, pat_name, to_char(admdate,'dd/mm/rr') from ward_admission_vw where admdate=trunc(sysdate)-1 order by 1")
#cur.execute("select staff_no minno, to_char(admdate,'dd/mm/rr') admdate, (hospno||'/'||hospyr) hospno, pat_name, pat_sex, to_char(pat_age) pat_age, pat_local_add, pat_admit_unit, pat_provdiag, pat_adm_doc from ward_admission_vw where category='94' and admdate=trunc(sysdate)-1 order by 1")

cur.execute("select nvl(replace(ip_no,'-','.'),'.') ip_no, nvl(replace(rpfc_acc_no,'-','.'),'.') rpfc_acc_no, nvl(replace(bot_acc_no,'-','.'),'.') bot_acc_no, nvl(replace(w_name,'-','.'),'.') w_name, nvl(replace(w_gender,'-','.'),'.') w_gender, nvl(replace(w_phy_hand,'-','.'),'.') w_phy_hand,to_char(w_dob,'DD.MM.RRRR') w_dob, nvl(replace(w_category,'-','.'),'.') w_category, nvl(replace(fh_code,'-','.'),'.') fh_code, nvl(blood_group,'.') blood_group, nvl(replace(marital_status,'-','.'),'.') marital_status, nvl(replace(displaced_status,'-','.'),'.') displaced_status,nvl(replace(fh_name,'-','.'),'.') fh_name, nvl(replace(mother_name,'-','.'),'.') mother_name, nvl(replace(spouse_name,'-','.'),'.') spouse_name,nvl(replace(ident_mark,'-','.'),'.') ident_mark,nvl(replace(t_address1,',','.'),'.') t_address1,nvl(replace(t_address2,',','.'),'.') t_address2,nvl(replace(t_city,',','.'),'.') t_city,nvl(replace(t_pincode,'-','.'),'.') t_pincode,nvl(replace(t_cntry_code,'-','.'),'.') t_cntry_code,nvl(replace(t_telno,'-','.'),'.') t_telno,nvl(replace(t_state,'-','.'),'.') t_state,nvl(replace(email_id,'-','.'),'.') email_id,nvl(replace(p_address1,',','.'),'.') p_address1,nvl(replace(p_address2,',','.'),'.') p_address2,nvl(replace(p_city,',','.'),'.') p_city,nvl(replace(p_pincode,'-','.'),'.') p_pincode,nvl(replace(p_cntry_code,'-','.'),'.') p_cntry_code,nvl(replace(p_telno,'-','.'),'.') p_telno,nvl(replace(p_state,'-','.'),'.') p_state,nvl(replace(bank_key,'-','.'),'.') bank_key,nvl(replace(bank_accno,'-','.'),'.') bank_accno,nvl(replace(pan_no,'-','.'),'.') pan_no,nvl(doc_verification,'Y')  doc_verification,nvl(replace(id_docno,'-','.'),'.') id_docno,nvl(replace(principal_emp,'-','.'),'.') principal_emp,nvl(replace(m_user,'-','.'),'.') m_user, to_char(m_entdate,'DD.MM.RRRR') ent_date,to_char(m_ctrl_no) m_ctrl_no ,nvl(replace(id_proof,'-','.'),'.') id_proof,(nvl(aadhaar_no,'')||'') aadhaar_no from clc_worker_master where m_user != '1000' and trunc(m_entdate)=trunc(sysdate)-1  and length(ip_no) >= 10     order by m_user")

file = open("F:\pyora\clc_worker_master.csv", "w")

file.write('IP-NO'+ ',' + 'RPFC Acc No' + ',' + 'BOT Acc No' + ',' + 'W-Name' + ',' + 'W-Gender' + ',' + 'Phy-Hand' + ',' + 'Dob' + ',' + 'Cat' + ',' + 'FH-Cd' + ',' + 'B-Gr.' + ',' + 'M-Status' + ',' + 'Disp-St' + ',' + 'FH-Name' + ',' + 'M-Name' + ',' + 'SP-NAme.' + ',' + 'I-Mark' + ',' + 'T_Add1.' + ',' +  'T-Add2.' +  ',' + 'T-City.' + ',' + 'T-Pin.' + ',' + 'T-CCode.' + ',' + 'T-TelNo.' + ',' + 'T_State.' +  ',' + 'Email-Id.' + ',' + 'P-Add1' + ',' + 'P-Add2.' + ',' +'P-City' + ',' + 'P-Pin.' + ',' + 'P-CCode.' + ',' + 'P-Tel.' + ',' +  'P-St.' + ',' + 'Bank-Key.' + ',' + 'Acc No.' + ',' + 'PAN' + ',' + 'Doc' + ',' + 'Id-Doc' + ',' + 'P-Emp' + ',' +  'M-User.' + ',' +  'EntDt' + ',' + 'CtrlNo' + ',' + 'Id-Proof' + ',' + 'Aadhar' + '\n')
for row in cur:
#     file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + '\n')
      file.write(row[0]+ ',' + row[1] + ',' + row[2] + ',' + row[3] + ',' + row[4] + ',' + row[5] + ',' + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + ',' + row[10]+ ',' + row[11] + ',' + row[12] + ',' + row[13] + ',' + row[14] + ',' + row[15] + ',' + row[16] + ',' + row[17] + ',' + row[18] + ',' + row[19] + ','+ row[20]+ ',' + row[21] + ',' + row[22] + ',' + row[23] + ',' + row[24] + ',' + row[25] + ',' + row[26] + ',' + row[27] + ',' + row[28] + ',' + row[29] + ','+ row[30]+ ',' + row[31] + ',' + row[32] + ',' + row[33] + ',' + row[34] + ',' + row[35] + ',' + row[36] + ',' + row[37] + ',' + row[38] + ',' + row[39]+ ',' + row[40] + ',' + row[41] + '\n')

file.close()
cur.close()
conn.close()
##############################################################################################################################################
# Convert the CSV To Excel File Let see what happens
wb = openpyxl.Workbook()
ws = wb.active
f = open('F:\pyora\clc_worker_master.csv')
reader = csv.reader(f, delimiter=',')
for row in reader:
     ws.append(row)
f.close()
wb.save('F:\pyora\clc_worker_master.xlsx')


##########################################################################################################################
##### SEND MAIL WITH ATTACHMENT USING PYTHON
#attachmentname = 'F:\pyora\ward_med_tpa.csv' #path to an attachment, if you wish
attachmentname  = 'F:\pyora\clc_worker_master.xlsx' #path to an attachment, if you wish

username = 'citbgh@gmail.com'
password = 'citbgh@827001'

fromaddr   = 'citbgh@gmail.com>' #must be a vaild 'from' addy in your GApps account
toaddr     = 'clcbokaro@gmail.com'

#toaddr     = 'mdindiabokaro@gmail.com'
#toaddr    = 'mdindiabokaro@gmail.com'
ccaddr     = 'singh.sharadk@gmail.com'
#toaddr     = [toaddr] + ccaddr 

replyto    = fromaddr #unless you want a different reply-to
msgsubject = 'SAIL:BOKARO:CLC:CLC Worker Master Data<Do Not Reply To this E-Mail id>!'

htmlmsgtext = """Dear Sir/Madam<br/>

                  PFA the CLC Worker Master Data. This is automatically scheuled to be sent through the system at 06:00 AM on daily basis.
                  If there is any issue revert back with the issue to bslsrm@sailbsl.in
                  
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
    os.remove("F:\pyora\clc_worker_master.csv")
    os.remove("F:\pyora\clc_worker_master.xlsx")
    
except:
    print ('Email NOT sent to %s successfully. %s ERR: %s %s %s ', str(toaddr), 'tete', str(sys.exc_info()[0]), str(sys.exc_info()[1]), str(sys.exc_info()[2]) )
    #just in case

############################################################################################################################################
