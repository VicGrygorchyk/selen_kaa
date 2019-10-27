import time
from typing import Callable

from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from se_wrapper import help_utils
from se_wrapper.element.wrapped_element_interface import WrappedElementInterface


TimeoutType = help_utils.TimeoutType
ElementType = help_utils.ElementType
DEFAULT_TIMEOUT = help_utils.DEFAULT_TIMEOUT


class Wait:

    def __init__(self, webdriver: WebDriver):
        self._webdriver: WebDriver = webdriver

    def element_be_in_dom(self, selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        if not isinstance(selector, str):
            raise TypeError("Selector should be a string for `element_be_in_dom()` method.")
        return self._set_condition_for_wait(selector, ec.presence_of_element_located, timeout)

    def element_to_be_visible(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        return self._switch_on_element_type(
            target,
            string=self._set_condition_for_wait(target, ec.visibility_of_element_located, timeout),
            web_element_type=self._wait_until(ec.visibility_of(target), timeout),
            wrapped_element_type=self._wait_until(ec.visibility_of(target.web_element), timeout)
        )

    def element_to_disappear(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """True if the element is not present and/or not visible.
        True if element is not visible, but it's still present in DOM.
        """

        def wrapped_webelement_disappears():
            try:
                if target.web_element.is_displayed():
                    return False
                return True
            except (NoSuchElementException, StaleElementReferenceException):
                return True

        return self._switch_on_element_type(
            target,
            string=self._set_condition_for_wait(target, ec.invisibility_of_element_located, timeout),
            web_element_type=self._wait_until(ec.invisibility_of_element(target), timeout),
            wrapped_element_type=self.wait_fluently(
                wrapped_webelement_disappears,
                timeout,
                f"TimeoutException while waited {timeout} for the element {target.selector} to disappear."
            )
        )

    def no_element_in_dom(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """If NoSuchElementException or StaleElementReferenceException
        it's legit result for this condition.

        """

        def no_wrapped_webelement_in_dom():
            try:
                if target.web_element:
                    return False
            except (NoSuchElementException, StaleElementReferenceException):
                return True

        try:
            return self._switch_on_element_type(
                target,
                string=self._set_condition_for_wait(target, ec.invisibility_of_element_located, timeout),
                web_element_type=self._wait_until(ec.staleness_of(target), timeout),
                wrapped_element_type=self.wait_fluently(
                    no_wrapped_webelement_in_dom,
                    timeout,
                    f"TimeoutException while waited {timeout} for the element {target.selector} "
                    f"to not be present in DOM."
                )
            )
        except (NoSuchElementException, StaleElementReferenceException):
            return True

    def element_to_contain_text(self, target: ElementType, text: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        return self._switch_on_element_type(
            target,
            string=self._wait_until(
                ec.text_to_be_present_in_element((help_utils.get_selector_type(target), target), text),
                timeout
            ),
            web_element_type=self._wait_until(lambda: text in target.text, timeout),
            wrapped_element_type=self._wait_until(lambda: text in target.web_element.text, timeout)
        )

    def element_have_similar_text(self, target: ElementType,
                                  expected_text: str,
                                  timeout: TimeoutType = DEFAULT_TIMEOUT):
        """ Wait until web element contains expected text.
        Returns True if similar text.
        This method is different from `wait_element_to_contain_text`,
        as it ignores whitespaces, newtabs, cases for similarity comparision.
        """
        if isinstance(target, str):
            selector_type = help_utils.get_selector_type(target)
            element = self._webdriver.find_element(by=selector_type, value=target)
        elif isinstance(target, WebElement):
            element = target
        else:
            element = target.web_element
        text_ = None

        def get_text_in_element():
            """Func to check if element contains similar text. """
            nonlocal text_
            nonlocal element
            if text_ is None:
                text_ = element.text
            element_text = element.text
            if element_text == expected_text:
                return element
            if expected_text.lower() == element_text.lower():
                return element
            if "".join(expected_text.split()) == "".join(element_text.split()):
                return element
            return None

        try:
            return self._wait_until(get_text_in_element, timeout)
        except TimeoutException as exc:
            raise TimeoutException(
                msg=f"Waited {timeout} seconds for text {expected_text}. Got {text_}\n{exc.msg}"
            )

    def element_to_get_class(self, target: ElementType,
                             expected_class: str,
                             timeout: TimeoutType = DEFAULT_TIMEOUT):
        """ Wait until web element gets expected class """

        if isinstance(target, str):
            selector_type = help_utils.get_selector_type(target)
            element = self._webdriver.find_element(by=selector_type, value=target)
        elif isinstance(target, WebElement):
            element = target
        else:
            element = target.web_element
        class_not_expected = None

        def check_class_in_element():
            """Func to check if class is present in element.
            Driver is passed by Selenium wait() method.
            """
            nonlocal class_not_expected
            result = []
            expected_class_ls = expected_class.split(" ")
            actual_class = element.get_attribute("class")
            for class_ in expected_class_ls:
                for element_class_ in actual_class.split(" "):
                    if element_class_ == class_:
                        result.append(element)
            if len(result) == len(expected_class_ls):
                return element
            if class_not_expected is None:
                class_not_expected = actual_class
            return None

        try:
            return self._wait_until(check_class_in_element, timeout)
        except TimeoutException as exc:
            raise TimeoutException(msg=f"Waited {timeout} seconds for class {expected_class}. "
                                       f"Got {class_not_expected}\n{exc.msg}")

    def url_to_contain(self, expected_url: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """ Wait until webdriver gets expected url. """
        error_url = None

        def get_url(driver):
            if expected_url in str(driver.current_url):
                return True
            nonlocal error_url
            error_url = driver.current_url
            return None

        try:
            return self._wait_until(get_url, timeout)
        except TimeoutException as exc:
            raise TimeoutException(msg=f"Waited {timeout} seconds for url {expected_url}. "
                                   f"Got {error_url}\n{exc.msg}")

    def page_title_contains(self, title: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait for page title contains a specific string."""
        return self._wait_until(condition=ec.title_contains(title), timeout=timeout)

    def _wait_until(self, condition, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wrapper method around Selenium WebDriverWait() with until().
        :param condition: Selenium expected_condtions
        :param timeout: int
        :return: boolean
        """
        return wait.WebDriverWait(self._webdriver, timeout).until(condition)

    def _set_condition_for_wait(self, selector, condition, timeout):
        by_ = help_utils.get_selector_type(selector)
        return self._wait_until(condition((by_, selector)), timeout)

    @staticmethod
    def _switch_on_element_type(target, string, web_element_type, wrapped_element_type):
        """Strategy for target object, which can be str aka css selector,
        Selenium WebElement or WrappedWebElement.

        """
        if isinstance(target, WrappedElementInterface):
            func = wrapped_element_type
        else:
            switch = {
                "str": string,
                "WebElement": web_element_type
            }
            func = switch.get(target.__class__.__name__, None)
            if not func:
                raise TypeError("Target shall be an instance of string, WebElement or WebElementWrapper.")
        return func()

    @staticmethod
    def wait_fluently(condition: Callable, timeout: TimeoutType, err_msg: str):
        """Custom wait for special cases.
        :param condition: function to verify if Condition is True
        :param timeout: time to wait for positive condition.
        :param err_msg: error message
        :return: True if condition, else raises TimeoutException

        """
        start_time = time.time()
        while True:
            if time.time() - start_time >= timeout:
                raise TimeoutException(err_msg)
            if condition:
                return True
            time.sleep(0.3)
