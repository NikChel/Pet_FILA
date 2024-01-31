from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains

project_path = "C:\\Users\\globl\\PycharmProjects\\Pet_2"
webdriver_path = "C:\\Users\\globl\\PycharmProjects\\resource\\chromedriver.exe"


class BaseClass:
    """Настройки для webdriver"""
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)     # after finishing work, leave the browser open
    # options.add_argument('--headless')  # minimized window mode
    g = Service(webdriver_path)
    driver = webdriver.Chrome(options=options, service=g)
    driver.maximize_window()
    action = ActionChains(driver)

    wait_time = 30  # standard explicit wait time
    reconnect = 5   # standard number of reconnections

    def __init__(self, base_url, open_base_url):
        """Запуск webdriver по заданному адресу"""
        if open_base_url:
            self.base_url = self.try_connect_url(base_url)

    """Actions"""

    def click(self, xpath, description="some", wait_time=wait_time, scroll=True, next_page=False):
        button = WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        if scroll:
            self.action.scroll_to_element(button).perform()
        else:
            self.scroll_to_end(end=False)
        WebDriverWait(self.driver, wait_time).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        if next_page:
            url = self.get_current_url()
            button.click()
            self.check_url_is_change(old_url=url)
        else:
            button.click()
        print('Click to', description, 'button, success')

    def move_to_element(self, xpath, description="some", wait_time=wait_time, scroll=True):
        element = WebDriverWait(self.driver, wait_time).until(ec.presence_of_element_located((By.XPATH, xpath)))
        if scroll:
            self.action.scroll_to_element(element).perform()
        else:
            self.scroll_to_end(end=False)
        self.action.move_to_element(element).perform()
        print("Move to", description, "object")

    def select_in_dom(self, xpath, description="some", wait_time=wait_time):
        element = WebDriverWait(self.driver, wait_time).until(ec.presence_of_element_located((By.XPATH, xpath)))
        print('Select', description, 'object')
        return element

    def select_clickable(self, xpath, description="some", wait_time=wait_time):
        button = WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        self.action.scroll_to_element(button).perform()
        WebDriverWait(self.driver, wait_time).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        print(description, "button is clickable")

    def send_keys(self, keys, xpath, description='some', wait_time=wait_time):
        write = WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        self.action.scroll_to_element(write).perform()
        write = WebDriverWait(self.driver, wait_time).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        write.send_keys(keys)
        print('Send keys -', keys, 'in', description, 'field')

    def scroll_to_end(self, description="some", end=True):
        prev_height = -1
        max_scrolls = 100
        scroll_count = 1
        while scroll_count < max_scrolls:
            html = self.driver.find_element(By.TAG_NAME, 'html')
            if end:
                html.send_keys(Keys.PAGE_DOWN)
            else:
                html.send_keys(Keys.PAGE_UP)
            time.sleep(1)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                print("Scroll to end", description, "page")
                break
            prev_height = new_height
            scroll_count += 1

    def clear_field(self, xpath, description="some"):
        self.send_keys(keys=Keys.CONTROL + "a", xpath=xpath)
        self.send_keys(keys=Keys.BACKSPACE, xpath=xpath)
        print(description, "field Cleared")

    """Methods"""

    def get_text(self, xpath, description='some', wait_time=wait_time):
        check = WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        check_text = check.text
        print("Extracted text from the", description, 'field', "-", check_text)
        return check_text

    def get_attribute_value(self, xpath, attribute, wait_time=wait_time):
        check = WebDriverWait(self.driver, wait_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        check_attribute = check.get_attribute(attribute)
        print("Extracted value from the", attribute, 'attribute', "-", check_attribute)
        return check_attribute

    def get_screenshot(self, assert_screen=False):
        now_date = datetime.datetime.utcnow().strftime("%Y.%m.%d.%H.%M.%S")
        name_screenshot = "screenshot" + now_date + ".png"
        if assert_screen:
            path = project_path + "\\screens\\assert\\"
        else:
            path = project_path + "\\screens\\success\\"
        self.driver.save_screenshot(path + name_screenshot)
        print("Screenshot", name_screenshot, "saved")
        return name_screenshot

    def get_current_url(self):
        get_url = self.driver.current_url
        return get_url

    def try_connect_url(self, base_url):
        connect = False
        for n in range(self.reconnect):
            self.driver.get(base_url)
            current_url = self.get_current_url()
            if current_url != base_url:
                print("Connection failed, reconnect, try", n + 1)
                time.sleep(3)
                continue
            else:
                connect = True
                break
        assert connect is True, "Can't connect"
        print("\nOpen", base_url)
        return base_url

    def check_url_is_change(self, old_url, reconnect=reconnect):
        status = False
        current_url = None
        for n in range(reconnect):
            current_url = self.get_current_url()
            time.sleep(1)
            if current_url == old_url:
                print("Url not change, try", n+1)
                time.sleep(2)
            else:
                status = True
                break
        assert status is True, print("Fail open new url")
        print("\nOpen", current_url)
        return current_url

    def count_mathing_elements(self, xpath, description="some", wait_time=wait_time):
        WebDriverWait(self.driver, wait_time).until(ec.presence_of_element_located((By.XPATH, xpath)))
        lst_element = self.driver.find_elements(By.XPATH, xpath)
        count_element = len(lst_element)
        print("Count", description, "element =", count_element)
        return count_element, lst_element

    def assert_url(self, url, wait_time=wait_time):
        check_url = WebDriverWait(self.driver, wait_time).until(ec.url_to_be(url))
        assert check_url, (f"Test failed, expected - {url}, receive - {self.get_current_url()}, check "
                           f"{self.get_screenshot(assert_screen=True)}")
        print("Test url success,", url, '==', check_url)

    def assert_word(self, word, xpath, description_text='some', wait_time=wait_time, attribute=False):
        if not attribute:
            element_word = self.get_text(xpath=xpath, wait_time=wait_time, description=description_text)
        else:
            element_word = self.get_attribute_value(xpath=xpath, attribute=attribute, wait_time=wait_time)
        assert element_word.lower() == word.lower(), (f"Test failed, expected - {word}, receive - "
                                                      f"{element_word}, check screenshot "
                                                      f"{self.get_screenshot(assert_screen=True)}")
        print("Test word success,", element_word, '==', word)
