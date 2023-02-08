class get_streams_from_channel(object):
    def __init__(self, channel_url, limit=20):
        """
        channel_url: 頻道首頁連結
        limit: 想要抓的直播url數量，預設20
        """
        self.channel_url = channel_url
        # 下面排除尚未直播的影片url
        test_limit = 5 # test_limit先抓5部近期直播，看下方test會回傳多少直播
        test_list = [] # test_list儲存回傳直播數量，回傳如果只有3，表示有2部尚未開始的直播
        while len(test_list) == 0: 
            test = get_channel(channel_url=self.channel_url,
                            content_type='streams',
                            limit=test_limit)
            # 由於get_channel本身沒有跳過「尚未直播」的直播的功能，因此手動修改內部程式碼
            # get_channel經過我自己的修改，達到可以跳過「即將直播」的直播
            # change the code inside of get_channel, so that I can skip "coming soon" stream
            for i in test:
                test_list.append(i['videoId'])
            test_limit += 1 # 如果尚未開始的直播超過5部，就再+1探索真實數量
        # 下面的(test_limit - len(test_list))就是尚未開始的直播數量，要加到limit上
        real_limit = limit + (test_limit - len(test_list) - 1)
        # 排除完成
        self.videos = get_channel(channel_url=self.channel_url,
                     content_type='streams',
                     limit=real_limit)
        self.url_list = []
    
    def main(self):
        for i in self.videos:
            self.url_list.append('https://www.youtube.com/watch?v=' + i['videoId'])
        return self.url_list
'''
# 下面是示範code
get_streams_from_channel(channel_url='https://www.youtube.com/@nyoro0606tw',
                         limit=5).main()
# 會return近五個已經直播的url
'''
