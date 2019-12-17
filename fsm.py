# from transitions.extensions import GraphMachine
import os
from transitions import Machine
import re
from utils import send_message, check_date_format, querl_sql, plot_kbar, plot_roi
from linebot.models import *
from datetime import datetime
from imgurpython import ImgurClient
import pandas as pd

# for imgur
CLIENT_ID = os.environ.get('imgur_client_id')
CLIENT_SECRET = os.environ.get('imgur_client_secret')

fig_path = './temp/temp.png'

user_strategy_num = {}

class TocMachine(Machine):
    def __init__(self, id=None, **machine_configs):
        self.machine = Machine(model=self, **machine_configs)
        self.id = id
    
    def on_enter_init(self, event):
        content = '基本功能：'
        content += '\n1.請先選擇你想知道的訊息，如果想知道台指期走勢請輸入期貨或future，如果想知道期貨機器人的交易表現請輸入策略或strategy\n'
        content += '\nVIP功能：'
        content += '\n1.每天晚上8點推播告知使用者明天期貨機器人的預測結果'
        content += '\n2.每天自動化爬蟲會到期交所爬近30日內的期貨tick資料，成功完成後會告知使用者'
        content += '\n3.監測自動化交易程式，當停損停利或建倉成功時以及有任何異常交易都會發訊息告知使用者'
        send_message(event, TextSendMessage(text=content))
    
    def is_go_to_future(self, event):
        text=(event.message.text).lower()
        return 0 == (text.find('future') and  text.find('期貨'))

    def is_go_to_strategy(self, event):
        text=(event.message.text).lower()
        return 0 == (text.find('strategy') and  text.find('策略'))

    def on_enter_future(self, event):
        content = '請輸入想查詢的日期區段ex:2019/11/11~2019/11/29'
        send_message(event, TextSendMessage(text=content))

    def is_go_to_future_date(self, event):
        text=event.message.text
        split_date = text.split('~')
        if(len(split_date) != 2):
            content = '輸入日期格式錯誤請再確認'
            send_message(event, TextSendMessage(text=content))
            return False
        else:
            start = split_date[0]
            end = split_date[1]
            if (check_date_format(start)[0] and check_date_format(end)[0]):
                return True
            else:
                content = '輸入日期格式錯誤請再確認'
                send_message(event, TextSendMessage(text=content))
                return False

    def on_enter_future_date(self, event):
        text=event.message.text
        split_date = text.split('~')
        start = check_date_format(split_date[0])[1]
        end = check_date_format(split_date[1])[1]
        s = start[4]
        start = datetime.strptime(start, f'%Y{s}%m{s}%d')
        end = datetime.strptime(end, f'%Y{s}%m{s}%d')
        if (end - start).days < 5:
            df = querl_sql(start, end, False)
            isday = False
        else:
            df = querl_sql(start, end, True)
            isday = True
        if df.empty:
            content = '查無資料請重新輸入'
            send_message(event, TextSendMessage(text=content))
            self.go_back_future(event)
        else:
            # plot
            plot_kbar(df, True, fig_path, isday)
            # -- upload
            # imgur with account: your.mail@gmail.com

            client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
            print("Uploading image... ")
            image = client.upload_from_path(fig_path, anon=True)
            print("Done")

            url = image['link']
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            send_message(event, image_message)
            print('查詢結束回到初始狀態')
            self.go_init(event)

    def on_enter_strategy(self, event):
        content = '請輸入要查詢的策略代碼1~3'
        content += '\n1: 固定停損交易策略, 停利點60, 停損點20'
        content += '\n2: 固定停損交易策略, 停利點50, 停損點30'
        content += '\n3: 動態停利交易策略, 停利點60, 停損點20'
        send_message(event, TextSendMessage(text=content))
    
    def is_go_to_strategy_num(self, event):
        # test num 1~3
        text=event.message.text
        if(len(text) != 1):
            content = '輸入策略代碼錯誤請重新輸入'
            send_message(event, TextSendMessage(text=content))
            return False
        else:
            num = int(text)
            if (num<=3 and num>=1):
                user_strategy_num[event.source.user_id] = num
                return True
            else:
                content = '輸入策略代碼錯誤請重新輸入'
                send_message(event, TextSendMessage(text=content))
                return False

    def on_enter_strategy_num(self, event):
        content = '請輸入想查詢的日期區段ex:2019/11/11~2019/11/29'
        send_message(event, TextSendMessage(text=content))
        
    def is_go_to_strategy_date(self, event):
        text=event.message.text
        split_date = text.split('~')
        if(len(split_date) != 2):
            content = '輸入日期格式錯誤請再確認'
            send_message(event, TextSendMessage(text=content))
            return False
        else:
            start = split_date[0]
            end = split_date[1]
            if (check_date_format(start)[0] and check_date_format(end)[0]):
                return True
            else:
                content = '輸入日期格式錯誤請再確認'
                send_message(event, TextSendMessage(text=content))
                return False

    def on_enter_strategy_date(self, event):
        text=event.message.text
        split_date = text.split('~')
        start = check_date_format(split_date[0])[1]
        end = check_date_format(split_date[1])[1]
        s = start[4]
        start = datetime.strptime(start, f'%Y{s}%m{s}%d')
        end = datetime.strptime(end, f'%Y{s}%m{s}%d')
        num = user_strategy_num[event.source.user_id]
        df = pd.read_pickle(f'./strategy/strategy_{num}.pkl')
        df = df[(df.Date>=start) & (df.Date<=end)]
        df['ROI'] -= df['ROI'][0]
        if df.empty:
            content = '查無資料請重新輸入'
            send_message(event, TextSendMessage(text=content))
            self.go_back_future(event)
        else:
            # plot
            plot_roi(df, True, fig_path)
            # -- upload
            # imgur with account: your.mail@gmail.com

            client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
            print("Uploading image... ")
            image = client.upload_from_path(fig_path, anon=True)
            print("Done")

            url = image['link']
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            send_message(event, image_message)
            print('查詢結束回到初始狀態')
            self.go_init(event)
    # def on_exit_state2(self):
    #     print("Leaving state2")