import random
from base.base_page import BasePage


class CatalogPage(BasePage):
    """Данные"""

    base_url = "https://www.fila.com/warehouse-sale"
    product_on_page_num = '1'

    def __init__(self, open_base_url=False):
        """Запуск webdriver по заданному адресу"""
        base_url = self.base_url
        super().__init__(base_url, open_base_url)

    """Locators"""

    left_scroll_button = "//div[@class='swiper-button-prev']"
    accept_button = "//button[@class='tracking-consent-accept']"

    """Locators combined"""

    name_field = "(//a[@class='name-link'])["
    price_field = "(//span[@class='product-sales-price'])["
    color_field_first = "(//ul[@class='swatch-list'])["
    color_field_second = "/li/a[@title]"
    quick_add_button = "(//button[@class='open-quick-add-button'])["
    size_button_first = "(//div[@class='quick-add-variants'])["
    size_button_second = "/button"
    product_button = "(//div[@class='swiper-slide swiper-slide-active']/a)["
    right_scroll_button = "(//div[@class='swiper-button-next'])["
    promo_field = "(//div[@class='product-promo selected']/div/p/strong)["

    """Methods"""

    def quick_add(self, product_on_page_num=product_on_page_num):
        data_get_name_price = self.get_product_data(product_on_page_num=product_on_page_num)
        name = data_get_name_price[0]
        price = data_get_name_price[1]
        product_button = data_get_name_price[2]
        promo = data_get_name_price[3]
        promo_text = data_get_name_price[4]
        color_field = self.color_field_first + str(product_on_page_num) + self.end_field + self.color_field_second
        qick_add_button = self.quick_add_button + str(product_on_page_num) + self.end_field
        size_button = self.size_button_first + str(product_on_page_num) + self.end_field + self.size_button_second
        right_scroll_button = self.right_scroll_button + str(product_on_page_num) + self.end_field
        self.move_to_element(xpath=product_button, description="product")
        self.click(xpath=right_scroll_button, description="right scroll")
        self.click(xpath=self.left_scroll_button, description="left scroll")
        data_count = self.count_mathing_elements(xpath=color_field, description="color")
        count = data_count[0]
        random_num_color = random.randint(a=1, b=int(count))
        color_field = "(" + color_field + ")[" + str(random_num_color) + self.end_field
        color = self.get_attribute_value(xpath=color_field, attribute="title")
        self.move_to_element(xpath=product_button, description="product")
        self.click(xpath=color_field, description="color")
        self.move_to_element(xpath=product_button, description="product")
        self.click(xpath=qick_add_button, description="quick add")
        data_count = self.count_mathing_elements(xpath=size_button, description="size")
        count = data_count[0]
        random_num_size = random.randint(a=1, b=count)
        size_button = "(" + size_button + ")[" + str(random_num_size) + self.end_field
        size = self.get_attribute_value(xpath=size_button, attribute="title")
        self.click(xpath=size_button, description="size")
        return name, price, color, size, product_button, promo, promo_text

    def get_product_data(self, product_on_page_num=product_on_page_num):
        name_field = self.name_field + str(product_on_page_num) + self.end_field
        price_field = self.price_field + str(product_on_page_num) + self.end_field
        promo_field = self.promo_field + str(product_on_page_num) + self.end_field
        product_button = self.product_button + str(product_on_page_num) + self.end_field
        name = self.get_attribute_value(xpath=name_field, attribute="title")
        price = self.get_text(xpath=price_field, description="price")
        data_promo = self.get_promo(xpath=promo_field, description="product")
        promo = data_promo[0]
        promo_text = data_promo[1]
        if not promo:
            pass
        else:
            price = price.partition("$")[2]
            price = format(float(price) / 100 * (100 - float(promo)), '.2f')
            price = "$" + str(price)
        return name, price, product_button, promo, promo_text
