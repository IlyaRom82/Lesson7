# PR placeholder: ничего не меняем, просто для отображения изменений2
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage


@pytest.mark.saucedemo
def test_saucedemo_purchase():
    # Настройка драйвера Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Открываем сайт
        driver.get("https://www.saucedemo.com/")
        print("Открыли сайт:", driver.current_url)

        # Авторизация
        login_page = LoginPage(driver)
        login_page.enter_username("standard_user")
        login_page.enter_password("secret_sauce")
        login_page.click_login()
        print("После логина:", driver.current_url)

        # Ждём загрузки инвентаря
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
        )
        print("Инвентарь загружен:", driver.current_url)

        # Добавляем рюкзак в корзину (по data-test ID)
        add_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "add-to-cart-sauce-labs-backpack")
            )
        )
        add_button.click()
        print("Клик по Add to cart выполнен")

        # Проверяем, что кнопка сменилась на Remove
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "remove-sauce-labs-backpack")
            )
        )
        print("Товар успешно добавлен в корзину")

        # Переходим в корзину
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        print("Клик по иконке корзины:", driver.current_url)

        # Ждем открытия страницы корзины
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title"))
        )
        print("Корзина открыта:", driver.current_url)

        # Проверяем товар в корзине
        cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        print("Найден товар в корзине:", cart_item.text)
        assert cart_item.text == "Sauce Labs Backpack"

    finally:
        driver.quit()
