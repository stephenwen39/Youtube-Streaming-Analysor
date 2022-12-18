class compare_different_live(object):
    def __init__(self, url_list):
        # 因為之後可能會進行跨直播主的比較，用dict比較好改變key name來辨識直播主
        self.url_dict = dict(zip([i for i in range(0, len(url_list))], url_list))
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

# 下面是示範code，包含visualization功能

url_list = ['https://www.youtube.com/watch?v=0m_Z8FSuBDQ',
            'https://www.youtube.com/watch?v=3L5sbxIGmAg&t=1s',
            'https://www.youtube.com/watch?v=T6yGWzUA29o']
ans = compare_different_live(url_list).main_analysis()
# call df of url #0: ans[0]['user_df']
# 接下來準備視覺化df
temp_user_df = ans[0]['user_df'][['user_id', 'message_count']]
temp_user_df.insert(2, "from", [0] * len(temp_user_df), True)
for i in ans:
    if i != 0:
        df = ans[i]['user_df'][['user_id', 'message_count']]
        df.insert(2, "from", [i] * len(df), True)
        temp_user_df = temp_user_df.append(df)
        # temp_user_df = temp_user_df.merge(ans[i]['user_df'][['user_id', 'message_count']], on='user_id', how='outer')
        # temp_user_df['message_count'] = temp_user_df['message_count_x'] + temp_user_df['message_count_y']
temp_user_df = temp_user_df.fillna(0)
temp_user_df = temp_user_df.sort_values(by='user_id')
temp_user_df.head()

import altair as alt
from vega_datasets import data

source = temp_user_df

alt.Chart(source).mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
).encode(
    x=alt.X('user_id',sort="-y",axis=alt.Axis(labelAngle=-45)),
    y='sum(message_count)',
    color='from'
).interactive()
