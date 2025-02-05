from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import time
import math

class WhatsAppWebClient:
    def __init__(self, chatname=None):
        if os.name == "nt":
            driverPath = "driver/chromedriver_2.24.exe"
            dataPath = "Data"
        else:
            driverPath = "driver/chromedriver"
            dataPath = "Data/ChatBot"
        self.chatname=chatname
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=" + dataPath)
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=driverPath)
        self.driver.get('https://web.whatsapp.com')
        time.sleep(15)
        print('Now you can select appropriate chat')
        self.chatsList = self.get_chats()
                
        if isinstance(chatname, str):
            self.activate_chat(self.chatname)
    def get_chats(self, attempts=3):
        chats = None
        for i in range(attempts):
            try:
                chatsRoot = self.driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div')
                return chatsRoot.find_elements_by_class_name('X7YrQ')
            except:
                time.sleep(5)
        return None

    def activate_chat(self, name):
        """
        activate (by sending click) to the chat containing name:str
        """
        for chat in self.chatsList:
            if name in chat.text:
                chat.click()
                return 0
        return 1, 'chat name not found, ensure exact case match'
    def send_message(self, message, chatname=None):
        
        assert is_instance(message, str), 'Message must be string'

        if chatname is not None:
            self.activate_chat(chatname)
            time.sleep(2)
        message_h = self.driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
        message_h.send_keys(message)
        message_h.send_keys(Keys.ENTER)
    def read_messages(self):
        messages = None
        messageRoot = self.driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div')
        messageList = messageRoot.find_elements_by_class_name('FTBzM')
        
        return [message for message in [m.text for m in messageList]]

cl=WhatsAppWebClient(chatname='NGT team chat')

print(cl.chatsList)
print(cl.activate_chat('NGT team chat'))
print(cl.read_messages()[-1])

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + dataPath)
driver = webdriver.Chrome(chrome_options=options, executable_path=driverPath)
driver.get('https://web.whatsapp.com')

#open tab
driver.execute_script("window.open('','_blank');")
#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 

class Message():
    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __eq__(self, other):
        return self.message == other.message


if os.name == "nt":
    driverPath = "driver/chromedriver_2.24.exe"
    dataPath = "Data"
else:
    driverPath = "driver/chromedriver"
    dataPath = "Data/ChatBot"


options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + dataPath)
driver = webdriver.Chrome(chrome_options=options, executable_path=driverPath)
driver.get('https://web.whatsapp.com')

#open tab
driver.execute_script("window.open('','_blank');")
#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
driver.switch_to_window(driver.window_handles[1])
#driver.get('http://www.square-bear.co.uk/mitsuku/nfchat.htm')
driver.get('http://www.mars.com')
import time;time.sleep(25)
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

input("Choose a chat on whatsapp and press enter : ")
chatHistory = []
replyQueue = []
firstRun = True

print("Starting...")

while True:
    try:

        driver.switch_to_window(driver.window_handles[0])
        usersDiv = driver.find_element_by_id("side")
        messageDiv = driver.find_element_by_id("main")
        messageList = messageDiv.find_elements_by_class_name("msg")

        newMessages = []
        for message in reversed(messageList):
            bubbleText = None
            try:
                bubbleText = message.find_element_by_class_name(
                    "message-chat").find_element_by_class_name("bubble")
            except:
                pass

            if bubbleText is not None:
                author = "Unknown"
                msgObj = None
                if "has-author" in bubbleText.get_attribute("class"):
                    try:
                        author = bubbleText.find_element_by_class_name(
                            "message-author").find_element_by_class_name("emojitext").text
                    except Exception as e:
                        pass
                elif "msg-group" in message.get_attribute("class"):
                    author = "Akshay Aradhya"
                try:
                    text_message = bubbleText.find_element_by_class_name(
                        "message-text").find_element_by_class_name("emojitext").text
                    if len(text_message) > 0:
                        msgObj = Message(author, text_message)
                except Exception as e:
                    pass

                if len(chatHistory) > 0 and (msgObj is not None) and msgObj == chatHistory[-1]:
                    break
                elif msgObj is not None:
                    newMessages.append(msgObj)

        # print("New Messages : ", len(newMessages))
        for message in reversed(newMessages):
            chatHistory.append(message)

        # Update Unknown Users
        for i in range(len(chatHistory)):
            if i > 0 and chatHistory[i].user == "Unknown":
                chatHistory[i].user = chatHistory[i - 1].user

        for message in reversed(newMessages):
            if message.message[0] == "$" and firstRun == False:
                replyQueue.append(message)

        # print("Querries =", len(replyQueue))

        firstRun = False
        if len(replyQueue) == 0:
            continue

        # Switch tabs and get Response
        driver.switch_to_window(driver.window_handles[1])
        driver.switch_to_default_content()
        driver.switch_to.frame('input')
        textField = driver.find_elements_by_tag_name("input")[1]

        responses = []

        for message in replyQueue:

            textField.send_keys(message.message[1:] + Keys.ENTER)
            responseBody = None
            fontTags = driver.find_elements_by_tag_name("font")

            for tag in fontTags:
                if tag.get_attribute("face") == "Trebuchet MS,Arial" and tag.get_attribute("color") == "#000000":
                    responseBody = tag
                    break

            start = responseBody.text.find("Μitsuku")
            end = responseBody.text.find("You", 4)
            firstName = message.user.split(' ')[0]
            resp = responseBody.text[start + 10:end - 2]
            print(start, end, repr(resp))
            responses.append("@" + firstName + " : " + resp)

        replyQueue = []
        # Switch tabs and reply on whatsapp
        driver.switch_to_window(driver.window_handles[0])
        inputMessage = messageDiv.find_element_by_class_name(
            'pluggable-input-body')

        for response in responses:
            lines = response.split('\n')
            for line in lines:
                inputMessage.send_keys(line)
                inputMessage.send_keys(Keys.SHIFT, Keys.ENTER)
            inputMessage.send_keys(Keys.ENTER)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
