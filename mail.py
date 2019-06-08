# -*- coding: UTF-8 -*-
import traceback
from email.header import Header
from email.mime.text import MIMEText
import smtplib

sender = 'zhangzongqian32@gmail.com'
receiver = '1650658858@qq.com'
def send_mail(subject = None,contents=None,password = None):
    #主题
    """**主题如果是纯中文或纯英文则字符数必须大于等于5个，
    不然会报错554 SPM被认为是垃圾邮件或者病毒** """
    if not subject:
        subject = '不好，出错啦！'
    #内容
    if not contents:
        contents='测试'
    #服务器地址
    smtpserver = 'smtp.gmail.com'
    #用户名（不是邮箱）
    username = '提醒'
    #163授权码

    msg = MIMEText(contents, 'plain', 'utf-8')  # 中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = username
    msg['To'] = receiver
    #服务器地址和端口25
    smtp = smtplib.SMTP(smtpserver,587)
    #smtp.set_debuglevel(1)
    smtp.starttls()
    try:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        smtp.quit()
        print('发送邮件成功')
    except:
        traceback.print_exc()

