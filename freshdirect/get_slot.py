import time
from selenium import webdriver
import winsound
import threading
import os
import traceback
import freshdirect.grocery_config as config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def create_driver(url):
    options = webdriver.ChromeOptions()
    project_dir=f"{os.path.dirname(os.path.realpath(__file__))}/.."
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options,
                              executable_path=f'{project_dir}/chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.get(url)
    return driver
def waitandclick(driver, xpath):
    checkout = wait_and_find(driver, xpath)
    checkout.click()


def wait_and_find(driver, xpath, wait_time=10):
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.XPATH, xpath)))
    checkout = driver.find_element_by_xpath(xpath)
    return checkout


def alert_user(slots):
    freq = 2500
    dur = 5000

    class AlertThread(threading.Thread):
        def __init__(self):
            super().__init__()
            self.stopped = False

        def run(self):
            self.stopped = False
            while not self.stopped:
                winsound.Beep(freq, dur)
                time.sleep(1)
                #print(f"Stopped: {self.stopped}")

    thread = AlertThread()
    thread.start()
    input(f"Found slot({slots}) - please order: Press any key to stop the beep")
    thread.stopped = True
    print("Waiting for alert thread to die")
    thread.join()
    print("alert thread is dead")


def run_loop(url: str, loop_func):
    driver = create_driver(url)
    signinbutton = driver.find_element_by_xpath('//*[@id="nav-link-accountList"]')
    signinbutton.click()
    email = driver.find_element_by_xpath('//*[@id="ap_email"]')
    email.click()
    email.send_keys(config.amazon_username)
    email.submit()
    password = driver.find_element_by_id('ap_password')
    password.click()
    password.send_keys(config.amazon_password)
    password.submit()
    cart = driver.find_element_by_id('nav-cart')
    cart.click()
    waitandclick(driver, '//*[@id="sc-alm-buy-box-ptc-button-VUZHIFdob2xlIEZvb2Rz"]/span/input')
    waitandclick(driver, '//*[@id="a-autoid-0"]/span/a')
    con2 = driver.find_element_by_xpath('//*[@id="subsContinueButton"]/span/input')
    con2.click()

    slots =[]
    while True:
        try:
            if len(slots) > 0:
                alert_user(slots)
            import sys
            if len(sys.argv) == 1:
                cmd = input("""Please enter how many times you want to loop for result:
                enter * for infinite loop
                enter q to quit
                 """)
            else:
                time.sleep(3)
                cmd = sys.argv[1]
            if cmd == "*":
                slots = loop_func(driver, retries=None)
            elif cmd == "q":
                driver.quit()
                break
            else:
                slots = loop_func(driver, retries=int(cmd))
        except Exception as e:
            print(f"Exception occurred in run_loop: {e}")
            traceback.print_exc()