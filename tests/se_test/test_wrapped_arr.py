from se_wrapper.element.se_elements_array import SeElementsArray
from se_wrapper.element.se_web_element import SeWebElement
from tests.webapp.driver_wrapper import WrappedElementsArray, WebElementWrapper
from tests.webapp.pages.index_page import THE_SAME_CLASS
from se_wrapper.utils import se_utils


def test_find_elements_works(app):
    app.goto_index_page()
    # verify find element works
    the_same_text = se_utils.find_all_elements_by_css(app.web_driver,
                                                      THE_SAME_CLASS,
                                                      timeout=1)
    assert len(the_same_text) == 7


def test_init_elements_works(app):
    index_page = app.goto_index_page()
    # verify init element works
    assert len(index_page.the_same_text) == 7


def test_arr_is_lazy(app):
    """Verify the init doesn't crash before the element is visible."""
    thesame_element = app.web_driver.init_all_web_elements(THE_SAME_CLASS)
    app.goto_index_page()
    # only here element is rendered
    assert len(thesame_element) == 7


def test_can_override_webelements_type(app):
    """Verify we can extend SeElementsArray and pass new class to config."""
    index_page = app.goto_index_page()
    assert type(index_page.the_same_text) is WrappedElementsArray
    assert isinstance(index_page.the_same_text, SeElementsArray)


def test_elem_in_arr(app):
    index_page = app.goto_index_page()
    fst_elem = index_page.the_same_text.pop()
    assert type(fst_elem) is WebElementWrapper
    assert isinstance(fst_elem, SeWebElement)
    for elem in index_page.the_same_text:
        assert elem.is_displayed()
