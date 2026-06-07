"""
Demo test: PlaywrightTimeout environment drift

Reproduces a real CI reliability issue:
- Passes locally when playwright is NOT installed (fallback to Exception)
- Fails in CI where playwright IS installed (requires message argument)

Root cause: conditional import creates different behavior across environments.
"""
try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
except ImportError:
    PlaywrightTimeout = Exception


def test_playwright_timeout_handles_timeout_gracefully():
    """Test that PlaywrightTimeout can be instantiated in timeout handling code."""
    # BUG: Missing required message argument
    # Works locally (PlaywrightTimeout = Exception, no args needed)
    # Fails in CI (PlaywrightTimeout = playwright TimeoutError, requires message)
    timeout = PlaywrightTimeout("timeout exceeded")
    assert timeout is not None


def test_playwright_timeout_with_message():
    """Test that PlaywrightTimeout works with message argument."""
    timeout = PlaywrightTimeout("timeout exceeded")
    assert timeout is not None
