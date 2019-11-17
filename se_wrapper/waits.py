import time
from typing import Callable

from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException

from se_wrapper.utils import se_utils
from se_wrapper.element.se_element_interface import SeElementInterface
from se_wrapper.utils import custom_types


TimeoutType = custom_types.TimeoutType
ElementType = custom_types.ElementType


class Wait:

    DEFAULT_TIMEOUT = 4

    def __init__(self, webdriver: WebDriver):
        self._webdriver: WebDriver = webdriver

    def element_be_in_dom(self, selector: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        if not isinstance(selector, str):
            raise TypeError("Selector should be a string for `element_be_in_dom()` method.")
        return self._set_condition_for_wait(selector, ec.presence_of_element_located, timeout)

    def element_to_be_visible(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):

        def wrapped_visible():
            target.get_web_element_by_timeout(timeout)
            return target if target.is_displayed() else False

        return self._switch_on_element_type(
            target,
            string=lambda: self._set_condition_for_wait(target, ec.visibility_of_element_located, timeout),
            web_element_type=lambda: self._wait_until(ec.visibility_of(target), timeout),
            wrapped_element_type=lambda: self.wait_fluently(
                wrapped_visible, timeout,
                f"TimeoutException while waited {timeout} for the element '{target.selector}' to be visible."
            )
        )

    def element_to_be_invisible(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """True if the element is not present and/or not visible.
        Difference from `element_not_present`: returns True if element is not visible,
        but it's still present in DOM.
        """

        def wrapped_webelement_disappears():
            try:
                # init web_element within wait's timeout, not web_element's
                target.get_web_element_by_timeout(timeout)
                if target.web_element.is_displayed():
                    return False
                # return True if element is not stale, but is not displayed
                return target
            except (NoSuchElementException, StaleElementReferenceException):
                return target

        return self._switch_on_element_type(
            target,
            string=lambda: self._set_condition_for_wait(target, ec.invisibility_of_element_located, timeout),
            web_element_type=lambda: self._wait_until(ec.invisibility_of_element(target), timeout),
            wrapped_element_type=lambda: self.wait_fluently(
                wrapped_webelement_disappears,
                timeout,
                f"TimeoutException while waited {timeout} for the element '{target.selector}' to disappear."
            )
        )

    def element_not_present(self, target: ElementType, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """True if there is no NoSuchElementException or StaleElementReferenceException.

        """

        def no_wrapped_webelement_in_dom():
            try:
                target.get_web_element_by_timeout(timeout)
                if target.web_element.is_enabled():
                    return False
                # it might be unreached condition, but keep it for code consistency
                return target
            except (NoSuchElementException, StaleElementReferenceException):
                return target

        try:
            return self._switch_on_element_type(
                target,
                string=lambda: self._set_condition_for_wait(target, ec.invisibility_of_element_located, timeout),
                web_element_type=lambda: self._wait_until(ec.staleness_of(target), timeout),
                wrapped_element_type=lambda: self.wait_fluently(
                    no_wrapped_webelement_in_dom,
                    timeout,
                    f"TimeoutException while waited {timeout} for the element '{target.selector}' "
                    f"to not be present in DOM."
                )
            )
        except (NoSuchElementException, StaleElementReferenceException):
            return True

    def element_to_contain_text(self, target: ElementType, text: str, timeout: TimeoutType = DEFAULT_TIMEOUT):

        def has_text_in_target():
            target.get_web_element_by_timeout(timeout)
            return target if text in target.text else False

        err_msg = f"TimeoutException while waited {timeout} for the element to contain text '{text}'. " \
                  f"Actual text '{target.text}'"

        return self._switch_on_element_type(
            target,
            string=lambda: self._wait_until(
                ec.text_to_be_present_in_element((se_utils.get_selector_type(target), target), text),
                timeout),
            web_element_type=lambda: self.wait_fluently(has_text_in_target, timeout, err_msg),
            wrapped_element_type=lambda: self.wait_fluently(has_text_in_target, timeout, err_msg)
        )

    def element_to_have_exact_text(self, target: ElementType, text: str,
                                   timeout: TimeoutType = DEFAULT_TIMEOUT):

        def has_exact_text_in_target():
            target.get_web_element_by_timeout(timeout)
            return target if text == target.text else False

        err_msg = f"TimeoutException while waited {timeout} for the element to have exact text '{text}'." \
                  f" Actual text '{target.text}'"

        return self._switch_on_element_type(
            target,
            string=lambda: self._wait_until(
                ec.text_to_be_present_in_element((se_utils.get_selector_type(target), target), text),
                timeout),
            web_element_type=lambda: self.wait_fluently(has_exact_text_in_target, timeout, err_msg),
            wrapped_element_type=lambda: self.wait_fluently(has_exact_text_in_target, timeout, err_msg)
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
            selector_type = se_utils.get_selector_type(target)
            element = self._webdriver.find_element(by=selector_type, value=target)
        elif isinstance(target, WebElement):
            element = target
        else:
            target.get_web_element_by_timeout(timeout)
            element = target
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
            return False

        return self.wait_fluently(get_text_in_element, timeout,
                                  f"TimeoutException while waited {timeout} for text '{expected_text}'. "
                                  f"Actual text is '{text_}'")

    def element_to_get_class(self, target: ElementType,
                             expected_class: str,
                             timeout: TimeoutType = DEFAULT_TIMEOUT):
        """ Wait until web element gets expected class """

        if isinstance(target, str):
            selector_type = se_utils.get_selector_type(target)
            element = self._webdriver.find_element(by=selector_type, value=target)
        elif isinstance(target, WebElement):
            element = target
        else:
            target.get_web_element_by_timeout(timeout)
            element = target
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
            return False

        return self.wait_fluently(check_class_in_element, timeout,
                                  f"TimeoutException while waited  {timeout} for class '{expected_class}'. "
                                  f"Actual class is '{class_not_expected}'.")

    def url_to_contain(self, expected_url: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """ Wait until webdriver gets expected url. """
        error_url = None

        def get_url(driver):
            if expected_url in str(driver.current_url):
                return True
            nonlocal error_url
            error_url = driver.current_url
            return False

        try:
            return self._wait_until(get_url, timeout)
        except TimeoutException as exc:
            raise TimeoutException(msg=f"TimeoutException while waited {timeout} for url '{expected_url}'. "
                                       f"Got '{error_url}'.\n{exc.msg}")

    def page_title_contains(self, title: str, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait for page's title to contain a specific string."""
        return self._wait_until(condition=ec.title_contains(title), timeout=timeout)

    def element_to_include_child_element(self, target: ElementType,
                                         child_css_selector,
                                         timeout: TimeoutType):
        """Wait for a web element to have another web element as a child element."""

        def nested(web_element):
            try:
                return web_element.find_element(by=se_utils.get_selector_type(child_css_selector),
                                                value=child_css_selector)
            except NoSuchElementException:
                return False

        webelement_ = target
        if isinstance(target, str):
            self.element_be_in_dom(target)
            webelement_ = self._webdriver.find_element(by=se_utils.get_selector_type(target),
                                                       value=target)
        elif isinstance(target, WebElement):
            webelement_ = target
        else:
            target.get_web_element_by_timeout(timeout)
            webelement_ = target

        return self.wait_fluently(lambda: nested(webelement_),
                                  timeout,
                                  f"TimeoutException while waiting for the element "
                                  f"to have a child '{child_css_selector}'.")

    def element_to_be_in_viewport(self, target, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wait until element inside viewport's coordinates."""
        find_viewport_pos_script = """
              var height = document.documentElement.clientHeight;
              var width = document.documentElement.clientWidth;
              var arr = [height, width];
              return arr;
          """
        rect_ = self._webdriver.execute_script(find_viewport_pos_script)
        height = rect_[0]
        width = rect_[1]

        if isinstance(target, str):
            self.element_be_in_dom(target)
            webelement_ = self._webdriver.find_element(by=se_utils.get_selector_type(target),
                                                       value=target)
        elif isinstance(target, WebElement):
            webelement_ = target
        else:
            target.get_web_element_by_timeout(timeout)
            webelement_ = target

        def get_element_pos():

            nonlocal height, width, webelement_
            pos_x = webelement_.location.get('x')
            pos_y = webelement_.location.get('y')
            if all((pos_x < width, pos_y < height)):
                return webelement_
            return None

        return self.wait_fluently(get_element_pos,
                                  timeout,
                                  f"TimeoutException while waiting {timeout} sec for element "
                                  f"to be in viewport.")

    def _wait_until(self, condition, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wrapper method around Selenium WebDriverWait() with until().
        :param condition: Selenium expected_condtions
        :param timeout: int
        :return: boolean
        """
        if not timeout:
            timeout = 0
        return wait.WebDriverWait(self._webdriver, timeout).until(condition)

    def _wait_until_not(self, condition, timeout: TimeoutType = DEFAULT_TIMEOUT):
        """Wrapper method around Selenium WebDriverWait() with until_not().
        :param condition: Selenium expected_conditions
        :param timeout: int
        :return: boolean
        """
        if not timeout:
            timeout = 0
        return wait.WebDriverWait(self._webdriver, timeout).until_not(condition)

    def _set_condition_for_wait(self, selector, condition, timeout):
        by_ = se_utils.get_selector_type(selector)
        if not timeout:
            timeout = 0
        return self._wait_until(condition((by_, selector)), timeout)

    @staticmethod
    def _switch_on_element_type(target, string, web_element_type, wrapped_element_type):
        """Strategy for target object, which can be str aka css selector,
        Selenium WebElement or WrappedWebElement.

        """
        if isinstance(target, SeElementInterface):
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
        """Custom wait for special cases where driver is not needed as arg for condition.
        :param condition: function to verify if Condition is True
        :param timeout: time to wait for positive condition.
        :param err_msg: error message
        :return: element if condition is True, else raises TimeoutException

        """
        if not timeout:
            timeout = 0
        start_time = time.time()
        while True:
            if time.time() - start_time >= timeout:
                raise TimeoutException(err_msg)
            res = condition()
            if res:
                return res
            time.sleep(0.3)
