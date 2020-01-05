import pytest
from selenium.webdriver.common.by import By


from selen_kaa.utils import se_utils


@pytest.mark.parametrize("selector", ("div", ".class", "div[class='test']",
                                      "img[class^='irc_mut'][src^='http']"))
def test_css_selector(selector):
    assert se_utils.get_selector_type(selector) == By.CSS_SELECTOR


@pytest.mark.parametrize("selector", (
    "//div", "./div/div/.class",
    "//div[@id='rso']//div[@class='test tttest']//a[contains(@href, '/imgres')]",
    "/html//div[contains(text(), 'The page')]",
    "/bookstore/book[price>35.00]/title"
))
def test_xpath_selector(selector):
    assert se_utils.get_selector_type(selector) == By.XPATH
