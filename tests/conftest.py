import pytest
from pages.AccountPage import AccountPage
from pages.CheckoutPage import CheckoutPage
from pages.ShoppingCartPage import ShoppingCartPage


@pytest.fixture(scope='module')
def login():
    lp = AccountPage(True)
    lp.log_in()


@pytest.fixture(scope='module')
def logout():
    yield
    lp = AccountPage(True)
    lp.log_out()


@pytest.fixture(scope='function')
def clear_input_field():
    yield
    chp = CheckoutPage()
    chp.clear_all_field()


@pytest.fixture(scope='function')
def clear_cart():
    yield
    scp = ShoppingCartPage(True)
    scp.clear_cart()
