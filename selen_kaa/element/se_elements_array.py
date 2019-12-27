from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from selen_kaa.utils.se_utils import get_selector_type
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located
from selen_kaa.utils import custom_types
from selen_kaa.element.se_web_element import SeWebElement


TimeoutType = custom_types.TimeoutType


class SeElementsArray:
    """Lazy initialization of a list of web_elements.
    We need this for calling a list of wrapped web_elements,
    instead of standard find_elements().
    """

    DEFAULT_TIMEOUT = 4

    def __init__(self, webdriver: WebDriver, css_selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        self._webdriver = webdriver
        self._css_selector = css_selector
        self._timeout = timeout
        self._elements_array = []

    @property
    def _lazy_array(self):
        if not self._elements_array:
            elements_ = WebDriverWait(self._webdriver, self._timeout).until(
                presence_of_all_elements_located((get_selector_type(self.selector), self.selector))
            )
            for elem in elements_:
                wrapped_elem = SeWebElement(self._webdriver, self._css_selector, self._timeout)
                wrapped_elem.web_element = elem
                self._elements_array.append(wrapped_elem)

        return self._elements_array

    def __getattr__(self, attr):
        try:
            orig_attr = self._lazy_array.__getattribute__(attr)
            if callable(orig_attr):
                def hooked(*args, **kwargs):
                    return orig_attr(*args, **kwargs)
                return hooked
            return orig_attr
        except AttributeError as exc:
            raise AttributeError(f"No attribute {attr}.\n{exc}")

    def __getitem__(self, index):
        return self._lazy_array[index]

    def __len__(self):
        return len(self._lazy_array)
