"""
Demo: PlaywrightTimeout instantiation bug
This reproduces the CI failure in tests/unit_tests/utils/test_screenshot_utils.py
"""
try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
except ImportError:
    PlaywrightTimeout = Exception

def test_playwright_timeout_with_args():
    # This works everywhere
    timeout = PlaywrightTimeout("timeout exceeded")
    assert timeout is not None

def test_playwright_timeout_without_args():
    # This is the bug - fails when playwright is installed (CI)
    # passes when playwright is not installed (local Exception fallback)
    timeout = PlaywrightTimeout()
    assert timeout is not None
