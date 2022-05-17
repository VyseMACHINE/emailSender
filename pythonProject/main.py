import csv
import sys
import pymysql
import pandas as pd
import smtplib
import os
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from config import host, user, password, db_name
try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected")
    print("#" * 20)
    try:
        sql_query = pd.read_sql_query("SELECT * FROM `emg-cm`.wincc_tags;", connection)
        df = pd.DataFrame(sql_query)
        df.to_csv(r'data.csv', index=False, sep=';', encoding='ANSI', quoting=csv.QUOTE_ALL)

    finally:
        connection.close()
except Exception as ex:
    print("connection refused")
    print(ex)

def send_email():
        sender = "quqfall@gmail.com"
        receiver = "Razak.Karsa@gmail.com"
        password = "28180418"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        try:
            server.login(sender, password)
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = sender
            msg["Subject"] = "отправка файла"

            for file in os.listdir(r"C:\Users\User\PycharmProjects\pythonProject"):
                print(file)

            with open("data.csv") as f:

                file = MIMEText(f.read())
            filename = datetime.date.today().strftime('%d-%m-%Y.csv')
            file.add_header('content-disposition', 'attachment', filename=filename)
            msg.attach(file)
            server.sendmail(sender, receiver, msg.as_string())
            server.quit()

            return "The message was send successfully!"
        except Exception as _ex:
            return f"{_ex}\nCheck your login or password!"


def main():
    print(send_email())


if __name__ == '__main__':
     main()












