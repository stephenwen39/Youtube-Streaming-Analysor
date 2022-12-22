class compare_different_live(object):
    def __init__(self, url_list):
        # 因為之後可能會進行跨直播主的比較，用dict比較好改變key name來辨識直播主
        self.url_list = url_list
        self.url_dict = dict(zip([i for i in range(0, len(self.url_list))], self.url_list))
        self.result_dict = {}
        
    def main_analysis(self):
        for i in self.url_dict:
            print('url', i, 'processing...')
            basic_df = message_analysor(self.url_dict[i]).main()
            user_df = user_analysor(basic_df).main()
            live_time_line_df = live_info(basic_df).main()
            self.result_dict[i] = {'basic_df': basic_df,
                                   'user_df': user_df,
                                   'live_time_line_df': live_time_line_df}
        return self.result_dict

    def user_message_data_merge(self):
        '''
        This function provide user's messages count from different live
        remember to run main_analysis() first
        '''
        # 建立基本資料集，下面的for loop再插入其他資料集
        # 'user_identity', 'identity_time'
        user_df = self.result_dict[0]['user_df'][['user_id', 
                                                  'message_count', 
                                                  'user_identity', 
                                                  'identity_time']]
        user_df.insert(4, "from", [0] * len(user_df), True)
        for i in self.result_dict:
            if i != 0:
                df = self.result_dict[i]['user_df'][['user_id', 
                                                     'message_count', 
                                                     'user_identity', 
                                                     'identity_time']]
                df.insert(4, "from", [i] * len(df), True)
                user_df = user_df.append(df)
        # 最後的資料清理，一般來說不會用到
        user_df = user_df.fillna(0)
        # 使用user id排序
        user_df = user_df.sort_values(by='user_id')
        user_df = user_df.reset_index()
        user_df = user_df.drop(user_df.columns[0], axis=1)
        return user_df

    def user_identity_info(self, user_df):
        user_df = user_df.drop_duplicates(['user_id'])
        user_identity_df = user_df.groupby(['user_identity', 'from'])\
        ['user_id'].count().reset_index()
        user_identity_df.rename(columns = {'user_id':'user_cnt'}, inplace = True)
        user_identity_df = user_identity_df.sort_values(by=['from', 'user_identity'])
        # 整理index
        user_identity_df = user_identity_df.reset_index()
        user_identity_df = user_identity_df.drop(user_identity_df.columns[0],axis=1)
        return user_identity_df

    def user_participation_rate(self, user_df):
        '''每個「至少參與1次的觀眾」的近limit場直播中，參加的比率
        比如limit=5，至少參與1次的觀眾數量為100，rate就是這100名觀眾中，平均每人參與5場中的幾場
        '''
        user_df = user_df.groupby(['user_id'])['from'].count().reset_index()
        user_df.rename(columns = {'from':'participation_cnt'}, inplace = True)
        rate = user_df.participation_cnt.sum() / (len(self.url_list) * len(user_df))
        return (user_df, rate)
'''
# 下面是示範code
url_list = ['https://www.youtube.com/watch?v=0m_Z8FSuBDQ',
            'https://www.youtube.com/watch?v=3L5sbxIGmAg&t=1s',
            'https://www.youtube.com/watch?v=T6yGWzUA29o']
ans = compare_different_live(url_list).main_analysis()
# call df of url #0: ans[0]['user_df']
'''
