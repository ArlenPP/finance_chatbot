# from transitions.extensions import GraphMachine
from transitions import Machine
import re
# from utils import send_text_message


date_message='請輸入想查詢的日期區段ex:2019/11/11~2019/11/29'

def check_date_format(date):
    pass

def querl_sql(table, start_date, end_date):
    pass

class TocMachine(Machine):
    def __init__(self, id=None, **machine_configs):
        self.machine = Machine(model=self, **machine_configs)
        self.id = id
    
    def on_enter_init(self, event):
        print("在初始狀態")
    
    def is_go_to_future(self, event):
        # text=event.message.text
        text = event
        return 0 == (text.find('future') and  text.find('期貨'))

    def is_go_to_strategy(self, event):
        # text=event.message.text
        text = event
        return 0 == (text.find('strategy') and  text.find('策略'))

    def on_enter_future(self, event):
        content = date_message
        print(content)

    def is_go_to_future_date(self, event):
        date=event
        # if check_date_format(date):
        if (date=='True'):
            return True
        else:
            print('輸入日期格式錯誤請再確認')
            return False

    def on_enter_future_date(self, event):
        print("I'm entering future_date")
        # 如果沒有這個資料要回到future
        # reply_token = event.reply_token
        # send_text_message(reply_token, "Trigger state2")
        error = input()
        if error=='True':
            print('查無資料請重新輸入')
            self.go_back_future(event)
        else:
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