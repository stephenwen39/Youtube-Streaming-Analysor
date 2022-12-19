class get_streams_from_channel(object):
    def __init__(self, channel_url, limit=20):
        """
        channel_url: 頻道首頁連結
        limit: 想要抓的直播url數量，預設20
        """
        self.channel_url = channel_url
        # 下面排除尚未直播的影片url
        test = get_channel(channel_url=self.channel_url,
                           content_type='streams',
                           limit=limit)
        # 由於get_channel本身沒有跳過「尚未直播」的直播的功能，因此手動修改內部程式碼
        # get_channel經過修改，達到可以跳過「即將直播」的直播
        # change the code inside of get_channel, so that I can skip "coming soon" stream
        test_list = []
        for i in test:
            test_list.append(i['videoId'])
        # 排除完成
        self.videos = get_channel(channel_url=self.channel_url,
                     content_type='streams',
                     limit=limit + (limit - len(test_list)))
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
