from base.base_page import BasePage


class AccountPage(BasePage):
    """Данные"""

    login = "for.share.test.mail@gmail.com"
    password = "87654321fstm"
    base_url = "https://www.fila.com/account"
    check_login_word = "Personal Info"
    check_logout_word = "Sign In"

    def __init__(self, open_base_url=False):
        """Запуск webdriver по заданному адресу"""
        base_url = self.base_url
        super().__init__(base_url, open_base_url)

    """Locators"""

    email_field = "(//input[@class='input-text email-input required'])[1]"
    password_field = "(//input[@class='input-text-pw password-input required'])[1]"
    remember_button = "//label[@for='dwfrm_login_rememberme']"
    login_button = "(//button[@name='dwfrm_login_login'] )[1]"
    check_field_login_word = "((//div[@class='grid-head'])/h3)[1]"
    check_field_logout_word = "(//div[@class='login-box login-account'])/h2"
    logout_button = "//a[@href='/on/demandware.store/Sites-FILA-Site/en_US/Login-Logout']"

    """Methods"""

    def log_in(self, login_inp=login, password_inp=password):
        print("Begin log-in")
        self.send_keys(keys=login_inp, xpath=self.email_field, description="email")
        self.send_keys(keys=password_inp, xpath=self.password_field, description="password")
        self.click(xpath=self.remember_button, description="remember")
        self.click(xpath=self.login_button, description="login")
        self.assert_word(word=self.check_login_word, xpath=self.check_field_login_word,
                         description_text="check_word")
        self.scroll_to_end(description="account")
        print("Log-in success")

    def log_out(self):
        print("Begin log-out")
        self.click(xpath=self.logout_button, description="log-out")
        self.assert_word(word=self.check_logout_word, xpath=self.check_field_logout_word,
                         description_text="check_word")
        print("Log-out success")
