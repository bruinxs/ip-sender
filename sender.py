#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib import request, parse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import argparse

def is_ip_change():
    ip = None
    last_ip = ""

    try:
        u = request.urlopen('https://api.ip.la/')
        resp = u.read()
        ip = resp.decode('utf-8')
    except request.HTTPError as e:
        print(e)

    try:
        with open('last_ip.txt', 'r+') as f:
            last_ip = f.read()
            if last_ip != ip:
                f.write(ip)
    except FileNotFoundError as e:
        with open('last_ip.txt', 'x+') as f:
            f.write(ip)
        print(e)

    if ip != last_ip:
        return ip

def send_mail(smtp_host, smtp_user, smtp_passwd, mail_receiver, ip):
    mail_message = MIMEText(ip, 'plain', 'utf-8')
    mail_message['From'] = smtp_user
    # mail_message['From'] = Header(smtp_user, 'utf-8')
    # mail_message['To'] =  Header(mail_receiver, 'utf-8')
    mail_message['Subject'] = Header('IP变换', 'utf-8')
    try:
        smtp = smtplib.SMTP_SSL(smtp_host, 465) 
        # smtp.set_debuglevel(1)
        smtp.login(smtp_user,smtp_passwd)  
        smtp.sendmail(smtp_user, [mail_receiver], mail_message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件,", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="smtp host", required=True)
    parser.add_argument("-u", "--user", help="smtp user", required=True)
    parser.add_argument("-p", "--passwork", help="smtp passwork", required=True)
    parser.add_argument("-r", "--receiver", help="mail receiver", required=True)
    args = parser.parse_args()

    while True:
        try:
            print("run...")
            ip = is_ip_change()
            if ip :
                send_mail(args.host, args.user, args.passwork, args.receiver, ip)
        except Exception as e:
            print(e)
        time.sleep(600)
    

 
