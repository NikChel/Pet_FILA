from selenium.webdriver.common.by import By
import random
from base.base_page import BasePage
from selenium.common import TimeoutException


class ProductPage(BasePage):
    """Данные"""

    base_url = "https://www.fila.com/mens-grant-hill-1-x-trailpacer/1QM00780.html"

    def __init__(self, open_base_url=False):
        """Запуск webdriver по заданному адресу"""
        base_url = self.base_url
        super().__init__(base_url, open_base_url)

    """Locators"""

    name_product = "//h1[@class='product-name']"
    price_product_standard = "//span[@class='price-standard no-sale']"
    price_product_discount = "(//span[@class='price-sales'])"
    price_product_no_discount = "//span[@class='price-standard']"
    promo_field = "//span[@class='promo-title']/p/strong/span"
    size_button = "(//ul[@class='swatches size']/li)"
    color_button = "(//ul[@class='swatches Color']/li/a)"
    quantity_product_field = "//div[@class='quantity-container']/input"
    add_to_cart_button = "//button[@id='add-to-cart']"

    "Locators - Added To Your Bag"

    view_bag_button = "//button[@class='checkout']"
    close_window = ("(//button[@class='ui-button ui-corner-all ui-widget "
                    "ui-button-icon-only ui-dialog-titlebar-close'])[2]")
    add_name_product = "//div[@class='product-name']"
    add_size_product = "//div[@class='checkoutminicart minicartproducts'][1]/div[1]/div[2]/div[2]/div/div[2]/span[2]"
    add_quantity_product = ("(//div[@class='checkoutminicart minicartproducts']/div/div[@class='mini-cart-details'])"
                            "/div[@class='mini-cart-pricing']/span/span")
    add_standard_price_product = "//div[@class='checkoutminicart minicartproducts'][1]/div[1]/div[2]/div[1]/div[2]/span"
    add_discount_price_product = ("//div[@class='checkoutminicart "
                                  "minicartproducts'][1]/div[1]/div[2]/div[1]/div[2]/span[2]")
    add_promo = "//div[@class='checkoutminicart minicartproducts'][1]/div[1]/div[2]/div[4]/span/p/strong/span"

    """Methods"""

    def check_name_price(self, name, price):
        self.assert_word(word=name, xpath=self.name_product, description_text="name")
        try:
            self.assert_word(word=price, xpath=self.price_product_standard,
                             description_text="price standard", wait_time=5)
        except TimeoutException:
            self.assert_word(word=price, xpath=self.price_product_discount,
                             description_text="price discount")

    def check_product_window(self, name, quantity_product, size, price):
        self.assert_word(word=name, xpath=self.add_name_product, description_text="add name product")
        self.assert_word(word=quantity_product, xpath=self.add_quantity_product, description_text="add quantity "
                                                                                                  "product")
        self.assert_word(word=size, xpath=self.add_size_product, description_text="add size product")
        try:
            self.assert_word(word=price, xpath=self.add_discount_price_product, description_text="add price product",
                             wait_time=5)
        except TimeoutException:
            self.assert_word(word=price, xpath=self.add_standard_price_product, description_text="add price product")
        self.click(xpath=self.close_window, description="close window")

    def select_size(self):
        self.select_in_dom(xpath=self.size_button, description="size button")
        lst_element = self.driver.find_elements(By.XPATH, self.size_button)
        lst_num = []
        count = 0
        for n in lst_element:
            count += 1
            result = n.get_attribute("class")
            if result == "" or result == "selected":
                lst_num.append(count)
            else:
                pass

        random_size_num = str(random.choice(lst_num))
        random_size_xpath = self.size_button + "[" + random_size_num + "]"
        self.click(xpath=random_size_xpath, description="size")
        size_attribute_xpath = random_size_xpath + "/a"
        size_attribute = self.get_attribute_value(xpath=size_attribute_xpath, attribute="title")
        return size_attribute

    def select_color(self):
        data_count_colors = self.count_mathing_elements(xpath=self.color_button, description="color")
        count_colors = data_count_colors[0]
        random_num = random.randint(a=1, b=int(count_colors))
        random_color_xpath = self.color_button + "[" + str(random_num) + "]"
        self.click(xpath=random_color_xpath, description="color")
        color_attribute = self.get_attribute_value(xpath=random_color_xpath, attribute="title")
        return color_attribute
