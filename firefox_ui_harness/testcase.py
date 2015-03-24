# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import MarionetteTestCase

from firefox_puppeteer import Puppeteer


class FirefoxTestCase(MarionetteTestCase, Puppeteer):
    """
    Test case that inherits from a Puppeteer object so Firefox specific
    libraries are exposed to test scope.
    """
    def __init__(self, *args, **kwargs):
        MarionetteTestCase.__init__(self, *args, **kwargs)

    def setUp(self, *args, **kwargs):
        MarionetteTestCase.setUp(self, *args, **kwargs)
        Puppeteer.set_marionette(self, self.marionette)

        self._start_window_handles = self.marionette.window_handles
        self.marionette.set_context('chrome')
        self.browser = self.windows.current

    def tearDown(self, *args, **kwargs):
        self.marionette.set_context('chrome')

        try:
            # Marionette needs an existent window to be selected. Take the first
            # browser window which has at least one open tab
            # TODO: We might have to make this more error prone in case the
            # original window has been closed.
            self.browser.focus()
            self.browser.tabbar.tabs[0].switch_to()

            self.prefs.restore_all_prefs()

            # This assertion should be run after all other tearDown code
            # so that in case of a failure, further tests will not run
            # in a state that is more inconsistent than necessary.
            end_window_handles = self.marionette.window_handles
            if len(self._start_window_handles) < len(end_window_handles):
                leaked_windows = set(end_window_handles) - set(self._start_window_handles)
                for win in self.windows.all:
                    win.switch_to()
                    if self.windows.current.handle in leaked_windows:
                        self.logger.error("Chrome window opened but not closed by this test:\n\tType: %s\n\tURL: %s" %
                                          (self.marionette.get_window_type(), self.marionette.get_url()))
                    if self.marionette.get_window_type() == "navigator:browser":
                        for tab in win.tabbar.tabs:
                            if tab.handle in leaked_windows:
                                with self.marionette.using_context('content'):
                                    self.logger.error("Tab opened but not closed by this test:\n\tType: %s\n\tURL: %s" %
                                                      (self.marionette.get_window_type(), self.marionette.get_url()))

                self.browser.focus()
                self.fail("A test must not leak window handles. "
                          "This test started the browser with %s open "
                          "top level browsing contexts, but ended with %s." %
                          (len(self._start_window_handles), len(end_window_handles)))

        finally:
            MarionetteTestCase.tearDown(self, *args, **kwargs)
