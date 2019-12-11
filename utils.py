import os

import re
from linebot import LineBotApi
from db.database import StockDB
from db.db_config import db_config
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf

db = StockDB(**db_config)

CHANNEL_TOKEN = os.environ.get('Line_ChatBot_Token_Futures')
line_bot_api = LineBotApi(CHANNEL_TOKEN)


def send_message(event, msg):
    line_bot_api.reply_message(event.reply_token, msg)

    return "OK"

def check_date_format(text):
    filtter = r'[\d]{4}(.)([1-9]|0[1-9]|1[0-2])(.)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])'
    match = re.search(filtter, text)
    if not match:
        return False, None
    else:
        return True, match.group()

def querl_sql(start_date, end_date, isDay=True):
    return db.read_data(start_date, end_date, isDay)

def upload_img():
    pass

def plot_candlestick(ax, data):
    ax.set_xticks(range(0, len(data['Time']), 30))
    ax.set_xticklabels(data['Time'][::30], rotation=45)
    mpf.candlestick2_ochl(ax, data['Open'], data['Close'], data['High'], data['Low'],width=1, colorup='r', colordown='green',alpha=0.6)
    ax.grid()
    ax.set_ylabel('Price', size=20)

def plot_candlestick_by_date(ax, data):
    ax.set_xticks(range(0, len(data['Date']), 30))
    ax.set_xticklabels(data['Date'][::30], rotation=45)
    mpf.candlestick2_ochl(ax, data['Open'], data['Close'], data['High'], data['Low'],width=1, colorup='r', colordown='green',alpha=0.6)
    ax.grid()
    ax.set_ylabel('Price', size=20)

def plot_kbar(data, plot=True, path=None, isday=False):
    fig = plt.figure(figsize=(13,10))
    ax = fig.add_subplot(1, 1, 1)
    if not isday:
        plot_candlestick(ax, data)
    else:
        plot_candlestick_by_date(ax, data)
    if(not plot): plt.close()
    if(path): 
        plt.savefig(path)
        plt.close()
    return fig