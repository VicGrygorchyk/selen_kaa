from se_wrapper.element.web_element_wrapper import WebElementWrapper


class WrappedWebElement(WebElementWrapper):
    """ Class is used to provide a lazy initialization of the WebElement.
    WebElement is going to be searched only when is called.
    So, web element can be declared in __init__ of the page class and be found only when needed for interaction.

    """

    def __init__(self, webdriver: DriverWrapper, selector, timeout=DEFAULT_TIMEOUT):
        self.webdriver = webdriver
        self.selector = selector
        self.timeout = timeout

    @property
    def web_element(self):
        try:
            return self.webdriver.find_element_by_selector(self.selector)
        except NoSuchElementException as exc:
            raise NoSuchElementException(f"Web Element with selector {self.selector} has not been found."
                                         f"\n{exc.msg}")

    def __getattr__(self, attr):
        """ Calls method or properties on self.web_element.
        Returns callable or attribute of WebElement.
        :param attr: any attr of the WebElement
        :return: Any

        """
        try:
            orig_attr = self.web_element.__getattribute__(attr)
            if callable(orig_attr):
                def hooked(*args, **kwargs):
                    return orig_attr(*args, **kwargs)
                return hooked
            return orig_attr
        except AttributeError as exc:
            raise AttributeError(f"WebElement has no attribute {attr}.\n{exc}")

    def should_be_displayed(self, timeout=None):
        """ Check for element to be visible on the html page.
        :param timeout:
        :return: boolean
        """
        timeout_ = timeout if timeout else self.timeout
        return self.webdriver.wait_element_to_appear(self.selector, timeout=timeout_)

    def should_have_class(self, expected_class: str, timeout=None):
        """ Check for element to have a specific class.
        :param expected_class: class_name for expected class (not css_selector).
        :param timeout: how long to wait for condition.
        :return: boolean
        """
        timeout_ = timeout if timeout else self.timeout
        try:
            return self.webdriver.wait_element_to_get_class(self.selector, expected_class, timeout=timeout_)
        except TimeoutException:
            return False

    def should_have_element(self, child_selector, timeout=None):
        """
        Wait until web_element get a desired child element.
        :param child_selector: str
        :param timeout: int
        :return: bool.
        """
        timeout_ = timeout if timeout else self.timeout
        result = False
        try:
            if self.webdriver.wait_element_be_in_dom(child_selector, timeout=timeout_):
                if self.find_element(by=self.webdriver.get_selector_type(child_selector), value=child_selector):
                    result = True
            return result
        except TimeoutException:
            raise TimeoutException(msg=f"{self.selector} has no element with locator='{child_selector}'")

    def should_contain_text(self, text: str, timeout=None):
        """ Checks element has provided text in texts attribute.
        Not precise comparision, e.g. returns True for:
        "some" in "this is some text", " test\n" and "test", "TEST" and "test"
        :param text: str
        :param timeout: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        return self.webdriver.wait_element_have_similar_text(self.selector, text, timeout=timeout_)

    def should_have_exact_text(self, text: str, timeout=None):
        """ Checks element has exactly provided text, and no other text.
        Precise comparision, e.g. returns False if "some" == "this is some text"
        :param text: str
        :param timeout: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        if self.webdriver.wait_element_to_contain_text(self.selector, text, timeout=timeout_):
            return self.webdriver.find_element_by_selector(self.selector).text == text
        return False

    def should_be_stale(self, timeout=None):
        """ Check for web element to be stale or absent on the html page.
        :param timeout: equal to the self.timeout if other not passed. :type: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        return self.webdriver.wait_element_staleness(self.selector, timeout=timeout_)

    def should_be_invisible(self, timeout=None):
        """ Check for web element to be invisible to the end user.
        :param timeout: equal to the self.timeout if other not passed. :type: int
        :return: boolean
        """
        timeout_ = self.timeout
        if timeout:
            timeout_ = timeout
        return self.webdriver.wait_element_invisibility(self.selector, timeout=timeout_)

    def set_text_value(self, text):
        """ Clears the input area before sending a new text key. """
        self.web_element.clear()
        self.web_element.send_keys(text)

    def double_click(self):
        """ Don't want to do double click with ActionChains -) """
        self.web_element.click()
        self.web_element.click()

    def click(self, timeout=DEFAULT_TIMEOUT):
        """ Click element, throws ElementNotClickableException if element can't handle click.
        Wait with timeout, if click is not possible.
        """
        start_time = time.time()
        while True:
            try:
                self.web_element.click()
                break
            except WebDriverException as exc:
                if ElementNotClickableError.can_handle_exception(exc):
                    if time.time() - start_time > timeout:
                        error = f"Element location is {self.web_element.location}. {exc.msg}"
                        raise ElementNotClickableError(msg=error)
                    continue
                else:
                    raise WebDriverException(msg=exc.msg)

    def get_class(self):
        """Get class of element """
        return self.web_element.get_attribute("class")
