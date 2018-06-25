#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib import request, parse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import configparser, argparse

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
        with open('/tmp/last_ip.txt', 'r') as f:
            last_ip = f.read()
        if last_ip != ip:
            with open('/tmp/last_ip.txt', 'w') as f:
                f.write(ip)
    except FileNotFoundError as e:
        with open('/tmp/last_ip.txt', 'x+') as f:
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
    parser.add_argument("-c", "--config", help="config file", required=True)
    args = parser.parse_args()
    
    try:
        config = configparser.ConfigParser()
        config.read(args.config)
        host = config[config.default_section]["host"]
        user = config[config.default_section]["user"]
        passwork = config[config.default_section]["passwork"]
        receiver = config[config.default_section]["receiver"]

        if host == "" or user == "" or  receiver == "":
            print(args.config, "config is illegal")
            exit(1)

    except Exception as e:
        print(e)
        exit(1)

    while True:
        try:
            print("run...")
            ip = is_ip_change()
            if ip :
                send_mail(host, user, passwork, receiver, ip)
        except Exception as e:
            print(e)
        time.sleep(600)
    

 
