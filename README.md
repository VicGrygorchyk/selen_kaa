An lightweight extension to Selenium Python.<br/>
It's inspired by [Selenide](https://github.com/selenide/selenide "Selenide GitHub page") from Java world and 
obsolete [Selene](https://github.com/yashaka/selene "Selene Github page")

## Short Features Overview:
- **Selen-kaa** is easy integrated with your existing Selenium code, 
- **Sele-kaa** doesn't break any line of your existing project!
- **Selen-kaa** is compatible with any standard Selenium methods.
<br/>For instance:
```
# Your old Selenium code
browser = webdriver.Chrome()
browser.get("https://www.seleniumhq.org/")

# The same works with `selen-kaa`
from se_wrapper.webdriver import SeWebDriver

browser = BrowserDriver(webdriver.Chrome())  # wrap your browser to SeWebDriver 
browser.get("https://www.seleniumhq.org/")
# any methods from the WebDriver works!
element = browser.find_element_by_css(".test-class")
```
Besides standard Selenium, **Selen-kaa** introduces more convenient way to 
interact with a web page and web elements through `init_web_element()`
and `init_all_web_elements()`:<br/>
What it gives you? Possibility to create the web element in `__init__()` method of a Page Object, 
as the WebDriver would search this element only at the time of interaction with it:
```
browser = BrowserDriver(webdriver.Chrome())

class MyPage:

    def __init__():
        # lazy creation of a web element
        # it's safe, you would have no NoSuchElementException
        # even if `self.element1` has not been rendered yet on the web page, 
        self.element1 = browser.init_web_element("#test")
    
page = MyPage()
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
When `SeWebDriver` initializes a new `SeWebElement` it waits for the element 
with a default timeout (4 seconds), so you don't need to handle waits your self!

Use css selector or xpath for SeWebElement initialization:<br/>
__Valid__:<br/>
```
browser.init_web_element("#this_hashtag_for_id")
browser.init_web_element(".this-dor-for-class")
browser.init_web_element("button[class='my-button']")
browser.init_web_element("//div//a[contains(@href, '/imgres')]")
```
[About CSS selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors "Mozilla page")

### More handful methods
Wait for element with css selector ".test-class" to be visible.
Condition `should` raises Timeout exception if the element is not visible within `timeout`.
Condition `expect` returns True if the element is visible or False if it is not visible within `timeout`.
```python
browser = BrowserDriver(webdriver.Chrome())  # wrap your browser to SeWebDriver 
element = browser.init_web_element(".test-class")

element.should.be_visible(timeout)
element.expect.be_visible(timeout)
```
Wait for element with css selector ".test-class" to be invisible.
```python
element.should.be_invisible(timeout)
element.expect.be_invisible(timeout)
```
Wait for element with css selector ".test-class" to have class.
```python
element.should.have_class(expected_class, timeout)
element.expect.have_class(expected_class, timeout)
```
Wait for element with css selector ".test-class" to include another element with css or xpath selector.
```python
element.should.include_element(child_selector, timeout)
element.expect.include_element(child_selector, timeout)
```
Wait for element with css selector ".test-class" to contain a text.
`Contain` would be True for "text" in "this is fulltext."
```python
element.should.contain_text(text, timeout)
element.expect.contain_text(text, timeout)
```
Wait for element with css selector ".test-class" to have_similar_text.
Not precise comparision, e.g. returns True for:
"some" in "this is some text", " test\n" and "test", "TEST" and "test". 
Ignores whitespaces and is case insensitive.
```python
element.should.have_similar_text(text, timeout)
element.expect.have_similar_text(text, timeout)
```
Wait for element with css selector ".test-class" to have exact text.
Strict comparision "text == text"
```python
element.should.have_exact_text(text, timeout)
element.expect.have_exact_text(text, timeout)
```
Wait for element with css selector ".test-class" to be not present in dom.
```python
element.should.not_present_in_dom(timeout)
element.expect.not_present_in_dom(timeout)
```
Wait for element with css selector ".test-class" to be on the screen.
Checks if element's coordinates match viewport height and width.
```python
element.should.be_on_the_screen(timeout)
element.expect.be_on_the_screen(timeout)
```
