class user_analysor(object):
    def __init__(self, df):
        self.df = df

    def main(self):
        # 計算發訊息數量
        df_temp_1 = self.message_counter()
        # 把使用者的訊息都集合成一個list
        df_temp_2 = self.message_lister()
        # 把使用者的時間都集合成一個list
        df_temp_3 = self.timelister()
        # 上述結果merge
        df_result_1 = df_temp_1.merge(df_temp_2, on='user_id', how='inner')
        df_result_2 = df_result_1.merge(df_temp_3, on='user_id', how='left')
        # 改message_x, message_y欄位名字
        df_result_2.rename(columns = {'message_x':'message_count', 'message_y':'message_list'}, inplace = True)
        # merge最後的其他不需計算的欄位
        self.df = self.df.drop_duplicates(['user_id'])
        df_result_2 = df_result_2.merge(self.df[['user_id', 'user_identity', 'identity_time', 'Verified_or_not']], on='user_id', how='left')
        return df_result_2

    def message_counter(self):
        return self.df.groupby(['user_id'])[['message']].count().reset_index()
    
    def message_lister(self):
        return self.df.groupby(['user_id'])['message'].apply(list).reset_index()

    def timelister(self):
        return self.df.groupby(['user_id'])['time'].apply(list).reset_index()

# 下面是測試code
a = user_analysor(df3_set)

df = a.main()
df.head(30)
