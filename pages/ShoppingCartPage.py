from base.base_page import BasePage
from selenium.common import TimeoutException

from utilities.logger import Logger


class ShoppingCartPage(BasePage):
    """Данные"""

    base_url = "https://www.fila.com/shopping-cart"
    error_limit_message = "Limited:"

    def __init__(self, open_base_url=False):
        """Запуск webdriver по заданному адресу"""
        base_url = self.base_url
        super().__init__(base_url, open_base_url)

    """Locators combined"""

    product_first = "(//tr[@class]["
    name_product_second = "]/td[2]/div[1]/div[1]/a)"
    size_product_second = "]/td[2]/div[1]/div[3]/div[1]/span[2])"
    quantity_product_second = "]/td[2]/div[@class='qty desktop-only'])/span[2]"
    discount_price_product_second = "]/td[4]/span[2])"
    standard_price_product_second = "]/td[4]/span)"
    subtotal_product_second = "]/td[5]/span)"
    promo_product_second = "]/td[2]/div[11]/span/p/strong/span)"

    """Locators"""

    total = "//tr[@class='order-total']/td[2]"
    checkout = "//button[@class='button-fancy-large']"
    error = "//div[contains(text(),'Limited:')]"
    quantity = "(//tr[@class]/td[3]/div[1]/span)"
    decrease_quantity = "(//tr[@class]/td[3]/div[1]/label[1])"
    remove_button = "//div[@class='cart-edit-remove']/button[@class='button-text button-remove close-link'][1]"

    """Methods"""

    def check_product(self, name, price, size, quantity, num, promo=False):
        Logger.add_start_step(method="check_product")
        xpath_name = self.product_first + str(num) + self.name_product_second
        xpath_size = self.product_first + str(num) + self.size_product_second
        xpath_quantity = self.product_first + str(num) + self.quantity_product_second
        xpath_subtotal = self.product_first + str(num) + self.subtotal_product_second
        if not promo:
            xpath_price = self.product_first + str(num) + self.standard_price_product_second
        else:
            xpath_price = self.product_first + str(num) + self.discount_price_product_second
            xpath_promo = self.product_first + str(num) + self.promo_product_second
            self.assert_word(word=promo, xpath=xpath_promo, description_text="promo")
        self.assert_word(word=price, xpath=xpath_price, description_text="price")
        self.assert_word(word=name, xpath=xpath_name, description_text="name")
        self.assert_word(word=size, xpath=xpath_size, description_text="size")
        self.assert_word(word=quantity, xpath=xpath_quantity, description_text="quantity")
        subtotal = "$" + str(format(float(price.partition("$")[2]) * float(quantity), '.2f'))
        self.assert_word(word=subtotal, xpath=xpath_subtotal, description_text="subtotal")
        print("Success check product", num)
        Logger.add_end_step(url=self.get_current_url(), method="check_product")
        return subtotal

    def check_limited(self):
        Logger.add_start_step(method="check_limited")
        try:
            self.select_in_dom(xpath=self.error, description="error message", wait_time=5)
            error = True
        except TimeoutException:
            error = False
        Logger.add_end_step(url=self.get_current_url(), method="check_limited")
        return error

    def limited_fix(self):
        Logger.add_start_step(method="limited_fix")
        print("\nLimited error, start decrease")
        data_count = self.count_mathing_elements(xpath=self.quantity, description="quantity")
        count_object = data_count[0]
        for n in range(count_object):
            count = n+1
            xpath_quantity = self.quantity + "[" + str(count) + "]"
            quantity = self.get_text(xpath=xpath_quantity, description="quantity")
            xpath_decrease = self.decrease_quantity + "[" + str(count) + "]"
            if quantity != "1":
                print("Too much quantity product - " + str(count) + ", need decrease")
                while quantity != "1":
                    self.click(xpath=xpath_decrease, description="decrease quantity")
                    quantity = self.get_text(xpath=xpath_quantity, description="quantity")
            print("Success, quantity product -", count, "= 1")

        try:
            self.select_in_dom(xpath=self.error, description="error message", wait_time=5)
        except TimeoutException:
            print("Success, limit error fixed\n")
        Logger.add_end_step(url=self.get_current_url(), method="limited_fix")

    def clear_cart(self):
        Logger.add_start_step(method="clear_cart")
        print("Start clear cart")
        while True:
            try:
                self.click(xpath=self.remove_button, description="remove button", wait_time=10)
            except TimeoutException:
                break
        print("Success clear cart")
        Logger.add_end_step(url=self.get_current_url(), method="clear_cart")
