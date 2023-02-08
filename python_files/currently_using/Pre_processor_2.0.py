# 12/16的內容
class message_analysor(object):
    def __init__(self, url):
        self.message_df = pd.DataFrame(columns=['raw_data'])
        
        self.url = url
        self.chat = ChatDownloader().get_chat(self.url)
        self.test = []
        for message in self.chat:                        # iterate over messages
            self.test.append(self.chat.format(message))
        self.message_df['raw_data'] = self.test
    
    def main(self):
        self.Time_processer()
        self.Identity_name_chat_processer()
        return self.message_df

    def Time_processer(self):
        def time_string_add(x):
            if x[-1] == ' ':
                x = x.split(' ', 1)[0]
            if len(x) == 4: # 1:21
                return '00:0'+x
            elif len(x) == 5: # 17:31
                return '00:'+x
            elif len(x) == 7: # 1:21:21
                return '0'+x
            else:
                return x
        # 解決時間正負號，階段4
        self.message_df['is_time_positive'] = \
        self.message_df.raw_data.apply(lambda x: False if x[0] == '-' else True)
        
        # 丟棄時間負號，階段5
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(lambda x: x if x[0] != '-' else x[1:])
        # 擷取小時、分鐘、秒數
        self.message_df['time'] = \
        self.message_df.raw_data.apply(lambda x: x.split('|')[0])
        # 補齊符合datetime的時間字串格式
        self.message_df['time'] = \
        self.message_df.time.apply(time_string_add)
        # 先轉換time成datetime才可以再轉換為time
        self.message_df['time'] = pd.to_datetime(self.message_df['time'])
        # 轉換datetime為time
        self.message_df['time'] = self.message_df.time.dt.time
        # 階段7
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(lambda x: x.split('|', 1)[1])

        return self
    
    def Identity_name_chat_processer(self):
        # 如果接下來[0]是'('表示他有一定的身份，為類別1，否則就是others，為類別2
        # 類別1的前三個字會透露他的身份，'Mod','Mem','Own','New'，所以分流處理
        # 分流使用def實作並交由apply套用處理
        # 分流確認身份後，再確認身份時間
        # 如果是other就直接給予other身份就好
        def Verified_filter(x):
            if x[2:5] == 'Ver':
                return True
            else:
                return False
        def Verified_deleter(x):
            if x[2:5] == 'Ver': #Verified
                if x[11] == ',':
                    ans = x.split(',', 1)[1]
                    ans = ans.split(' ', 1)[1]
                    return ' (' + ans
                else:
                    return x.split(')', 1)[1]
            return x
        def identity_filter(x):
            # 多考量一個verified, 只要帳號有勾勾就是有，跟會員與否無關
            # if 後面的 and是為了確保不會有user id長得像「(帽子)北海市長孔文舉」
            # 因為一般來說()裡面是要識別其身份
            if x[1] == '(' and x[2:5] in ('Mem', 'Mod', 'New', 'Own'):
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
            if x[1] == '(' and x[2:5] in ('Mem', 'Mod', 'New', 'Own'):
                if x[2:5] == 'Mem':
                    return x.split('(', 2)[2]
                elif x[2:5] == 'Mod': # 假設若多重身份Mod會在第一個
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
                try:
                    return x.split(' ', 1)[1] # name
                except:
                    print('error time_deleter:',x)
                    return x.split(' ', 1)[0] # name
            value = x.split(')', 2)
            return value[2]
        # 建立Verified身份
        self.message_df['Verified_or_not'] = \
        self.message_df.raw_data.apply(Verified_filter)
        # 移除Verified 在raw_data中的身份
        self.message_df['raw_data'] = \
        self.message_df.raw_data.apply(Verified_deleter)
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
        # 改成user_id
        self.message_df = self.message_df.rename({'raw_data': 'user_id'}, axis=1)
        
        return self

# 下面是示範code
url = 'https://www.youtube.com/watch?v=0m_Z8FSuBDQ'
a = message_analysor(url)

df = a.main()
df.tail(5)
