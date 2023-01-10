# -*- coding: utf8 -*-
#Author : Luyoung
#Date : 2023-01-06
#Modify Date : 2023-01-07

import json
import random
import time
import requests
# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header

def main_handler(event, context):

    param1 = {"user":"@qq.com","password":""}
    param2 = {"user":"@qq.com","password":""}
    param3 = {"user":"@qq.com","password":""}
    
    if time.strftime('%H') == '05':
        param1["step"] = str(random.randint(60000, 61000))
        param2["step"] = str(random.randint(30000, 31000))
        param3["step"] = str(random.randint(30000, 31000))
    else:
        param1["step"] = str(random.randint(61000, 63000))
        param2["step"] = str(random.randint(31000, 33000))
        param3["step"] = str(random.randint(31000, 33000))
    
    content = ''
    content += updateStep(json.dumps(param1))
    content += updateStep(json.dumps(param2))
    content += updateStep(json.dumps(param3))

    #发送邮件日志
    sendLog(content)

    return content

def updateStep(param):

    rs = ''
    url = ''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36','Content-Type': 'application/json'}
    try:
        r = requests.post(url, timeout=10, headers=headers, data=param)
        r.raise_for_status()
        if r.status_code== 200:
            r.encoding = 'utf-8'
            rs += time.strftime("%Y-%m-%d %H:%M:%S")+'\n'+r.text+'\n\n'
    except Exception as e:
        rs += str(e)

    return rs

def sendLog(context):

    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = '@qq.com'
    password = ''
    # 收信方邮箱
    to_addr = '@qq.com'
    # 发信服务器
    smtp_server = 'smtp.qq.com'

    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(context, 'plain', 'utf-8')
    # 邮件头信息
    msg['From'] = Header('Zepp Life')  # 发送者
    msg['To'] = Header('')  # 接收者
    subject = '步数修改日志'+time.strftime("%Y-%m-%d %H:%M")
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        # 建立连接--qq邮箱服务和端口号（可百度查询）
        smtpobj.connect(smtp_server, 465)    
        # 登录--发送者账号和口令
        smtpobj.login(from_addr, password)   
        # 发送邮件
        smtpobj.sendmail(from_addr, to_addr, msg.as_string()) 
        #print("邮件发送成功")
    except smtplib.SMTPException as e:
        #发送失败
        str(e)
    finally:
        # 关闭服务器
        smtpobj.quit()
