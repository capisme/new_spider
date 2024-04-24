# _*_ coding : utf -8 _*_
# coding=gbk
# @Time : 2023/2/17 15:40
# @Author : Cap
# @File : send_email
# @Project : Project
import smtplib
import ssl
from email.message import EmailMessage

class Email:
    def send_email(self, num):
        # 使用 smtplib 模块发送纯文本邮件

        EMAIL_ADDRESS = "cxxxxx.com"  # 邮箱的地址
        EMAIL_PASSWORD = "xxxx"  # 授权码

        # 使用ssl模块的context加载系统允许的证书，在登录时进行验证
        context = ssl.create_default_context()

        # 建立一个列表来存储目标邮箱地址
        contacts = ['capht2021@163.com ', ]
        # 为了防止忘记关闭连接也可以使用with语句
        try:
            with smtplib.SMTP_SSL("smtp.163.com", 465, context=context) as smtp:  # 完成加密通讯
                # 连接成功后使用login方法登录自己的邮箱
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                for contact in contacts:
                    subject = "今日数据量"  # 邮件标题内容
                    body = str(num)
                    msg = EmailMessage()
                    msg['subject'] = subject  # 邮件标题
                    msg['From'] = EMAIL_ADDRESS  # 邮件发件人
                    msg['To'] = contact  # 邮件的收件人
                    msg.set_content(body)  # 使用set_content()方法设置邮件的主体内容
                    # 使用send_message方法发送邮件信息
                    smtp.send_message(msg)
                    print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("无法发送邮件", e)


if __name__ == '__main__':
    c = Email()
    c.send_email(121)
