A lightweight wrapper around Selenium Python.<br/>
It's a simple extension to standard Selenium.
We believe we should use standard Selenium, when it works, and use additional methods, 
when Selenium annoys, mainly with waits.

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
element = browser.find_element_by_css(".test-class")
```
Besides standard Selenium, `selen-kaa` introduces more convenient way to 
interact with a web page and web elements through `init_web_element()`
and `init_all_web_elements()`:<br/>
- you can freely create the web element in `__init__()`, as the WebDriver 
would search this element 
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
browser.get("www.some.com")
page.element1.click() # WebDriver would `find_element` and click it only on this step
```
<br/>

`init_web_element()` returns `SeWebElement` object, which has attributes 
of standard WebElement but with additional logic of lazy initialization,
 custom waits and conditions.
`init_all_web_elements()` returns `SeElementsArray` - a collection of 
`SeWebElement` objects with the same lazy initialization logic.

```
element1 = browser.init_web_element("#test")
element1.should.be_visible(timeout=4) # wait 4 seconds until element becomes visible

elements = browser.init_all_web_elements(".test-class")
elements[0].should.have_exact_text(text="first element", timeout=4)
```

You may override `init_web_element` and `init_all_web_elements` with 
to implement additional logic:
```
class MySeWebElement(SeWebElement):
    pass

class MySeElementsArray(SeElementsArray):
    pass

class DriverWrapper(SeWebDriver):

    def init_web_element(self, selector: str, timeout: TimeoutType = 1):
        return MySeWebElement(self.webdriver, selector, timeout)

    def init_all_web_elements(self, selector: str, timeout: TimeoutType = None):
        arr = super().init_all_web_elements(selector, timeout)
        arr.element_type = MySeWebElement
        return arr
```
Pay attention, that you can change a type of element in 
`SeElementsArray` by assigning a value to `element_type` property of 
`SeElementsArray`.
