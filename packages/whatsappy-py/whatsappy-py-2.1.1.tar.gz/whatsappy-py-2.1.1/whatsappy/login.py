import os
import re
import cv2
import shelve
import platform
from time import sleep
from os import getlogin, mkdir
from selenium import webdriver
from send2trash import send2trash
from webdriver_manager.chrome import ChromeDriverManager
from .error import LoginError

os.environ["WDM_LOG_LEVEL"] = "0"


def get_qrcode(driver, timeout):

    for _ in range(timeout//5):
        qr_code = driver.find_element_by_css_selector(".landing-main")

        qr_code.screenshot("qrcode.png")

        img = cv2.imread("qrcode.png", 1)

        cv2.imshow("Scan the QRCode to login", img)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        try:
            driver.find_element_by_xpath(
                '//*[@id="side"]/div[1]/div/label/div/div[2]'
            )

            send2trash("qrcode.png")
            break
        except:
            pass


def login(self, visible: bool = True, timeout: int = 60):
    """Logs in whatsapp and shows the QRCode if necessary

    Args:
        visible (bool, optional): Shows the process. Defaults to False.
        timeout (int, optional): Limit time to login in seconds. Defalts to 60
    """

    os_path = {
        "Windows": rf"{os.path.expanduser('~')}/AppData/Local/Google/Chrome/User Data/Default",   # Windows
        "Linux": rf"{os.path.expanduser('~')}/.config/google-chrome/default",                            # Linux
        "Darwin": rf"{os.path.expanduser('~')}/Library/Application Support/Google/Chrome/Default" # Mac OS
    }

    usr_path = os_path[platform.system()] 

    try:
        self.mydata = shelve.open("data/data")
    except:
        try:
            mkdir("data")
        except:
            pass

        self.mydata = shelve.open("data/data")
        
        options = webdriver.ChromeOptions()
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=OFF")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self.mydata["user_agent"] = driver.execute_script(
            "return navigator.userAgent"
        )
        driver.close()

    print(f'Logging as: {self.mydata["user_agent"]}')

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={usr_path}")
    options.add_argument(f"--user-agent={self.mydata['user_agent']}")
    options.add_argument("--start-maximized")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=OFF")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    self.mydata.close()

    if not visible:
        options.add_argument("--headless")

    self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    self.driver.get("https://web.whatsapp.com")

    logged = False
    for _ in range(timeout):
        try:
            self.driver.find_element_by_xpath(
                '//*[@id="side"]/div[1]/div/label/div/div[2]'
            )
            break

        except:
            if not visible:
                try:
                    self.driver.find_element_by_css_selector(".landing-main")

                    get_qrcode(self.driver, timeout)
                    break

                except:
                    sleep(1)
            
            else:
                sleep(1)


    self.driver.implicitly_wait(60)
    self.driver.find_element_by_xpath(
        '//*[@id="side"]/div[1]/div/label/div/div[2]'
    )

    logged = True

    if logged or visible:
        print("Done")
    else:
        self.close()
        raise LoginError("Failed to login to WhatsApp")


def close(self):
    """Exit the whatsapp"""

    self.driver.close()
