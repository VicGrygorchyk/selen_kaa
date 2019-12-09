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


def test_timeout_duration_on_visibility(app):
    index_page = app.goto_index_page()
    start_t = time.time()
    assert not index_page.test_div.expect.be_visible(timeout=1)
    after_1_sec_time = time.time()
    assert all((after_1_sec_time - start_t >= 1, after_1_sec_time - start_t <= 2))

    start_t2 = time.time()
    assert not index_page.test_div.expect.be_visible(timeout=5)
    after_6_sec_time = time.time()
    assert all((after_6_sec_time - start_t2 >= 5, after_6_sec_time - start_t2 <= 6))
