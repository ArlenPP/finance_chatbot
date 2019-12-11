# finance_chatbot
## FSM Diagram
![](https://i.imgur.com/PK55TOS.png)

## 開發理念
因為每次要看最近的期貨走勢都還要到網路上去找，又或者想看最近預測模型交易的累積報酬率，都還要打開其他程式感覺很麻煩，所以才會想說藉由Line，使用聊天機器人，快速幫我們找到想要的資訊，並用圖片呈現給我們看。此外也想要透過Line來告知我們，當自動化交易程式出錯的時候。

## 功能介紹
1.以圖表呈現台指期在指定時間內的走勢，或交易模型的報酬率
2.每天晚上8點推播告知使用者明天期貨機器人的預測結果
3.每天自動化爬蟲會到期交所爬近30日內的期貨tick資料，成功完成後會告知使用者
4.監測自動化交易程式，當停損停利或建倉成功時以及有任何異常交易都會發訊息告知使用者

## Prerequisite
Python 3.6
Line開發者帳號
HTTPS Server

## Usage
1. 申請SSL
2.  
```
$ pip install -r requirement.txt
```
3.
```
python app.py
```
4. 設定Line webhook