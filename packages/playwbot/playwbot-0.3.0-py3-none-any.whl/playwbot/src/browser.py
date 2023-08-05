"""Implements Playwright's Browser.
"""

from typing import Optional, Union
from pathlib import Path
from playwright.sync_api import sync_playwright


class PlaywbotBrowser:
    def __init__(
        self,
        browser: str = "chromium",
        persistent: bool = False,
        user_data_dir: Optional[Union[str, Path]] = None,
        **kwargs
    ):
        self._playwright = self._start_playwright()
        if not persistent:
            self.browser = self._start_browser(browser, **kwargs)
        else:
            self.browser = self._start_persistent_browser(
                browser, user_data_dir=user_data_dir, **kwargs
            )

    @staticmethod
    def _start_playwright():
        return sync_playwright().start()

    def _start_browser(self, browser: str, **kwargs):
        if browser == "chromium":
            return self._playwright.chromium.launch(**kwargs)

        if browser == "firefox":
            return self._playwright.firefox.launch(**kwargs)

        if browser == "webkit":
            return self._playwright.webkit.launch(**kwargs)

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox', or 'webkit' as browser."
        )

    def _start_persistent_browser(
        self, browser: str, user_data_dir: Optional[Union[str, Path]], **kwargs
    ):
        if browser == "chromium":
            return self._playwright.chromium.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "firefox":
            return self._playwright.firefox.launch_persistent_context(
                user_data_dir, **kwargs
            )
        if browser == "webkit":
            return self._playwright.webkit.launch_persistent_context(
                user_data_dir, **kwargs
            )

        raise RuntimeError(
            "You have to select either 'chromium', 'firefox' or 'webkit' as browser."
        )

    def close_browser(self):
        self.browser.close()
        self._playwright.stop()
