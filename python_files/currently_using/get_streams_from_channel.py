class get_streams_from_channel(object):
    def __init__(self, channel_id, limit=20):
        """
        channel_id: 頻道id連結，目前沒有簡單方法可以獲取channel id，請使用網頁開發者模式或此網站獲取https://commentpicker.com/youtube-channel-id.php
        limit: 想要抓的直播url數量，預設20，limit=0的話會回傳empty list
        """
        self.url_list = []
        self.channel_id = channel_id
        session = YouTubeChatDownloader()
        generater = session.get_user_videos (channel_id = self.channel_id, 
                                             video_type = 'live', 
                                             params = None )
        self.limit = limit
        self.buffer = []
        while len(self.buffer) < self.limit:
            element = next(generater)
            if element['video_type'] != 'DEFAULT':
                continue
            else:
                self.buffer.append(element['video_id'])
    def main(self):
        for i in self.buffer:
            self.url_list.append('https://www.youtube.com/watch?v=' + i)
        return self.url_list
'''
get_streams_from_channel(channel_id='UC4J0GZLM55qrFh2L-ZAb2LA',
                         limit=5).main()
'''
