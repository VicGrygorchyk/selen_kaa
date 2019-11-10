from se_wrapper.element.se_elements_array import SeElementsArray
from se_wrapper.element.se_web_element import SeWebElement


class WebDriverConfig:

    WrappedElementType: type = SeWebElement
    WrappedElementArrayType: type = SeElementsArray
    DEFAULT_TIMEOUT = 4
