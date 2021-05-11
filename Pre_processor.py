from chat_downloader import ChatDownloader

class analysor(object):

  def __init__(self, url):
    self.pre = [] #在直播之前的留言
    self.post = [] #在直播開始之後的留言
    self.time = [] #把留言的分鐘數push進去
    self.time_sum = [] #計算每分鐘有多少留言
    self.name = [] #推入名稱
    self.chat = [] #推入留言
    self.name_chat = {} #名稱留言字典

    self.url = url
    chat = ChatDownloader().get_chat(self.url)       # create a generator
    self.test = []
    for message in chat:                        # iterate over messages
        self.test.append(chat.format(message))

  def main(self):

    for i, value in enumerate(self.test):

      if value[0] is '-':
        self.pre.append(value)
        #test_line = test[i].split('|')
        

      else: #不存在負號

        self.post.append(value)
        test_line = value.split('|') #分割時間與其他資料
        self.time.append(self.Time_processor(test_line[0]))

        if 'Member' in test_line[1]:#辨識成員與否
          #是成員
          self.Name_Chat_processor(test_line[1], '))')

        elif 'New' in test_line[1]:
          #是新成員
          if "Moderator" in test_line[1]:
            self.Name_Chat_processor(test_line[1], '))')
          else:
            self.Name_Chat_processor(test_line[1], ')')
        else:
          #非成員
          if 'Moderator' in test_line[1]:
            self.Name_Chat_processor(test_line[1], ')')
          else:
            self.Name_Chat_processor(test_line[1], '0')
    return self

  def Name_Chat_processor(self, test_line, signal):
    if signal is ')': #新成員且不是管理員
      test_brac = test_line.split(')')
      test_name_chat = test_brac[1].split(':') #test_name_chat 0號是名稱, 1號是留言
      self.name.append(test_name_chat[0])
      self.chat.append(test_name_chat[1])
      self.Chat_dictionary(test_name_chat[0], test_name_chat[1])

    if signal is '))': #老成員，不一定非管理員
      test_brac = test_line.split(')')
      test_name_chat = test_brac[1].split(':') #test_name_chat 0號是名稱, 1號是留言
      self.name.append(test_name_chat[0])
      self.chat.append(test_name_chat[1])
      self.Chat_dictionary(test_name_chat[0], test_name_chat[1])

    if signal is '0': #不是成員
      test_name_chat = test_line.split(':') #test_name_chat 0號是名稱, 1號是留言
      self.name.append(test_name_chat[0])
      self.chat.append(test_name_chat[1])
      self.Chat_dictionary(test_name_chat[0], test_name_chat[1])
    
    return self

  def Time_processor(self, time_ori):
    time_split = time_ori.split(':')
    if len(time_split) is 3:
      return int(time_split[0]) * 60 + int(time_split[1])
    elif len(time_split) is 2:
      return int(time_split[0])

  def Chat_dictionary(self, temp_name, temp_chat):
    #使用字典把每個人的留言數量跟留言都記錄下來
    if temp_name in self.name_chat.keys():
      self.name_chat[temp_name].append(temp_chat)
    else:
      self.name_chat[temp_name] = []
      self.name_chat[temp_name].append(temp_chat)
    return self
  
  def Time_counter(self):
    counter = 0
    while self.time:
      number = self.time.count(counter)
      self.time_sum.append(number)
      for i in range(0,number):
        self.time.remove(counter)
      counter += 1
    return self.time_sum

  def name_printer(self):
    return self.name

  def chat_printer(self):
    return self.chat
  
  def time_printer(self):
    return self.time
  
  def name_chat_printer(self):
    return self.name_chat
  
  
'''
TEST HERE
doo = analysor('https://www.youtube.com/watch?v=-T9LBEwUnho')
doo.main()
doo.name_chat_printer()
'''
