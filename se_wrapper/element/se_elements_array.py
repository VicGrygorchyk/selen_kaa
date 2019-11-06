from se_wrapper.element.se_web_element import SeWebElement


class SeElementsArray:
    """Lazy initialization of a list of web_elements.
    We need this for calling a list of wrapped web_elements,
    instead of standard find_elements().
    """

    def __init__(self, webdriver, css_selector, timeout):
        self._webdriver = webdriver
        self._css_selector = css_selector
        self._timeout = timeout
        self._elements_array = None

    @property
    def lazy_array(self):
        if not self._elements_array:
            self._elements_array = self._webdriver.find_all_elements_by_css(self._css_selector)
        return self._elements_array

    def __getitem__(self, index):
        element = SeWebElement(self._webdriver, self._css_selector, self._timeout)
        element.web_element = self._elements_array[index]
        return self._elements_array[index]
