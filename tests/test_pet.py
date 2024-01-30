import time
from pages.AccountPage import AccountPage
from pages.CatalogPage import CatalogPage
from pages.CheckoutPage import CheckoutPage
from pages.MainPage import MainPage
from pages.ProductPage import ProductPage
from pages.ShoppingCartPage import ShoppingCartPage
import allure


@allure.description("Test smoke for standard user")
def test_smoke_for_standard_user(login, clear_cart, clear_input_field, logout):

    """Data for test"""
    #  python -m pytest --alluredir=test_result/ tests/test_pet.py # command for start test with allure
    #  allure serve test_result/ # command for create allure report
    num_on_page_product_1 = "3"
    num_on_page_product_2 = "5"
    quantity_product_1 = "1"
    quantity_product_2 = "8"

    """Go to catalog page"""

    lp = AccountPage()
    lp.click(xpath=lp.fila_logo_button, description="fila logo", scroll=False, next_page=True)

    mp = MainPage()
    mp.click(xpath=mp.close_popup_button, description="close popup")
    mp.click(xpath=mp.shop_now_button, description="shop now", next_page=True)

    """Add first product & save data product"""

    cp = CatalogPage()
    cp.click(xpath=cp.accept_button, description="accept")
    data_product = cp.quick_add(product_on_page_num=num_on_page_product_1)
    name_1 = data_product[0]
    price_1 = data_product[1]
    size_1 = data_product[3]
    promo_text_1 = data_product[6]

    """Go to men boots page & select second product"""

    cp.move_to_element(xpath=cp.men, description="men", scroll=False)
    cp.click(xpath=cp.boots, description="boots", next_page=True)
    data_product = cp.get_product_data(product_on_page_num=num_on_page_product_2)
    name_2 = data_product[0]
    price_2 = data_product[1]
    product_button_2 = data_product[2]
    cp.click(xpath=product_button_2, description="product", next_page=True)

    """Add second product & save data product'"""

    pp = ProductPage()
    pp.check_name_price(name=name_2, price=price_2)
    pp.select_color()
    time.sleep(2)
    size_2 = pp.select_size()
    time.sleep(2)
    pp.clear_field(xpath=pp.quantity_product_field)
    pp.send_keys(keys=quantity_product_2, xpath=pp.quantity_product_field)
    pp.click(xpath=pp.add_to_cart_button, description="add to cart")

    """Check second product in popup window'"""

    pp.check_product_window(name=name_2, quantity_product=quantity_product_2, size=size_2, price=price_2)

    """Check all product in mini cart'"""

    pp.move_to_element(xpath=pp.mini_cart, description="mini cart")
    pp.move_to_element(xpath=pp.mini_cart_view_shopping_bag, description="view shopping bag")
    pp.check_mini_cart(name=name_1, quantity=quantity_product_1, price=price_1, size=size_1, num=2)
    pp.check_mini_cart(name=name_2, quantity=quantity_product_2, price=price_2, size=size_2, num=1)
    num_1 = pp.price_in_float(price=price_1)
    num_2 = pp.price_in_float(price=price_2)
    total_price = num_1 * float(quantity_product_1) + num_2 * float(quantity_product_2)
    total_price = pp.float_in_price(total_price)
    pp.assert_word(word=total_price, xpath=pp.mini_cart_subtotal, description_text="subtotal")

    """Go to shopping bag page & check all product"""

    pp.click(xpath=pp.mini_cart_view_shopping_bag, description='shopping bag', next_page=True)
    scp = ShoppingCartPage()
    error = scp.check_limited()
    if error:
        scp.limited_fix()
        quantity_product_2 = "1"
        total_price = num_1 * float(quantity_product_1) + num_2 * float(quantity_product_2)
        total_price = pp.float_in_price(total_price)
    subtotal_1 = scp.check_product(name=name_1, price=price_1, size=size_1, quantity=quantity_product_1, num=1,
                                   promo=promo_text_1)
    subtotal_2 = scp.check_product(name=name_2, price=price_2, size=size_2, quantity=quantity_product_2, num=2)
    subtotal_1 = scp.price_in_float(price=subtotal_1)
    subtotal_2 = scp.price_in_float(price=subtotal_2)
    total_cart_price = subtotal_1 + subtotal_2
    total_cart_price = scp.float_in_price(total_cart_price)
    assert total_price == total_cart_price
    scp.assert_word(word=total_cart_price, xpath=scp.total, description_text="total")

    """Go to checkout page & check all product"""

    scp.click(xpath=scp.checkout, description="checkout", next_page=True)
    chp = CheckoutPage()
    chp.check_product(name=name_1, price=price_1, size=size_1, quantity=quantity_product_1, num=1,
                      promo=promo_text_1)
    chp.check_product(name=name_2, price=price_2, size=size_2, quantity=quantity_product_2, num=2)
    chp.assert_word(word=total_cart_price, xpath=chp.check_total, description_text="total")

    """Input buyer data"""

    chp.send_keys(keys="Nikita", xpath=chp.first_name_field, description="First Name")
    chp.send_keys(keys="Chelovian", xpath=chp.last_name_field, description="Last Name")
    chp.send_keys(keys="Roosevelt Row", xpath=chp.street_field, description="Street Address")
    chp.send_keys(keys="5 apartment, 4 floor", xpath=chp.apt_floor_field, description="Apt., Suite, Floor (Optional)")
    chp.send_keys(keys="85323", xpath=chp.zip_field, description="Zip Code")
    chp.send_keys(keys="6025553890", xpath=chp.phone_field, description="Phone Number")
    chp.click(xpath=chp.state_drop_down, description="state dropdown")
    chp.click(xpath=chp.arizona_drop_down, description="arizona dropdown")
    time.sleep(1)
    chp.clear_field(xpath=chp.city_field, description="City")
    chp.send_keys(keys="Phoenix", xpath=chp.city_field, description="City")

    """Check clickable button continue & finish test"""

    chp.select_clickable(xpath=chp.continue_button, description="continue")
    chp.get_screenshot()
    print("Success, Test smoke for standard user")
