

def send_message(driver):
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys('hello from 1inda')
    message.send_keys(Keys.ENTER)
def read_messages(driver, contact):
    messages = None
    messageRoot = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div')
    messageList = messageRoot.find_elements_by_class_name('FTBzM')
    for message in [m.text for m in messageList]:
        print(message)

    return messages