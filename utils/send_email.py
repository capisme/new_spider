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
        # ʹ�� smtplib ģ�鷢�ʹ��ı��ʼ�

        EMAIL_ADDRESS = "cxxxxx.com"  # ����ĵ�ַ
        EMAIL_PASSWORD = "xxxx"  # ��Ȩ��

        # ʹ��sslģ���context����ϵͳ�����֤�飬�ڵ�¼ʱ������֤
        context = ssl.create_default_context()

        # ����һ���б����洢Ŀ�������ַ
        contacts = ['capht2021@163.com ', ]
        # Ϊ�˷�ֹ���ǹر�����Ҳ����ʹ��with���
        try:
            with smtplib.SMTP_SSL("smtp.163.com", 465, context=context) as smtp:  # ��ɼ���ͨѶ
                # ���ӳɹ���ʹ��login������¼�Լ�������
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                for contact in contacts:
                    subject = "����������"  # �ʼ���������
                    body = str(num)
                    msg = EmailMessage()
                    msg['subject'] = subject  # �ʼ�����
                    msg['From'] = EMAIL_ADDRESS  # �ʼ�������
                    msg['To'] = contact  # �ʼ����ռ���
                    msg.set_content(body)  # ʹ��set_content()���������ʼ�����������
                    # ʹ��send_message���������ʼ���Ϣ
                    smtp.send_message(msg)
                    print("�ʼ����ͳɹ�")
        except smtplib.SMTPException as e:
            print("�޷������ʼ�", e)


if __name__ == '__main__':
    c = Email()
    c.send_email(121)
