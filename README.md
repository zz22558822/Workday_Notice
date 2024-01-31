# Workday_Notice
補班日提醒工具

補班日提醒工具，運行後每天偵測是否為補班日前的設定日期，並透過郵件通知使用者。

## 檔案說明
- **Workday_Notice.py**: 主程式
- **Run_Auto_Notice.sh**: Ubuntu 快捷運行腳本

## 使用前需安裝的庫
```安裝前的庫
python -m pip install --upgrade pip
pip install requests
pip install schedule
```

# 須設定基礎參數
```python
sender_email = "<YOUR_EMAIL>"  # 寄件者
recipient_email = "<RECIPIENT_EMAIL>"  # 收件者
gmail_username = "<YOUR_GMAIL_ACCOUNT>"  # Gmail 帳號
gmail_password = "<YOUR_GOOGLE_APP_PASSWORD>"  # Gmail 應用程式密碼
days_to_check = 2  # 補班前幾日提醒(工作天)
```

## Ubuntu 腳本運行前設定
在使用 Ubuntu 腳本前，確保已設定執行權限:
```Ubuntu
sudo chmod +x Run_Auto_Notice.sh
```

API 資料來源: [ruyut/TaiwanCalendar](https://github.com/ruyut/TaiwanCalendar)