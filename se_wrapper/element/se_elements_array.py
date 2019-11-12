from selenium.webdriver.remote.webdriver import WebDriver

from se_wrapper.utils import se_utils
from se_wrapper.utils import custom_types


TimeoutType = custom_types.TimeoutType


class SeElementsArray:
    """Lazy initialization of a list of web_elements.
    We need this for calling a list of wrapped web_elements,
    instead of standard find_elements().
    """

    DEFAULT_TIMEOUT = 4

    def __init__(self, webdriver: WebDriver, css_selector: str,
                 WrappedElementType: type, timeout: TimeoutType = DEFAULT_TIMEOUT):
        self._webdriver = webdriver
        self._css_selector = css_selector
        self._timeout = timeout
        self._elements_array = None
        self.WrappedElementType = WrappedElementType

    @property
    def lazy_array(self):
        if not self._elements_array:
            self._elements_array = se_utils.find_all_elements_by_css(self._webdriver,
                                                                     self._css_selector,
                                                                     self._timeout)
        return self._elements_array

    def __getitem__(self, index):
        element = self.WrappedElementType(self._webdriver, self._css_selector, self._timeout)
        element.web_element = self._elements_array[index]
        return self._elements_array[index]
