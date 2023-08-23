###############################################################################
'''
   Program Name: clc_worker_master_xls.py
   Output File Generated is: F:\pyora\clc_worker_master.csv
   Table Used: clc_worker_master
   Scheduler: runs from the scheduler IPD_MED_TPA 
   This Program sends the clc worker master data on daily basis
   Written By: Sharad Kumar Singh, AGM, C&IT
   Working Status: Working
   Version: 1.0
   Created on: 26/12/2018
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
conn = cx_Oracle.connect('bgh/hpv185e@10.143.100.36:1521/bgh6')
cur  = conn.cursor()

#cur.execute("select nvl(replace(ip_no,'-','.'),'.') ip_no, nvl(replace(rpfc_acc_no,'-','.'),'.') rpfc_acc_no, nvl(replace(bot_acc_no,'-','.'),'.') bot_acc_no, nvl(replace(w_name,'-','.'),'.') w_name, nvl(replace(w_gender,'-','.'),'.') w_gender, nvl(replace(w_phy_hand,'-','.'),'.') w_phy_hand,to_char(w_dob,'DD.MM.RRRR') w_dob, nvl(replace(w_category,'-','.'),'.') w_category, nvl(replace(fh_code,'-','.'),'.') fh_code, nvl(blood_group,'.') blood_group, nvl(replace(marital_status,'-','.'),'.') marital_status, nvl(replace(displaced_status,'-','.'),'.') displaced_status,nvl(replace(fh_name,'-','.'),'.') fh_name, nvl(replace(mother_name,'-','.'),'.') mother_name, nvl(replace(spouse_name,'-','.'),'.') spouse_name,nvl(replace(ident_mark,'-','.'),'.') ident_mark,nvl(replace(t_address1,',','.'),'.') t_address1,nvl(replace(t_address2,',','.'),'.') t_address2,nvl(replace(t_city,',','.'),'.') t_city,nvl(replace(t_pincode,'-','.'),'.') t_pincode,nvl(replace(t_cntry_code,'-','.'),'.') t_cntry_code,nvl(replace(t_telno,'-','.'),'.') t_telno,nvl(replace(t_state,'-','.'),'.') t_state,nvl(replace(email_id,'-','.'),'.') email_id,nvl(replace(p_address1,',','.'),'.') p_address1,nvl(replace(p_address2,',','.'),'.') p_address2,nvl(replace(p_city,',','.'),'.') p_city,nvl(replace(p_pincode,'-','.'),'.') p_pincode,nvl(replace(p_cntry_code,'-','.'),'.') p_cntry_code,nvl(replace(p_telno,'-','.'),'.') p_telno,nvl(replace(p_state,'-','.'),'.') p_state,nvl(replace(bank_key,'-','.'),'.') bank_key,nvl(replace(bank_accno,'-','.'),'.') bank_accno,nvl(replace(pan_no,'-','.'),'.') pan_no,nvl(doc_verification,'Y')  doc_verification,nvl(replace(id_docno,'-','.'),'.') id_docno,nvl(replace(principal_emp,'-','.'),'.') principal_emp,nvl(replace(m_user,'-','.'),'.') m_user, to_char(m_entdate,'DD.MM.RRRR') ent_date,to_char(m_ctrl_no) m_ctrl_no ,nvl(replace(id_proof,'-','.'),'.') id_proof,(nvl(aadhaar_no,'')||'') aadhaar_no from clc_worker_master where m_user != '1000' and trunc(m_entdate)=trunc(sysdate)-1  and length(ip_no) >= 10     order by m_user")
#cur.execute("select str(ip_no), str(rpfc_acc_no), str(bot_acc_no), str(w_name), str(w_gender), str(w_phy_hand), str(w_dob), str(w_category), str(fh_code), str(blood_group), str(marital_status), str(displaced_status), str(fh_name), str(mother_name),str(spouse_name),str(ident_mark),str(t_address1), str(t_address2), str(t_city), str(t_pincode), str(t_cntry_code), str(t_telno), str(t_state), str(email_id), str(p_address1), str(p_address2), str(p_city), str(p_pincode), str(p_cntry_code), str(p_telno), str(p_state), str(bank_key), str(bank_accno), str(pan_no), str(doc_verification), str(id_docno), str(principal_emp) ,str(m_user) , str(ent_date), str(m_ctrl_no) , str(id_proof), str(aadhaar_no) from clc_worker_master_view where  trunc(m_entdate)>='28-DEC-2018'  and trunc(m_entdate)<='30-DEC-2018'     order by m_user")
#cur.execute("select ip_no, str(rpfc_acc_no), str(bot_acc_no), str(w_name), str(w_gender), str(w_phy_hand), str(w_dob), str(w_category), str(fh_code), str(blood_group), str(marital_status), str(displaced_status), str(fh_name), str(mother_name),str(spouse_name),str(ident_mark),str(t_address1), str(t_address2), str(t_city), str(t_pincode), str(t_cntry_code), str(t_telno), str(t_state), str(email_id), str(p_address1), str(p_address2), str(p_city), str(p_pincode), str(p_cntry_code), str(p_telno), str(p_state), str(bank_key), str(bank_accno), str(pan_no), str(doc_verification), str(id_docno), str(principal_emp) ,str(m_user) , str(ent_date), str(m_ctrl_no) , str(id_proof), str(aadhaar_no) from clc_worker_master_view where  trunc(m_entdate)>='28-DEC-2018'  and trunc(m_entdate)<='30-DEC-2018'     order by m_user")
#cur.execute("select ip_no,  rpfc_acc_no  ,  bot_acc_no  ,  w_name  ,  w_gender  ,  w_phy_hand  ,  w_dob  ,  w_category  ,  fh_code  ,  blood_group  ,  marital_status  ,  displaced_status  ,  fh_name  ,  mother_name  , spouse_name  , ident_mark  , t_address1  ,  t_address2  ,  t_city  ,  t_pincode  ,  t_cntry_code  ,  t_telno  ,  t_state  ,  email_id  ,  p_address1  ,  p_address2  ,  p_city  ,  p_pincode  ,  p_cntry_code  ,  p_telno  ,  p_state  ,  bank_key  ,  bank_accno  ,  pan_no  ,  doc_verification  ,  id_docno  ,  principal_emp   , m_user   ,  ent_date  ,  m_ctrl_no   ,  id_proof  ,  aadhaar_no   from clc_worker_master_view where  trunc(m_entdate)=trunc(sysdate)-1 order by m_user") 
cur.execute("select ip_no,  rpfc_acc_no  ,  bot_acc_no  ,  w_name  ,  w_gender  ,  w_phy_hand  ,  w_dob  ,  w_category  ,  fh_code  ,  blood_group  ,  marital_status  ,  displaced_status  ,  fh_name  ,  mother_name  , spouse_name  , ident_mark  , t_address1  ,  t_address2  ,  t_city  ,  t_pincode  ,  t_cntry_code  ,  t_telno  ,  t_state  ,  email_id  ,  p_address1  ,  p_address2  ,  p_city  ,  p_pincode  ,  p_cntry_code  ,  p_telno  ,  p_state  ,  bank_key  ,  bank_accno  ,  pan_no  ,  doc_verification  ,  id_docno  ,  principal_emp   , m_user   ,  ent_date  ,  m_ctrl_no   ,  id_proof  ,  aadhaar_no   from clc_worker_master_view where  trunc(m_entdate)>='27-DEC-2018' and trunc(m_entdate)<='02-JAN-2019' order by m_user") 

file = open(r"F:\pyora\clc_worker_master.csv", "w")
file.write('IP-NO'+ ',' + 'RPFC Acc No' + ',' + 'BOT Acc No' + ',' + 'W-Name' + ',' + 'W-Gender' + ',' + 'Phy-Hand' + ',' + 'Dob' + ',' + 'Cat' + ',' + 'FH-Cd' + ',' + 'B-Gr.' + ',' + 'M-Status' + ',' + 'Disp-St' + ',' + 'FH-Name' + ',' + 'M-Name' + ',' + 'SP-NAme.' + ',' + 'I-Mark' + ',' + 'T_Add1.' + ',' +  'T-Add2.' +  ',' + 'T-City.' + ',' + 'T-Pin.' + ',' + 'T-CCode.' + ',' + 'T-TelNo.' + ',' + 'T_State.' +  ',' + 'Email-Id.' + ',' + 'P-Add1' + ',' + 'P-Add2.' + ',' +'P-City' + ',' + 'P-Pin.' + ',' + 'P-CCode.' + ',' + 'P-Tel.' + ',' +  'P-St.' + ',' + 'Bank-Key.' + ',' + 'Acc No.' + ',' + 'PAN' + ',' + 'Doc' + ',' + 'Id-Doc' + ',' + 'P-Emp' + ',' +  'M-User.' + ',' +  'EntDt' + ',' + 'CtrlNo' + ',' + 'Id-Proof' + ',' + 'Aadhar' + '\n')
for row in cur:
#       file.write(str(row[0]).replace(',',' ')+'\n')
        file.write(str(row[0]).replace(',',' ')+ ',' + str(row[1]).replace(',',' ') + ',' + str(row[2]).replace(',',' ') + ',' + str(row[3]).replace(',',' ') + ',' + str(row[4]).replace(',',' ') + ',' + str(row[5]).replace(',',' ') + ',' + str(row[6]).replace(',',' ') + ',' + str(row[7]).replace(',',' ') + ',' + str(row[8]).replace(',',' ') + ',' + str(row[9]).replace(',',' ') + ',' + str(row[10]).replace(',',' ') + ',' + str(row[11]).replace(',',' ') + ',' + str(row[12]).replace(',',' ') + ',' + str(row[13]).replace(',',' ') + ',' + str(row[14]).replace(',',' ') + ',' + str(row[15]).replace(',',' ') + ',' + str(row[16]).replace(',',' ') + ',' + str(row[17]).replace(',',' ') + ',' + str(row[18]).replace(',',' ') + ',' + str(row[19]).replace(',',' ') + ','+ str(row[20]).replace(',',' ')+ ',' + str(row[21]).replace(',',' ') + ',' + str(row[22]).replace(',',' ') + ',' + str(row[23]).replace(',',' ') + ',' + str(row[24]).replace(',',' ') + ',' + str(row[25]).replace(',',' ') + ',' + str(row[26]).replace(',',' ') + ',' + str(row[27]).replace(',',' ') + ',' + str(row[28]).replace(',',' ') + ',' + str(row[29]).replace(',',' ') + ','+ str(row[30]).replace(',',' ')+ ',' + str(row[31]).replace(',',' ') + ',' + str(row[32]).replace(',',' ') + ',' + str(row[33]).replace(',',' ') + ',' + str(row[34]).replace(',',' ') + ',' + str(row[35]).replace(',',' ') + ',' + str(row[36]).replace(',',' ') + ',' + str(row[37]).replace(',',' ') + ',' + str(row[38]).replace(',',' ') + ',' + str(row[39]).replace(',',' ') + ',' + str(row[40]).replace(',',' ') + ',' + str(row[41]).replace(',',' ') + '\n')
file.close()
cur.close()
conn.close()
################################################################################
# Form the mail data

subject         = "SAIL:BOKARO:CLC:CLC Worker Master Data<Do Not Reply To this E-Mail id>!"
body            = "PFA the CLC Worker Master Data..... Sharad Kumar Singh/8986872752"
sender_email    = "citbgh@gmail.com"
#receiver_email  = "clcbokaro@gmail.com"
#bcc_email       = "singh.sharadk@gmail.com, s.sinha@sailbsl.in, shakti2k@gmail.com"
receiver_email  = "clcbokaro@gmail.com"
bcc_email       = "shakti2k@gmail.com"


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

filename = r"F:\pyora\clc_worker_master.csv"  # In same directory as script

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
dest_fname1 = (r"F:\pyora\bgh\bgh_arch\clc_worker_master.csv."+timestamp )
shutil.copy(r"F:\pyora\clc_worker_master.csv", dest_fname1)
os.remove(r"F:\pyora\clc_worker_master.csv")

###############################################################################
