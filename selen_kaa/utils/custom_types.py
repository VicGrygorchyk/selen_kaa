from typing import Union

from selenium.webdriver.remote.webelement import WebElement
from selen_kaa.element.se_element_interface import SeElementInterface


ElementType = Union[str, WebElement, SeElementInterface]
TimeoutType = Union[int, float, None]
