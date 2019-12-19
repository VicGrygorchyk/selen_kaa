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
        self._elements_array = []
        self._WrappedElementType = WrappedElementType

    @property
    def _lazy_array(self):
        if not self._elements_array:
            elements_ = se_utils.find_all_elements_by_css(self._webdriver,
                                                          self._css_selector,
                                                          self._timeout)
            for elem in elements_:
                wrapped_elem = self._WrappedElementType(self._webdriver,
                                                        self._css_selector,
                                                        self._timeout)
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
