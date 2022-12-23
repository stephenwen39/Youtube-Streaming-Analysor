class live_info(object):
    def __init__(self, df):
        self.df = df
    
    def main(self):
        # 截斷時間，01:01:50 -> 01:01:00，之後groupby會比較密集
        self.groupby_minutes()
        # 基於時間count使用者量
        df_temp_1 = self.user_counter()
        # 基於時間創造該分鐘數的留言使用者list
        df_temp_2 = self.user_lister()
        # 基於時間創造該分鐘數的留言list & message_cnt
        df_temp_3 = self.message_lister()
        print(df_temp_3['message'][1])
        df_temp_3['message_cnt'] = self.message_counter(df_temp_3)
        
        # merge by time
        df_temp_1 = df_temp_1.merge(df_temp_2, on='time', how='inner')
        df_temp_1 = df_temp_1.merge(df_temp_3, on='time', how='inner')
        # 補齊空白時間，之後畫圖比較好畫
        df_result = self.complete_blank_time(df_temp_1)
        # rename
        df_result.rename(columns = {'user_id_x':'user_cnt', 
                                    'user_id_y':'users_list',
                                    'message':'message_list'}, inplace = True)
        return df_result
    
    def groupby_minutes(self):
        def time_trunc(x):
            return str(x)[0:6]+'00'

        self.df['time'] = self.df.time.apply(time_trunc)
        self.df['time'] = pd.to_datetime(self.df['time'],format= '%H:%M:%S' ).dt.time

    def user_counter(self):
        return self.df.groupby(['time'])['user_id'].nunique().reset_index()

    def user_lister(self):
        return self.df.groupby(['time'])['user_id'].apply(list).reset_index()

    def message_lister(self):
        return self.df.groupby(['time'])['message'].apply(list).reset_index()

    def message_counter(self, df_temp_3):
        return df_temp_3.message.apply(lambda x: len(x))
    
    def complete_blank_time(self, df):
        '''填補空白時間段的方式是：
        1.確定最大時間 end_time，並且建立以分鐘為間隔的時間list
        2.跑for loop，如果該分鐘數沒有出現在df中，就在df最末端插入該分鐘數
        3.全部補齊後，根據分鐘數排序 ASC
        4.最後用reset_index跟drop index來重新設定索引，完成
        '''
        end_time = str(df.iloc[-1]['time'])[0:6]+'00'
        time_values = pd.date_range("00:00", end_time, freq="1min").time
        count = 0
        for i in df['time']:
            while time_values[count] < i:
                df.loc[-1] = [time_values[count], 0, [], [], 0] #
                count += 1
                df.index = df.index + 1
            count += 1
        df = df.sort_values(by='time')
        df = df.reset_index()
        return df.drop(['index'], axis=1)

# 下面是測試code
a = live_info(df) # df from message_analysor from Pre_processor_2.0.py
df2 = a.main()
df2.tail(10)
