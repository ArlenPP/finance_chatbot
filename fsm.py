# from transitions.extensions import GraphMachine
import os
from transitions import Machine
import re
from utils import send_message, check_date_format, querl_sql, plot_kbar
from linebot.models import *
from datetime import datetime
from imgurpython import ImgurClient

# for imgur
CLIENT_ID = os.environ.get('imgur_client_id')
CLIENT_SECRET = os.environ.get('imgur_client_secret')

fig_path = './temp/temp.png'


class TocMachine(Machine):
    def __init__(self, id=None, **machine_configs):
        self.machine = Machine(model=self, **machine_configs)
        self.id = id
    
    def on_enter_init(self, event):
        print("在初始狀態")
    
    def is_go_to_future(self, event):
        text=event.message.text
        return 0 == (text.find('future') and  text.find('期貨'))

    def is_go_to_strategy(self, event):
        text=event.message.text
        return 0 == (text.find('strategy') and  text.find('策略'))

    def on_enter_future(self, event):
        content = '請輸入想查詢的日期區段ex:2019/11/11~2019/11/29'
        msg = TextSendMessage(text=content)
        send_message(event, msg)

    def is_go_to_future_date(self, event):
        text=event.message.text
        split_date = text.split('s')
        start = split_date[0]
        end = split_date[1]
        if (check_date_format(start)[0] and check_date_format(end)[0]):
            return True
        else:
            print('輸入日期格式錯誤請再確認')
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
            print('查無資料請重新輸入')
            self.go_back_future(event)
        else:
            # plot
            plot_kbar(df, False, fig_path, isday)
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
        content = '請輸入要查詢的策略代碼'
        #! show 策略代碼所代表的意義
        print(content)
    
    def is_go_to_strategy_num(self, event):
        #! test num 1~5
        text=int(event)
        if (text<=5 and text>=1):
            return True
        else:
            print('輸入策略代碼錯誤請重新輸入')
            return False

    def on_enter_strategy_num(self, event):
        print(date_message)
        
    def is_go_to_strategy_date(self, event):
        date=event
        # if check_date_format(date):
        if (date=='True'):
            return True
        else:
            print('輸入日期格式錯誤請再確認')
            return False

    def on_enter_strategy_date(self, event):
        print("I'm entering strategy_date")
        # 如果沒有這個資料要回到future
        # reply_token = event.reply_token
        # send_text_message(reply_token, "Trigger state2")
        error = input()
        if error=='True':
            print('查無資料請重新輸入')
            self.go_back_strategy_num(event)
        else:
            print('查詢結束回到初始狀態')
            self.go_init(event)
    # def on_exit_state2(self):
    #     print("Leaving state2")