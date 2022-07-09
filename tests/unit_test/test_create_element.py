import pytest

from selenium.webdriver.common.by import By

from selen_kaa.element.se_web_element import SeWebElement
from selen_kaa.element.se_elements_array import SeElementsArray


@pytest.mark.parametrize("selector", ("div", ".class", "div[class='test']",
                                      "img[class^='irc_mut'][src^='http']"))
def test_create_se_web_element_by_css(selector):
    element = SeWebElement(None, selector)
    assert element.locator_strategy == By.CSS_SELECTOR


@pytest.mark.parametrize("selector", (
    "//div", "./div/div/.class",
    "//div[@id='rso']//div[@class='test tttest']//a[contains(@href, '/imgres')]",
    "/html//div[contains(text(), 'The page')]",
    "/bookstore/book[price>35.00]/title"
))
def test_create_se_web_element_by_xpath(selector):
    element = SeWebElement(None, selector)
    assert element.locator_strategy == By.XPATH


@pytest.mark.parametrize("param", (
    ("class-name", By.CLASS_NAME),
    ("img", By.TAG_NAME),
    ('**/XCUIElementTypeImage[`label == "test"`]', 'MobileBy.IOS_CLASS_CHAIN')
))
def test_create_se_web_element_by_custom_locator_strategy(param):
    selector, locator_strat = param
    element = SeWebElement(None, selector, locator_strategy=locator_strat)
    assert element.locator_strategy == locator_strat


@pytest.mark.parametrize("selector", ("div", ".class", "div[class='test']",
                                      "img[class^='irc_mut'][src^='http']"))
def test_create_web_element_arr_by_css(selector):
    elements = SeElementsArray(None, selector)
    assert elements.locator_strategy == By.CSS_SELECTOR


@pytest.mark.parametrize("selector", (
    "//div", "./div/div/.class",
    "//div[@id='rso']//div[@class='test tttest']//a[contains(@href, '/imgres')]",
    "/html//div[contains(text(), 'The page')]",
    "/bookstore/book[price>35.00]/title"
))
def test_create_se_web_element_arr_by_xpath(selector):
    elements = SeElementsArray(None, selector)
    assert elements.locator_strategy == By.XPATH


@pytest.mark.parametrize("param", (
    ("class-name", By.CLASS_NAME),
    ("img", By.TAG_NAME),
    ('**/XCUIElementTypeImage[`label == "test"`]', 'MobileBy.IOS_CLASS_CHAIN')
))
def test_create_se_web_element_by_custom_locator_strategy(param):
    selector, locator_strat = param
    elements = SeElementsArray(None, selector, locator_strategy=locator_strat)
    assert elements.locator_strategy == locator_strat
