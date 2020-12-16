# create by: wangyun
# create at: 2020/4/25 18:43
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config_path import report_path, details_path, report_pdf_path


def send_email(report_no):
    """
    发送邮件，包括html结果作为内容，以及excel详细结果作为附件
    :param report_no: 报告号
    """
    # 设置登录及服务器信息
    mail_host = 'smtp.sina.cn'
    mail_user = 'xxx@sina.cn'
    mail_pass = 'xxx'
    sender = 'xxx@sina.cn'
    receivers = ['xxx@xxx.cn']

    # 设置eamil信息
    # 添加一个MIMEmultipart类，处理正文及附件
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = '【自动化结果报告】' + report_no

    # 发送html
    report_file = ''
    date_path = os.path.join(report_path, report_no[:8])
    for i in os.listdir(date_path):
        if report_no in i:
            report_file = i
    report_file_path = os.path.join(date_path, report_file)
    with open(report_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        f.close()
    # 设置html格式参数
    part1 = MIMEText(content, 'html', 'utf-8')
    # 将内容附加到邮件主体中
    message.attach(part1)

    # 发送附件
    details_file = ''
    cur_date_path = os.path.join(details_path, report_no[:8])
    for i in os.listdir(cur_date_path):
        if report_no in i:
            details_file = i
    details_file_path = os.path.join(cur_date_path, details_file)
    with open(details_file_path, 'rb') as df:
        f = df.read()
        df.close()
    part2 = MIMEApplication(f)
    part2.add_header('Content-Disposition', 'attachment', filename=details_file)
    message.attach(part2)

    # 登录并发送
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)

        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('send email success.')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('send email error.', e)


def send_email2(report_no):
    """
    发送邮件，包括html转换图片的结果作为内容，以及excel详细结果作为附件
    :param report_no: 报告号
    """
    # 设置登录及服务器信息
    mail_host = 'smtp.sina.cn'
    mail_user = 'xxx@sina.cn'
    mail_pass = 'xxx'
    sender = 'xxx@sina.cn'
    receivers = ['xxx@xxx.cn']

    # 设置eamil信息
    # 添加一个MIMEmultipart类，处理正文及附件
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = '【自动化结果报告】' + report_no

    # # 发送图片
    # img_file = get_report_no_file(report_no, report_pdf_path)
    # img_part = MIMEApplication(open(img_file, 'rb').read())
    # img_part.add_header('Content-Disposition', 'attachment', filename=img_file)
    # message.attach(img_part)

    # 发送附件
    details_file = ''
    cur_date_path = os.path.join(details_path, report_no[:8])
    for i in os.listdir(cur_date_path):
        if report_no in i:
            details_file = i
    details_file_path = os.path.join(cur_date_path, details_file)
    with open(details_file_path, 'rb') as df:
        f = df.read()
        df.close()
    part2 = MIMEApplication(f)
    part2.add_header('Content-Disposition', 'attachment', filename=details_file)
    message.attach(part2)

    # 发送附件2
    report_pdf_file = ''
    report_date_path = os.path.join(report_pdf_path, report_no[:8])
    for i in os.listdir(report_date_path):
        if report_no in i:
            report_pdf_file = i
    report_pdf_file_path = os.path.join(report_date_path, report_pdf_file)
    with open(report_pdf_file_path, 'rb') as df:
        f = df.read()
        df.close()
    part3 = MIMEApplication(f)
    part3.add_header('Content-Disposition', 'attachment', filename=report_pdf_file)
    message.attach(part3)

    # 登录并发送
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)

        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('send email success.')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('send email error.', e)


if __name__ == '__main__':
    send_email2('20200502173942')
