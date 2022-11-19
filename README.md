# Youtube Streaming Analysor

計劃用pandas把pipeline重構成更有效率的處理方式(11/19)

TO DO: Use pandas package to refactor the data pipeline.(11/19)

-------------------------------

目前會有一個問題：如果使用者名稱中有New, Member等詞彙會造成判斷錯誤，修改中(10/15)

更新：上述問題已修復(10/16)

Currently problem: once there is "New" or "Member" in the user ID, error occour, fixing. (10/15)

Update: problem solved.(10/16)

-------------------------------

This is a tool for analysis youtuber/vtuber streaming data
, focus on chat/user pairs data analysis.

currently only pre-process function now.

process of analysis below:
<p align="center"><img width="80%" src="analysisProcess.png" /></p>
(with brown pixelization on user name)

process data flow by split chracters.

<p align="center"><img width="80%" src="description.png" /></p>

reference:
https://github.com/xenova/chat-downloader
