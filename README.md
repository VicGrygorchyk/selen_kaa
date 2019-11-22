A lightweight wrapper around Selenium Python.<br/>
It's a simple extension to standard Selenium.
The Philosophy is "__don't reinvent a wheel and
use standard Selenium, when it works and fix it, 
when Selenium annoys, mainly with waits and
 NoSuchElement exception__".

## Short Features Overview:
- It is easy integrated with your existing Selenium code and
- It is compatible with any standard Selenium methods.
<br/>For instance:
```
# Your Selenium code
browser = webdriver.Chrome()
browser.get("https://www.seleniumhq.org/")

# with `selen-kaa`
from se_wrapper.browser_driver import BrowserDriver

browser = BrowserDriver(webdriver.Chrome())
browser.get("https://www.seleniumhq.org/")
# any methods from the WebDriver works!
```
- Besides standard Selenium, `selen-kaa` introduces more convenient way to 
interact with a web page and web elements through `init_web_element()`
and `init_web_elements()`: 
you can freely create the web element in `__init__()`, as the WebDriver would search this element 
only at the time of interaction with it:
```
browser = BrowserDriver(webdriver.Chrome())

class MyPage:

    def __init__():
        # lazy creation of a web element
        self.element1 = browser.init_web_element("#test")
    
page = MyPage()
# even if `self.element1` has not been rendered yet on the web page, 
# it's safe, you would have no NoSuchElementException
page.element1.click() # only here the WebDriver would `find_element`
```
`init_web_element()` returns a wrapper around Selenium
WebElement, what has all standard WebElement's methods, but
have two main advantages:
1) Wrapped WebElement is going to be searched only when
any method is called on it (as shown above).
2) It has its own waits methods:
```
element1 = browser.init_web_element("#test")
element1.should.be_visible(timeout=4) # wait 4 seconds for element to be visible
```

- `selen-kaa` is basically about next logic:
1) It has `BrowserDriver`, which allows to use all standard Selenium methods 
and attributes of the WebDriver, but has additional logic for 
`init_web_element()` and `init_web_elements()`.
2) `init_web_element` returns `SeWebElement` object, which has attributes 
of standard WebElement but with additional logic of lazy initialization,
 custom waits and conditions.
3) `init_web_elements()` returns `SeElementsArray` - a collection of 
`SeWebElement` objects with the same lazy initialization logic.

- This library is highly customisable for extensions:
```
class MyElementWrapper(SeWebElement):
    pass
    
class MyElementsArray(SeElementsArray):
    pass

class Config(WebDriverConfig):

    WrappedElementType = MyElementWrapper
    WrappedElementArrayType = MyElementsArray
    DEFAULT_TIMEOUT = DEFAULT_TIMEOUT


class MyDriverWrapper(BrowserDriver):

    def __init__(self, webdriver):
        super().__init__(webdriver)
        self.config = Config()
```
So, you can add your own methods to `selen-kaa` main classes.

###  