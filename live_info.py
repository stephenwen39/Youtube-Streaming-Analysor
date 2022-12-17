class live_info(object):
    def __init__(self, df):
        self.df = df
    
    def main(self):
        # 截斷時間，01:01:50 -> 01:01:00，之後groupby會比較密集
        self.groupby_minutes()
        # 基於時間count訊息量
        df_temp_1 = self.message_counter()
        # 基於時間創造該分鐘數的留言使用者list
        df_temp_2 = self.user_lister()
        # 基於時間創造該分鐘數的留言list
        df_temp_3 = self.message_lister()
        # merge by time
        df_temp_1 = df_temp_1.merge(df_temp_2, on='time', how='inner')
        df_temp_1 = df_temp_1.merge(df_temp_3, on='time', how='inner')
        # 補齊空白時間，之後畫圖比較好畫
        df_result = self.complete_blank_time(df_temp_1)
        return df_result
    
    def groupby_minutes(self):
        def time_trunc(x):
            return str(x)[0:6]+'00'

        self.df['time'] = df.time.apply(time_trunc)
        self.df['time'] = pd.to_datetime(self.df['time'],format= '%H:%M:%S' ).dt.time

    def message_counter(self):
        return self.df.groupby(['time'])['user_id'].count().reset_index()

    def user_lister(self):
        return self.df.groupby(['time'])['user_id'].apply(list).reset_index()

    def message_lister(self):
        return self.df.groupby(['time'])['message'].apply(list).reset_index()
    
    def complete_blank_time(self, df):
        end_time = str(df.iloc[-1]['time'])[0:6]+'00'
        time_values = pd.date_range("00:00", end_time, freq="1min").time
        count = 0
        for i in df['time']:
            while time_values[count] < i:
                df.loc[-1] = [time_values[count], 0, [], []]
                count += 1
                df.index = df.index + 1
            count += 1
        df = df.sort_values(by='time')
        df = df.reset_index()
        return df.drop(['index'], axis=1)

# 下面是測試code
a = live_info(df) # df from message_analysor from Pre_processor_2.0.py
df2 = a.main()
df2.head()
