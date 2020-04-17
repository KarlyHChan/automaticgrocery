import time
from selenium import webdriver

driver = webdriver.Chrome(r'C:\Users\Karly\Documents\workspace\grocery\chromedriver.exe')
# Optional argument, if not specified will search path.
driver.get('http://www.google.com/')
time.sleep(0)  # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(0)  # Let the user actually see something!
driver.quit()


def launch_browser():
    """
    We use two third party packages to automate web browsing:
    1) selenium https://selenium-python.readthedocs.io/
        this is a python package used for automating testing browser gui.
    2) Chrome driver
        https://chromedriver.chromium.org/
        This is a driver used by selenium to launch Chrome

    Task:
    1 ) Create a python virtual environment that allows you to run your program
        a) make sure python 3 is installed in your machine, run
            > python --version
            to check the version
            if it is not there, install it
        b) create a virtual environment for this project
            > python -m venv venv
        c) activate the virtual environment
            > venv\Scripts\activate
        d) install the selenium package
            > pip install selenium
        e) Download chromdriver, follow instruction from the link to test launching chrome
            https://chromedriver.chromium.org/getting-started


    """