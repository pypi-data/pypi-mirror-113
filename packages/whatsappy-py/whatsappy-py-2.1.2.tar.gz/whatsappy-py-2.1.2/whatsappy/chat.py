import re
import shutil
import logging
from .tool import *
from os import path
from .error import BadPathError
from send2trash import send2trash
from selenium.webdriver.common.keys import Keys

last = ""


class Message:
    def __init__(self, author, content, time, date):
        self.author = author
        self.time = time
        self.date = date
        self.content = content

    def __str__(self):
        return f"Author: {self.author}\nTime: {self.time}\nDate: {self.date}\nContent: {self.content}"


def last_message(self):
    """Gets the last message from the chat

    Returns:
        Class: Last message
    """

    global Message

    info = self.driver.execute_script(
        """
        var a = document.querySelectorAll(".message-in");
        return a[a.length - 1].querySelector('.copyable-text').dataset.prePlainText;
    """
    )

    content = self.driver.execute_script(
        """
        var a = document.querySelectorAll(".message-in");
        return a[a.length - 1].querySelector('.copyable-text').innerText;
    """
    )

    time = re.compile(r"(\d+:\d+(\s)?(AM|PM)?)").findall(info)[0][0]
    date = re.compile(r"(\d+/\d+/\d+)").findall(info)[0]
    author = re.compile(r"] (.*):").findall(info)[0]

    return Message(author=author, content=content, time=time, date=date)


def new_message(self):
    """Returns True for a new message

    Returns:
        Bool: New message
    """

    global last

    try:
        message = self.last_message()
        if last == "":
            last = message.content

        if message.content != last:
            last = message.content
            
            logging.info(f"{message.author}: {message.content} (at {message.date} {message.time})")
            return True

        else:
            return False
    except:
        pass


def send(self, message: str):
    """Sends a message

    Args:
        message (str): The message you want to send
    """

    chat = self.driver.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]'
    )

    if message.find("\n"):
        for line in message.split("\n"):
            chat.send_keys(line)
            chat.send_keys(Keys.SHIFT + Keys.ENTER)
        chat.send_keys(Keys.ENTER)
    else:
        chat.send_keys(message)

    logging.info(f"You sent: {message}")


def send_file(self, file_path: str):
    """Sends a file

    Args:
        file_path (str, absolute path): The file of the path you want to send
    """

    if not path.isabs(file_path):
        raise BadPathError("The file path is not absolute")

    regex = re.compile(r"(\w+\.(\w+))")
    file_name = file_path.split("\\")[-1]
    isZip = False

    if regex.findall(file_name):
        if regex.findall(file_name)[0] in ["png", "jpg", "mp4", "3gpp"]:
            type = 1
        else:
            type = 3

    else:
        shutil.make_archive(file_name, "zip", file_name)

        file_path = path.abspath(file_name + ".zip")
        isZip = True

        type = 3

    self.driver.find_element_by_xpath(
        '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div/span'
    ).click()

    img_box = self.driver.find_element_by_xpath(
        f'//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[{type}]/button/input'
    )

    img_box.send_keys(file_path)

    while True:
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div'
            ).click()

            break
        except:
            pass

    if isZip:
        send2trash(file_name + ".zip")
    
    logging.info(f"You sent the file: {file_path}")


def reply(self, message: str):
    """Replies to the last message

    Args:
        message (str): The message you want to send
    """

    self.driver.execute_script(
        """
        var a = document.querySelectorAll('.message-in');
        var elem = a[a.length -1]
        var clickEvent = document.createEvent('MouseEvents');
        clickEvent.initEvent('dblclick', true, true);
        elem.dispatchEvent(clickEvent);
    """
    )
    self.send(message)

    logging.info(f"You replied with: {message}")


def reply_privately(self, message: str):
    """Sends a message message privatly to the last message in chat

    Args:
        message (str): The message you want to send
    """

    group_name = self.driver.find_element_by_xpath(
        '//*[@id="main"]/header/div[2]/div/div/span'
    ).text

    self.driver.execute_script(
        """
        var event = new MouseEvent('mouseover', {
            'view': window,
            'bubbles': true,
            'cancelable': true
        });

        var a = document.querySelectorAll('.message-in > div');
        var element = a[a.length -1];
        
        element.dispatchEvent(event);
    """
    )

    self.driver.find_element_by_css_selector(
        ".message-in > div > div > span > div > div"
    ).click()

    self.driver.find_element_by_css_selector(
        "#app > div > span:nth-child(4) > div > ul > li:nth-child(2)"
    ).click()

    logging.info(f"You changed chat reply privately")
    self.send(message)
    self.select_chat_by_name(group_name)


def reply_file_privately(self, file_path: str):
    """Sends a file privatly to the last message in chat

    Args:
        file_path (str, absolute path): The file of the path you want to send
    """

    group_name = self.driver.find_element_by_xpath(
        '//*[@id="main"]/header/div[2]/div/div/span'
    ).text

    self.driver.execute_script(
        """
        var event = new MouseEvent('mouseover', {
            'view': window,
            'bubbles': true,
            'cancelable': true
        });

        var a = document.querySelectorAll('.message-in > div');
        var element = a[a.length -1];
        
        element.dispatchEvent(event);
    """
    )

    self.driver.find_element_by_css_selector(
        ".message-in > div > div > span > div > div"
    ).click()

    self.driver.find_element_by_css_selector(
        "#app > div > span:nth-child(4) > div > ul > li:nth-child(2)"
    ).click()

    logging.info(f"You changed chat reply privately")
    self.send_file(file_path)
    self.select_chat_by_name(group_name)
