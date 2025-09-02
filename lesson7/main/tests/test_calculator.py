# PR placeholder: ничего не меняем, просто для отображения изменений2
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.calculator_page import CalculatorPage


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_addition_with_delay(driver):
    calc = CalculatorPage(driver)

    # 1. Открыть страницу
    calc.open()

    # 2. Установить задержку 45 секунд
    calc.set_delay("45")

    # 3. Нажать 7 + 8 =
    calc.click_button("7")
    calc.click_button("+")
    calc.click_button("8")
    calc.click_button("=")

    # 4. Ждём появления результата "15"
    WebDriverWait(driver, 50).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
    )

    # 5. Проверка
    assert calc.get_result() == "15"
