# Use Pandas to speed up the process
class message_analysor(object):
    def __init__(self, url):
        self.message_df = pd.DataFrame(columns=['raw_data'])
        
        self.url = url
        self.chat = ChatDownloader().get_chat(self.url)
        for message in self.chat:   
            value = self.chat.format(message)
            self.message_df = self.message_df.append({'raw_data': value}, ignore_index=True)
    
    def main(self):
        self.Time_processer()
        self.Identity_name_chat_processer()
        return self.message_df
    
    def Time_processer(self):
        # 解決時間正負號
        self.message_df['is_time_positive'] = \
        self.message_df.raw_data.apply(lambda x: False if x[0] == '-' else True)
        
        # 丟棄時間負號
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(lambda x: x if x[0] != '-' else x[1:])
        
        # 解決時間
        self.message_df['time'] = \
        self.message_df.raw_data.apply(lambda x: x.split('|')[0])
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(lambda x: x.split('|', 1)[1])

        return self
    
    def Identity_name_chat_processer(self):
        # 如果接下來[0]是'('表示他有一定的身份，為類別1，否則就是others，為類別2
        # 類別1的前三個字會透露他的身份，'Mod','Mem','Own','New'，所以分流處理
        # 分流使用def實作並交由apply套用處理
        # 分流確認身份後，再確認身份時間
        # 如果是other就直接給予other身份就好
        def identity_filter(x):
            if x[1] == '(':
                if x[2:5] == 'Mem':
                    return 'Member'
                elif x[2:5] == 'Mod':
                    return 'Moderator'
                elif x[2:5] == 'New':
                    return 'New member'
                elif x[2:5] == 'Own':
                    return 'Owner'
                else:
                    return 'Unknow'
            else:
                return 'other'
        
        def identity_deleter(x):
            if x[1] == '(':
                if x[2:5] == 'Mem':
                    return x.split('(', 2)[2]
                elif x[2:5] == 'Mod':
                    if x[11] == ',':
                        return x.split('(', 2)[2]
                    return x.split('(', 1)[1]
                elif x[2:5] == 'New': # 只有單括號
                    return x.split(')', 1)[1]
                elif x[2:5] == 'Own':
                    return x.split('(', 1)[1]
                else:
                    value1 = x.split(')', 1) # 為了防止姓名或留言裡面有()
                    if len(value1[0].split('(', 3)) == 4: # 表有三個括號
                        value = x.split('(', 3) # 這是防呆機制
                        return value[3]
                    elif len(value1[0].split('(', 2)) == 3: # 表有兩個括號
                        value = x.split('(', 2)
                        return value[2]
                    else:
                        value = x.split('(', 1)
                        return value[1]
            else:
                return x # 不會有括號
        def time_name_filter(x):
            try:
                num = int(x[0])
            except:
                return '0' # x.split(' ', 1)[1] # name
            value = x.split(')', 2)
            return value[0]
        def time_deleter(x):
            try:
                num = int(x[0])
            except:
                return x.split(' ', 1)[1] # name
            value = x.split(')', 2)
            return value[2]
        # 建立身份欄位
        self.message_df['user_identity'] = \
        self.message_df.raw_data.apply(identity_filter)
        # 丟棄身份
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(identity_deleter)
        # 建立訊息欄位
        self.message_df['message'] = \
        self.message_df.raw_data.apply(lambda x: x.split(':', 1)[1])
        # 丟棄訊息欄位的第一個空白
        self.message_df['message'] = \
        self.message_df.message.apply(lambda x: x.split(' ', 1)[1])
        # 丟棄訊息
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(lambda x: x.split(':', 1)[0])
        # 建立身份時間欄位
        self.message_df['identity_time'] = \
        self.message_df.raw_data.apply(time_name_filter)
        # 丟棄身份時間
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(time_deleter)
        return self

# 下面是示範code
# Try the following code
url = 'https://www.youtube.com/watch?v=pQi2A8ndsYg&ab_channel=USAGIHIMECLUB.%E5%85%94%E5%A7%AC'
a = message_analysor(url)

df3 = a.main()
df3.head(30)
