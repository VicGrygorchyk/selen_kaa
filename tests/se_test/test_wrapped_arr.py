from selen_kaa.element.se_elements_array import SeElementsArray
from selen_kaa.element.se_web_element import SeWebElement

from tests.webapp.driver_wrapper import WebElementWrapper
from tests.webapp.pages.index_page import THE_SAME_CLASS


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
    index_page = app.goto_index_page()
    assert isinstance(index_page.the_same_text, SeElementsArray)
    assert type(index_page.the_same_text[0]) is WebElementWrapper
    assert isinstance(index_page.the_same_text[0], SeWebElement)


def test_elem_in_arr(app):
    index_page = app.goto_index_page()
    fst_elem = index_page.the_same_text.pop()
    assert isinstance(fst_elem, SeWebElement)
    for index, elem in enumerate(index_page.the_same_text):
        assert elem.is_displayed()
        assert str(index) in elem.text
    assert all(("Test the same" in elem.text for elem in index_page.the_same_text))
    # assert elements are different
    assert index_page.the_same_text[0] != index_page.the_same_text[1]
    assert index_page.the_same_text[2] != index_page.the_same_text[3]
    assert index_page.the_same_text[4] != index_page.the_same_text[5]
