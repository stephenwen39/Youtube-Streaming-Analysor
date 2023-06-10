import json
from google.colab import auth
from google.cloud import bigquery
from google.colab import data_table
import pandas as pd
from chat_downloader.sites import YouTubeChatDownloader
# 取得youtube streams id
session = YouTubeChatDownloader()
generator = session.get_user_videos ( channel_id = 'UC4J0GZLM55qrFh2L-ZAb2LA' , video_type = 'live' , params = None )
id_dict = {}
cnt = 0
while cnt < 100: # 檢查近期的一定數量的直播影片
    #print(next(generator)['video_type'])
    try:
        temp = next(generator)
        if temp['video_type'] == 'DEFAULT': # 如果直播正常且已結束
            id_dict[cnt] = str('https://www.youtube.com/watch?v=')+temp['video_id'] 
            cnt += 1
    except:
        break # 如果沒有generator到頭了或頻道本身沒有任何直播，就跳脫
# 查詢已經在資料表中的直播id
sql = """
SELECT 
    stream_id
FROM 
    `triple-voyage-377203.youtube_data.channels_and_streams`
WHERE
    channel_id = 'UC4J0GZLM55qrFh2L-ZAb2LA'
"""

# 執行查詢
query_job = client.query(sql)
old_df = query_job.to_dataframe() # 老的資料
new_streams = []
for index, value in enumerate(id_dict): # 查找剛剛找到的直播是否已經在表中
    if id_dict[index] not in old_df['stream_id'].values:
        new_streams.append(id_dict[index]) # 新的就記錄起來
 
#準備insert到GBQ表中
if len(new_streams) > 0:
    new_channels = ['UC4J0GZLM55qrFh2L-ZAb2LA' for i in range(0, len(new_streams))]
    new_df = pd.DataFrame({'channel_id': new_channels, 'stream_id': new_streams})

    data_dict = new_df.to_dict(orient='records')

    errors = client.insert_rows_json(
            table='triple-voyage-377203.youtube_data.channels_and_streams',
            json_rows=data_dict) # 將不符合表架構的row忽略
    if errors:
        print(f'Encountered errors while inserting rows: {errors}')
    else:
        print(f'Successfully inserted {len(data_dict)} rows.')
else:
    print('new stream not founded')
