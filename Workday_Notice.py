# API
import requests
# 定時
import datetime
import schedule
import time
import os
# Mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 此處需填入 SMTP 資訊
sender_email = "sender_email@gmail.com" # 寄件者
recipient_email = "recipient_email@gmail.com" # 收件者
# 設定你的 Gmail 帳戶資訊
gmail_username = "You_Gmail_Account@gmail.com" # Gmail 帳號
gmail_password = "You_Google_App_Passwords" # Gmail 應用程式密碼
# 設定 Gmail SMTP 伺服器
smtp_server = "smtp.gmail.com"
smtp_port = 587
# 補班前幾日提醒(工作天)
days_to_check = 2

# 程式名稱
program_name, _ = os.path.splitext(os.path.basename(__file__))
# 運行提示
runTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"{runTime} >>> {program_name} 已開始運行")

# 今年日期數
def total_day(data):
    total_days = len(data)
    print(f"今年天數: {total_days}")

# 放假日資訊
def holiday(data):
    holiday_list = []
    holiday_week_list = []
    for item in data:
        if item["isHoliday"]:
            if item["week"] != "六" and item["week"] != "日":
                holiday_list.append(item["date"])
                holiday_week_list.append(item["week"])
    return holiday_list,holiday_week_list

# 補班日資訊
def no_holiday(data):
    no_holiday_list = []
    no_holiday_week_list = []
    for item in data:
        if not item["isHoliday"] and (item["week"] == "六" or item["week"] == "日"):
            no_holiday_list.append(item["date"])
            no_holiday_week_list.append(item["week"])
    return no_holiday_list,no_holiday_week_list

# 補班前兩天
def two_day(data):
    two_day_list = []
    for i in range(len(data)):
        if not data[i]["isHoliday"] and (data[i]["week"] == "六" or data[i]["week"] == "日"):
            count = 0
            for ii in range(i - 1, -1, -1):
                if (
                    not data[ii]["isHoliday"]
                    and data[ii]["week"] in ["一", "二", "三", "四", "五"]
                ):
                    if count == days_to_check - 1:
                        two_day_list.append(data[ii]["date"])
                        break  # 跳脫
                    else:
                        count += 1
    return two_day_list

# 寄信函式
def send_mail(content, html_template):
    # 今天的日期
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    message = MIMEMultipart()
    message['Subject'] = content[0]
    message['From'] = sender_email
    message['To'] = recipient_email

    # 將 HTML 內容中的 <HTML_CONTENT> 替換成實際的內容
    html_content = html_template.replace('<HTML_CONTENT>', content[1])
    # 將 HTML 內容加入郵件
    message.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(gmail_username, gmail_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print('')
        print(f"{today_date} - 完成: 郵件傳送成功.")
    except smtplib.SMTPException as e:
        print(f"{today_date} - 錯誤: 無法傳送郵件. {str(e)}")

# 主程序
def main():
    # 年度
    year_now = str(datetime.datetime.now().year)
    # API串接年度
    api_url_auto = f"https://cdn.jsdelivr.net/gh/ruyut/TaiwanCalendar/data/{year_now}.json"

    try:
        response = requests.get(api_url_auto)
        if response.status_code == 200:
            # API 帶入 data 變數
            data = response.json()
            # 獲取今日日期 
            now = datetime.datetime.now().strftime("%Y%m%d")
            # 獲取提醒日、補班日、補班日星期幾
            two_day_list = two_day(data)
            no_holiday_list = no_holiday(data)[0]
            no_holiday_week_list = no_holiday(data)[1]
            # 初始化
            Num = 0
            content = []
            # 今天如果是通知日就寄出 Mail
            for item in two_day_list:
                if (now == item):
                    print(f'今日為通知日: {now}')
                    # Mail 內容
                    content = [f'補班日提醒: {no_holiday_list[Num]}({no_holiday_week_list[Num]})需補班。', f'<HTML_CONTENT>', *content]
                    html_template = f"""
                    <!DOCTYPE html>
                    <html lang="zh-Hant-TW">
                    <head>
                        <title></title>
                        <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
                        <meta content="width=device-width, initial-scale=1.0" name="viewport">
                    </head>
                    <body>
                        <div class="container">{no_holiday_list[Num]}({no_holiday_week_list[Num]})需補班。</div>
                    </body>
                    </html>
                    """
                    # 調用寄信函式
                    send_mail(content, html_template)
                Num += 1
        else:
            print(f"錯誤: {response.status_code}")
    except :
        print('發生錯誤。')

# 每日早上 9:00 執行一次
schedule.every().day.at("09:00").do(main)
while True:
    schedule.run_pending()
    time.sleep(60)
