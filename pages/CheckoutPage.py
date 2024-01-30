import allure
from selenium.webdriver import Keys
from base.base_page import BasePage
from utilities.logger import Logger


class CheckoutPage(BasePage):
    """Данные"""

    base_url = None

    def __init__(self, open_base_url=False):
        """Запуск webdriver по заданному адресу"""
        base_url = self.base_url
        super().__init__(base_url, open_base_url)

    """Locators check"""

    check_product_first = "//div[@id='tabs-1']/div/div[2]/div/div["
    check_name_second = "]/div[2]/div/a"
    check_price_standard_second = "]/div[2]/div[1]/div/span"
    check_price_discount_second = "]/div[2]/div[1]/div/span[2]"
    check_size_second = "]/div[2]/div[2]/div/div[1]/span[2]"
    check_quantity_second = "]/div[2]/div[3]/span/span"
    check_promo_second = "]/div[2]/div[4]/span/p/strong/span"
    check_total = "//div[@id='tabs-1']/div/div[1]/table/tbody/tr[4]/td[2]"

    """Locators input"""

    first_name_field = "//input[@id='dwfrm_singleshipping_shippingAddress_addressFields_firstName']"
    last_name_field = "//input[@id='dwfrm_singleshipping_shippingAddress_addressFields_lastName']"
    street_field = "//input[@id='dwfrm_singleshipping_shippingAddress_addressFields_address1']"
    apt_floor_field = "//input[@id='dwfrm_singleshipping_shippingAddress_addressFields_address2']"
    zip_field = "//input[@id='dwfrm_singleshipping_shippingAddress_addressFields_zip']"
    phone_field = "//input[@id='dwfrm_singleshipping_shippingAddress_addressFields_phone']"
    city_field = "//input[@id='dwfrm_singleshipping_shippingAddress_addressFields_city']"

    """Locators button"""

    state_drop_down = "//span[@id='dwfrm_singleshipping_shippingAddress_addressFields_states_state-button']"
    arizona_drop_down = "//li[@class='ui-menu-item'][3]/div"
    select_drop_down = "//li[@class='ui-menu-item'][1]/div"
    continue_button = "//button[@class='button-fancy-large button-solid']"

    """Methods"""

    def check_product(self, name, price, size, quantity, num, promo=False):
        with allure.step("Check product"):
            Logger.add_start_step(method="check_product")
            xpath_name = self.check_product_first + str(num) + self.check_name_second
            xpath_size = self.check_product_first + str(num) + self.check_size_second
            xpath_quantity = self.check_product_first + str(num) + self.check_quantity_second
            if not promo:
                xpath_price = self.check_product_first + str(num) + self.check_price_standard_second
            else:
                xpath_price = self.check_product_first + str(num) + self.check_price_discount_second
                xpath_promo = self.check_product_first + str(num) + self.check_promo_second
                self.assert_word(word=promo, xpath=xpath_promo, description_text="promo")
            self.assert_word(word=price, xpath=xpath_price, description_text="price")
            self.assert_word(word=name, xpath=xpath_name, description_text="name")
            self.assert_word(word=size, xpath=xpath_size, description_text="size")
            self.assert_word(word=quantity, xpath=xpath_quantity, description_text="quantity")
            Logger.add_end_step(url=self.get_current_url(), method="check_product")
            print("Success check product", num)

    def clear_all_field(self):
        with allure.step("Clear all field"):
            Logger.add_start_step(method="clear_all_field")
            print("\n\nStart clear Shipping Address")
            self.clear_field(xpath=self.first_name_field, description="First Name")
            self.clear_field(xpath=self.last_name_field, description="Last Name")
            self.clear_field(xpath=self.street_field, description="Street Address")
            self.clear_field(xpath=self.apt_floor_field, description="Apt., Suite, Floor (Optional)")
            self.clear_field(xpath=self.zip_field, description="Zip Code")
            self.click(xpath=self.state_drop_down, description="state dropdown")
            self.click(xpath=self.select_drop_down, description="select dropdown")
            self.clear_field(xpath=self.city_field, description="City")
            self.clear_field(xpath=self.phone_field, description="Phone Number")
            self.send_keys(keys=Keys.RETURN, xpath=self.phone_field)
            Logger.add_end_step(url=self.get_current_url(), method="clear_all_field")
            print("Success clear Shipping Address")
