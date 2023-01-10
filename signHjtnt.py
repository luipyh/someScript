# -*- coding: utf8 -*-
#Author : Luyoung
#Date : 2023-01-09
#Modify Date : 2023-01-10

import json
import random
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def main_handler(event, context):

    requests.packages.urllib3.disable_warnings()

    log = ''

    cookie = login()
    log = getLog(cookie)

    if log != '':
        sendLog(log)
    else:
        log = getLog(cookie)

    if log != '':
        sendLog(log)
    else:
        sendLog("数据获取失败！")

def getLog(cookie):

    signLog = ''
    for i in range(10):
        signLog = sign(cookie)
        if signLog != '':
            break

    getUseDataLog = ''
    for i in range(10):
        getUseDataLog = getUseData(cookie)
        if getUseDataLog != '':
            break

    if signLog != '' and getUseDataLog != '':
        return getUseDataLog + signLog
    return ''
    

def doRequests(method, url, headers, data, proxies, verify):

    if method == "get":
        response = requests.get(url, timeout=10, headers=headers, data=data, proxies=proxies, verify=verify)
    elif method == "post":
        response = requests.post(url, timeout=10, headers=headers, data=data, proxies=proxies, verify=verify)
    
    response.raise_for_status()

    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response

    return ""

def login():

    url = 'https://www.hjtnt.link/auth/login'

    cookie = ''
    params = ["uid","email","key","ip","expire_in"]
    data = {"email":"@qq.com","passwd":"","code":"","remember_me":"on"}    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #'path': '/user/checkin',
        #'scheme': 'https',
        #'method': 'POST',
        #'authority': 'www.hjtnt.link',
        #'accept': 'application/json, text/javascript, */*; q=0.01',
        #'accept-encoding': 'gzip, deflate, br',
        #'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    try:
        response = doRequests('post', url, headers, data, '', False)
        if response != '':
            headers = str(response.headers).replace('\'','\"')
            headersDict = json.loads(headers)
            Set_Cookie = headersDict["Set-Cookie"].split(';')
            for i in Set_Cookie:
                v = i.replace(" path=/, ","")
                if v.split("=")[0] in params:
                    cookie += v + ";"
    except Exception as e:
        str(e)

    return cookie

def getUseData(cookie):

    url = 'https://www.hjtnt.link/user'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
        #'path': '/user/checkin',
        #'scheme': 'https',
        #'method': 'POST',
        #'authority': 'www.hjtnt.link',
        #'accept': 'application/json, text/javascript, */*; q=0.01',
        #'accept-encoding': 'gzip, deflate, br',
        #'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        #,'cookie': 'uid=;\
        #           email=;\
        #           key=;\
        #           ip=;\
        #           expire_in=;'
    }
    headers['cookie'] = cookie
    
    try:
        response = doRequests('get', url, headers, '', '', False)
        if response != '':
            html = response.text
            m = html.find("trafficDountChat")+17 #start index
            if m < 17:
                return ""
            n = html[m:].find(")") #end index
            useData = html[m:m+n].replace('\n','').replace(' ','').replace('\'','').split(',')
            return "今日已用：{}\n剩余可用：{}\n累计已用：{}\n".format(useData[1],useData[2],useData[0])
    except Exception as e:
        print(str(e))

    return ""

def sign(cookie):
    
    log = ''
    
    url = 'https://www.hjtnt.link/user/checkin'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
        #'path': '/user/checkin',
        #'scheme': 'https',
        #'method': 'POST',
        #'authority': 'www.hjtnt.link',
        #'accept': 'application/json, text/javascript, */*; q=0.01',
        #'accept-encoding': 'gzip, deflate, br',
        #'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        #,'cookie': 'uid=;\
        #           email=;\
        #           key=;\
        #           ip=;\
        #           expire_in=;'
    }
    headers['cookie'] = cookie

    try:
        response = doRequests('post', url, headers, '', '', False)
        if response != '':
            log += json.dumps(json.loads(response.text), sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
            return log
    except Exception as e:
        str(e)

    return ""

def sendLog(context):

    from_addr = ''
    password = ''
    to_addr = 'm'
    smtp_server = ''

    msg = MIMEText(context, 'plain', 'utf-8')
    msg['From'] = Header('火箭TNT')
    msg['To'] = Header('')
    subject = '火箭TNT日志'+time.strftime("%Y-%m-%d %H:%M")
    msg['Subject'] = Header(subject, 'utf-8')
    try:
        smtpobj = smtplib.SMTP_SSL(smtp_server)
        smtpobj.connect(smtp_server, 465)    
        smtpobj.login(from_addr, password)   
        smtpobj.sendmail(from_addr, to_addr, msg.as_string()) 
        #print("邮件发送成功")
    except smtplib.SMTPException as e:
        #发送失败
        str(e)
    finally:
        # 关闭服务器
        smtpobj.quit()

def getProxies():

    url = "https://www.baidu.com" #例如百度

    count = 2
    while count:

        try:
            
            proxies = getIp()
            if proxies != "":
                
                response = doRequests('get', url, '', '', proxies, False)
                
                if response != "":
                    
                    return proxies
                
        except Exception as e:
            str(e)
        count -= 1

    return ""

def getIp():

    url = 'http://proxy.siyetian.com/'

    try:
        response = doRequests('get', url, '', '', '',False)
        ipport = response.text
        return { 'http':ipport, 'https':ipport }
    except Exception as e:
        str(e)

    return ""
    
def getMyIp(proxies):

    url = 'https://2023.ip138.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Content-Type': 'text/html; charset=utf-8'
    }
    
    try:
        response = doRequests('get', url, headers, '', proxies, False)
        if response != "":
            html = response.text
            m = html.find("<title>")+7 #start index
            n = html[m:].find("</title>") #end index
            useData = html[m:m+n]
            print(useData)
    except Exception as e:
        print(e)

