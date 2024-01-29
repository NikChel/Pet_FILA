from selenium.common import TimeoutException
from base.base_class import BaseClass


class BasePage(BaseClass):
    """Данные"""
    def __init__(self, base_url, open_base_url):
        """Запуск webdriver по заданному адресу"""
        super().__init__(base_url, open_base_url)

    """Locators"""

    fila_logo_button = "//div[@class='navigation-main__logo']"
    men = "(//a[@href='https://www.fila.com/men'])[1]"
    boots = "(//a[@href='https://www.fila.com/men-boots'])[1]"
    header_promo = "//div[@class='header-promo-slot']/p/span"

    "Locators - Mini cart"

    mini_cart = "//a[@class='a bag-icon btn-cart']"
    mini_cart_name_product = "(//div[@class='mini-cart-name']/a)["
    mini_cart_size_product = "(//span[@class='value Size'])["
    mini_cart_standard_price_first_part = "(//div[@class='navigation-main__utility']//div[@class='mini-cart-price'])["
    mini_cart_standard_price_second_part = "]/span"
    mini_cart_discount_price_first_part = "(//div[@class='navigation-main__utility']//div[@class='mini-cart-price'])["
    mini_cart_discount_price_second_part = "]/span[2]"
    mini_cart_no_discount_price = ""
    mini_cart_quantity = "(//span[@class='value'])["
    mini_cart_subtotal = "(//div[@class='minicartsubtotals']/span[@class='value'])[1]"
    mini_cart_view_shopping_bag = "(//button[@class='button-flatlink view-bag'])[1]"
    end_field = "]"

    """Methods"""

    def get_promo(self, xpath=header_promo, description="some"):
        promo = None
        try:
            promo_text = self.get_text(xpath=xpath, description="product promo", wait_time=5)

            list_promo = promo_text.split(" ")
            for n in list_promo:
                if n.endswith("%"):
                    promo = n.partition("%")[0]
                    print("Extracted % from the", description, 'promo', "-", promo)
        except TimeoutException:
            promo = False
            promo_text = False
        return promo, promo_text

    def check_mini_cart(self, name, quantity, price, size, num):
        xpath_name = self.mini_cart_name_product + str(num) + self.end_field
        xpath_quantity_product = self.mini_cart_quantity + str(num) + self.end_field
        xpath_standard_price = (self.mini_cart_standard_price_first_part + str(num)
                                + self.mini_cart_standard_price_second_part)
        xpath_discount_price = (self.mini_cart_discount_price_first_part + str(num)
                                + self.mini_cart_discount_price_second_part)
        xpath_size = self.mini_cart_size_product + str(num) + self.end_field
        self.assert_word(word=name, xpath=xpath_name, description_text="mini cart name product")
        self.assert_word(word=quantity, xpath=xpath_quantity_product,
                         description_text="mini cart quantity product")
        self.assert_word(word=size, xpath=xpath_size, description_text="mini cart size product")
        try:
            self.assert_word(word=price, xpath=xpath_discount_price,
                             description_text="mini cart price product", wait_time=5)
        except TimeoutException:
            self.assert_word(word=price, xpath=xpath_standard_price,
                             description_text="mini cart price product", wait_time=5)

    @staticmethod
    def price_in_float(price):
        price = float(price.partition("$")[2])
        return price

    @staticmethod
    def float_in_price(result):
        result = "$" + str(format(result, '.2f'))
        return result
