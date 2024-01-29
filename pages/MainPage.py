from base.base_page import BasePage


class MainPage(BasePage):
    """Данные"""

    base_url = "https://www.fila.com/us"

    def __init__(self, open_base_url=False):
        """Запуск webdriver по заданному адресу"""
        base_url = self.base_url
        super().__init__(base_url, open_base_url)

    """Locators"""

    close_popup_button = ("//button[@class='ui-button ui-corner-all ui-widget "
                          "ui-button-icon-only ui-dialog-titlebar-close']")
    shop_now_button = "(//img[@class=' lazyloaded'])[1]"

    """Methods"""
