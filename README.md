# Youtube Streaming Analysor

-------------------------------

This is a tool for analysis youtuber/vtuber streaming data
, focus on chat/user pairs data analysis.

currently only pre-process function now.

process of analysis below:
<p align="center"><img width="80%" src="analysisProcess.png" /></p>
(with brown pixelization on user name)

process data flow by split chracters.

<p align="center"><img width="80%" src="description.png" /></p>

Pre_processor_2.0.py output:
<p align="center"><img width="80%" src="v2_table.png" /></p>

user_analysor.py output:
<p align="center"><img width="80%" src="user_info_table.png" /></p>

reference:
https://github.com/xenova/chat-downloader

-------------------------------
TO DO: 
1. Clarify the problem of the ":" sign between name and message.

-------------------------------

TIME LINE

2022.12.15: 新增user_analysor.py檔案，功能是彙整該直播中的所有使用者資訊，另外之前沒考量的Verified身份也在這次更新中修正完成

2022.12.15: Upload user_analysor.py, I use it to summarize user information in a streaming live, also I fix the 'Verified' identity problem. In the original version, I didn't consider the 'Verified' identity.

2022.11.22: 更改data pipeline，從直接匯入df改成先以list承接再統一匯入df，此舉改善11/21版本近十倍的效能（使用同一支直播影片測試，總花費CPU time從366下降到30）。對比Pre_processor.py，此版本增進了40%左右的效能，並且具備更多欄位，能達成更多目的

2022.11.22: Fix the data pipeline, use list to store raw data instead of using df directly, and improve 10 times of efficiency compare with the version build in 11.21. This version is 40% more efficiency compare with Pre_processor.py.

2022.11.21: 完成2.0版本的初步內容，以Pre_processor_2.0.py為檔案名稱，捨棄list與dict的資料裝載方式，清洗後的資料全面改用pandas的dataframe裝載

2022.11.21: Finish the 2.0 version, use dataframe to store the data

2022.11.19: 計劃用pandas把pipeline重構成更有效率的處理方式

2022.11.19: TO DO: Use pandas package to refactor the data pipeline.

2022.10.16: 10.15提出的問題已修復

2022.10.16: Update: problem mention at 10.15 solved.

2022.10.15: 目前會有一個問題：如果使用者名稱中有New, Member等詞彙會造成判斷錯誤，修改中

2022.10.15: Currently problem: once there is "New" or "Member" in the user ID, error occour, fixing.
