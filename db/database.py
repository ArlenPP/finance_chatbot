import pymysql
import inspect
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker


class StockDB(object):
    def __init__(self, host, port, user, password, db):
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset='utf8')
        self.cursor = self.db.cursor()
        
        # ORM
        self.engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, db))
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.day_ks = self.metadata.tables.get('day_ks')
        self.minute_ks = self.metadata.tables.get('minute_ks')
        self.trading_result = self.metadata.tables.get('trading_result')

    def exe_query(self, query):
        caller = inspect.stack()[1].function
        try:
            self.cursor.execute(query)
            #提交修改
            self.db.commit()
            result = self.cursor.fetchall()
            columns = self.cursor.description 
            columns = [v[0] for v in columns]
            df = pd.DataFrame(data=list(result), columns=columns) 
            df = df.set_index(pd.DatetimeIndex(df['Date']))
            return df
            print(caller + ' success')
        except pymysql.InternalError as error:
            #發生錯誤時停止執行SQL
            code, message = error.args
            self.db.rollback()
            print(caller + '\n\n' + str(code) + ' ' + message)

    def insert_data(self, df, table):
        df.to_sql(name=table, if_exists='append', index=False, con=self.engine)

    def read_data(self, start, end, isDay):
        
        if(True == isDay):
            table = self.day_ks
            date = self.day_ks.columns.Date
        else:
            table = self.minute_ks
            date = self.minute_ks.columns.Date

        session = self.Session()
        query = session.query(table).filter(date>=start, date<=end)
        df = pd.read_sql(query.statement, query.session.bind)
        df = df.set_index(pd.DatetimeIndex(df['Date']))
        session.close()
        return df
    
    def read_result(self, start, end, id):
        
        table = self.trading_result
        date = self.trading_result.columns.Date
        ts_id = self.trading_result.columns.TS_ID

        session = self.Session()
        query = session.query(table).filter(date>=start, date<=end, ts_id == id)
        df = pd.read_sql(query.statement, query.session.bind)
        df = df.set_index(pd.DatetimeIndex(df['Date']))
        session.close()
        return df

if __name__ == "__main__":

    mydb = StockDB(**db_config)
    # df = mydb.read_data("1991/1/10", "2019/03/21", False)
    # df = mydb.read_data("2019/01/1", "2019/1/30", "00:00", "14:00")
    # mydb.exe_query("delete from day_ks where Date=\"2019/3/21\"")
    # df = pd.read_csv("./product/fitx.csv")
    # mydb.insert_data(df, "day_ks")
    mydb.db.close()
