from chat_downloader import ChatDownloader

class analysor(object):

  def __init__(self, url):
    self.pre = [] #chats before streaming start
    self.post = [] #chats after streaming start
    self.time = [] #push time period in the array
    self.time_sum = [] #count the chats number per min
    self.name = [] #push the user name
    self.chat = [] #push the user chat
    self.name_chat = {} #user name and chat pair dict

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
        test_line = value.split('|') #split time and others data
        self.time.append(self.Time_processor(test_line[0]))

        if 'Member' in test_line[1]:#members or not
          #members
          self.Name_Chat_processor(test_line[1], '))')

        elif 'New' in test_line[1]:
          #new members
          if "Moderator" in test_line[1]:
            self.Name_Chat_processor(test_line[1], '))')
          else:
            self.Name_Chat_processor(test_line[1], ')')
        else:
          #not members
          if 'Moderator' in test_line[1]:
            self.Name_Chat_processor(test_line[1], ')')
    return self

  def Name_Chat_processor(self, test_line, signal):
    if signal is ')':
      test_brac = test_line.split(')')
      test_name_chat = test_brac[1].split(':') #test_name_chat 0 is name, 1 is chat
      self.name.append(test_name_chat[0])
      self.chat.append(test_name_chat[1])
      self.Chat_dictionary(test_name_chat[0], test_name_chat[1])

    if signal is '))':
      test_brac = test_line.split(')')
      test_name_chat = test_brac[1].split(':') #test_name_chat 0 is name, 1 is chat
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
    #push name and chat data in the dict
    if temp_name in self.name_chat.keys():
      self.name_chat[temp_name].append(temp_chat)
    else:
      self.name_chat[temp_name] = []
      self.name_chat[temp_name].append(temp_chat)
    return self

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
