import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import time 
from myproject.celery_app import app as celery_app
#@celery_app.task


def mail(receiveraddr, fattach):

    fromaddr = "support@crawlzero.com"
    toaddr = receiveraddr
    
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    
    # storing the senders email address   
    msg['From'] = fromaddr 
    
    # storing the receivers email address  
    msg['To'] = toaddr 
    
    # storing the subject  
    msg['Subject'] = "File status"
    
    # string to store the body of the mail 
    body = "You have successgully logged in"
    
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    
    # open the file to be sent  
    filename = "validfile.csv"
    # attachment = open("Path of the file", "rb") 
    attachment = fattach
    
    # # instance of MIMEBase and named as p 
    p = MIMEBase('application/vnd.ms-excel',  'octet-stream') 
    
    # To change the payload into encoded form 
    p.set_payload((attachment)) 
    
    # encode into base64 
    encoders.encode_base64(p) 
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    
    # # attach the instance 'p' to instance 'msg' 
    msg.attach(p) 
    
    # creates SMTP session 
    s = smtplib.SMTP('smtp.ionos.com', 587) 
    
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login(fromaddr, "RajeshRockey@0") 
    
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    
    # terminating the session 
    s.quit() 

def mailfail(receiveraddr, text):

    fromaddr = "support@crawlzero.com"
    toaddr = receiveraddr
    
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    
    # storing the senders email address   
    msg['From'] = fromaddr 
    
    # storing the receivers email address  
    msg['To'] = toaddr 
    
    # storing the subject  
    msg['Subject'] = "File Failed"
    
    # string to store the body of the mail 
    body = text
    
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    
    
    
   
    
 
    # creates SMTP session 
    s = smtplib.SMTP('smtp.ionos.com', 587) 
    
    # start TLS for security 
    s.starttls() 
    
    # Authentication 
    s.login(fromaddr, "RajeshRockey@0") 
    
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    
    # sending the mail 
    s.sendmail(fromaddr, toaddr, text) 
    
    # terminating the session 
    s.quit() 

