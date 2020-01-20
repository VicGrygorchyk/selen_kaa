import time

import pytest
from selenium.common.exceptions import TimeoutException


TIMEOUT_6_SEC = 6
TIMEOUT_BASE_ERR_MSG = "TimeoutException while waited {} second(s) for the element '{}' to {}."


def test_should_invisibility(app):
    index_page = app.goto_index_page()
    assert index_page.test_div.should.be_invisible(timeout=TIMEOUT_6_SEC)
    index_page.btn_show_div.click()
    assert index_page.test_div.should.be_visible(timeout=TIMEOUT_6_SEC)

    index_page.btn_hide_div.click()
    assert index_page.test_div.should.be_invisible(timeout=TIMEOUT_6_SEC)


def test_should_visible_web_element(app):
    """Verify be visible and be invisible works for Selenium WebElement."""
    index_page = app.goto_index_page()
    assert app.wait.element_to_be_invisible(index_page.test_div.web_element, timeout=TIMEOUT_6_SEC)
    index_page.btn_show_div.click()
    assert app.wait.element_to_be_visible(index_page.test_div.web_element, timeout=TIMEOUT_6_SEC)
    index_page.btn_hide_div.click()
    assert app.wait.element_to_be_invisible(index_page.test_div.web_element, timeout=TIMEOUT_6_SEC)


def test_should_visible_by_selector(app):
    """Verify be visible and be invisible works when to pass css selector to method."""
    index_page = app.goto_index_page()
    assert app.wait.element_to_be_invisible(index_page.test_div.selector, timeout=TIMEOUT_6_SEC)
    index_page.btn_show_div.click()
    assert app.wait.element_to_be_visible(index_page.test_div.selector, timeout=TIMEOUT_6_SEC)
    index_page.btn_hide_div.click()
    assert app.wait.element_to_be_invisible(index_page.test_div.selector, timeout=TIMEOUT_6_SEC)


def test_expect_invisibility(app):
    index_page = app.goto_index_page()
    assert index_page.test_div.expect.be_invisible(timeout=TIMEOUT_6_SEC)
    index_page.btn_show_div.click()
    assert index_page.test_div.expect.be_visible(timeout=TIMEOUT_6_SEC)

    index_page.btn_hide_div.click()
    assert index_page.test_div.expect.be_invisible(timeout=TIMEOUT_6_SEC)


def test_exception_on_visibility(app):
    index_page = app.goto_index_page()
    # raises(Error, match) param is too verbose for verification
    with pytest.raises(TimeoutException) as exc:
        assert index_page.test_div.should.be_visible(timeout=1)
        assert TIMEOUT_BASE_ERR_MSG.format(1, index_page.test_div.selector, 'be visible') == exc.msg


def test_exception_on_invisibility(app):
    index_page = app.goto_index_page()
    index_page.btn_show_div.click()
    time.sleep(6)
    with pytest.raises(TimeoutException) as exc:
        assert index_page.test_div.should.be_invisible(timeout=1)
        assert TIMEOUT_BASE_ERR_MSG.format(1, index_page.test_div.selector, 'disappear') in exc.msg


def test_expect_visibility_has_no_exception(app):
    index_page = app.goto_index_page()
    assert not index_page.test_div.expect.be_visible(timeout=1)


def test_expect_invisibility_has_no_exception(app):
    index_page = app.goto_index_page()
    index_page.btn_show_div.click()
    time.sleep(6)
    assert not index_page.test_div.expect.be_invisible(timeout=1)


def test_expect_no_exc_if_no_such_element(app):
    # no exception even such element doesn't exist
    index_page = app.goto_index_page()
    assert index_page.no_such_element.expect.be_invisible(1)


def test_timeout_duration_on_expect_visibility(app):
    index_page = app.goto_index_page()
    start_t = time.time()
    assert not index_page.test_div.expect.be_visible(timeout=1)
    after_1_sec_time = time.time()
    assert all((after_1_sec_time - start_t >= 1, after_1_sec_time - start_t <= 2))

    start_t2 = time.time()
    assert not index_page.test_div.expect.be_visible(timeout=5)
    after_6_sec_time = time.time()
    assert all((after_6_sec_time - start_t2 >= 5, after_6_sec_time - start_t2 <= 6))


def test_timeout_duration_on_invisibility(app):
    index_page = app.goto_index_page()
    start_t = time.time()
    assert index_page.test_div.expect.be_invisible(timeout=1)
    after_1_sec_time = time.time()
    # it should be True faster than 1 seconds, as the condition is true from beginning
    assert after_1_sec_time - start_t <= 1

    start_t2 = time.time()
    assert index_page.test_div.expect.be_invisible(timeout=5)
    after_6_sec_time = time.time()
    # it should be True faster than 5 seconds, as the condition is true from beginning
    assert after_6_sec_time - start_t2 <= 1


def test_invisible_timeout_none_and_zero(app):
    index_page = app.goto_index_page()
    start_t = time.time()
    assert index_page.test_div.expect.be_invisible()
    assert index_page.test_div.expect.be_invisible(None)
    assert index_page.test_div.expect.be_invisible(0)
    after_time = time.time()
    # it should be faster than 1 seconds
    assert after_time - start_t <= 1


def test_visible_timeout_none_and_zero(app):
    index_page = app.goto_index_page()
    start_t = time.time()
    assert index_page.btn_show_div.expect.be_visible()
    assert index_page.btn_show_div.expect.be_visible(None)
    assert index_page.btn_show_div.expect.be_visible(0)
    after_time = time.time()
    # it should be faster than 1 seconds
    assert after_time - start_t <= 1
