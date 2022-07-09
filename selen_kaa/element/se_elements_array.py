from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located

from selen_kaa.utils.se_utils import get_selector_type
from selen_kaa.utils import custom_types

TimeoutType = custom_types.TimeoutType


class SeElementsArray:
    """Lazy initialization of a list of web_elements.
    We need this for calling a list of wrapped web_elements,
    instead of standard find_elements().
    """

    DEFAULT_TIMEOUT = 4

    def __init__(self,
                 webdriver: WebDriver,
                 selector: str,
                 timeout: TimeoutType = DEFAULT_TIMEOUT,
                 locator_strategy: Optional[str] = None):
        self._webdriver = webdriver
        self._selector = selector
        self._timeout = timeout
        self._elements_array = []
        self._element_type = None
        self.locator_strategy = locator_strategy if locator_strategy else get_selector_type(self._selector)

    @property
    def element_type(self):
        if self._element_type is None:
            raise AttributeError("Type of element in SeElementsArray is None. "
                                 "Probably, you forgot to assign an element_type.")
        return self._element_type

    @element_type.setter
    def element_type(self, web_element_type):
        self._element_type = web_element_type

    @property
    def _lazy_array(self):
        if len(self._elements_array) < 1:
            try:
                elements_ = WebDriverWait(self._webdriver, self._timeout).until(
                    presence_of_all_elements_located((self.locator_strategy, self._selector))
                )
            except TimeoutException:
                # return empty array if no element is present on the page
                return []

            for elem in elements_:
                wrapped_elem = self._element_type(
                    self._webdriver, self._selector, self._timeout, self.locator_strategy
                )
                wrapped_elem.web_element = elem
                self._elements_array.append(wrapped_elem)

        return self._elements_array

    def __getattr__(self, attr):
        try:
            orig_attr = self._lazy_array.__getattribute__(attr)
            if callable(orig_attr):
                def hooked(*args, **kwargs):
                    # prevent recursion
                    result = orig_attr(*args, **kwargs)
                    # prevent recursion
                    if result == self._lazy_array:
                        return self
                    return result

                return hooked
            return orig_attr
        except AttributeError as exc:
            raise AttributeError(f"No attribute {attr}.\n{exc}")

    def __getitem__(self, index):
        return self._lazy_array[index]

    def __len__(self):
        return len(self._lazy_array)
