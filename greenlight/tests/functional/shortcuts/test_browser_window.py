# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.testcase import FirefoxTestCase


class TestBrowserWindowShortcuts(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        # Putting history in the tab so this works the same way when running
        # alone as when running multiple tests.
        with self.client.using_context('content'):
            self.client.navigate("data:text/html,<title>Test</title>")
            self.client.navigate("about:blank")

    def test_addons_manager(self):
        key = self.browser.get_localized_entity('addons.commandkey')
        windows = self.client.window_handles
        start_window = self.client.current_window_handle

        # On Linux the shortcut will only work if no other text field has focus
        # TODO: Remove focus from the location bar
        self.browser.send_keys(self.keys.SHIFT, self.keys.ACCEL, key)
        self.wait_for_condition(lambda mn: len(mn.window_handles) == len(windows) + 1)

        # TODO: For now we have to hard-code the tab, but we should really work
        # with events here to get the new tab automatically.
        self.marionette.set_context("content")

        # Marionette currently fails to detect the correct tab
        self.client.switch_to_window((set(self.client.window_handles) - set(windows)).pop())
        self.wait_for_condition(lambda mn: mn.get_url() == "about:addons")
        self.client.close()
        self.client.switch_to_window(start_window)

    def test_search_field(self):
        current_name = self.marionette.execute_script("""
            return window.document.activeElement.localName;
        """)

        # This doesn't test anything if we're already at input.
        self.assertNotEqual(current_name, "input")

        keys = [self.keys.ACCEL]
        if self.marionette.session_capabilities['platformName'] == 'LINUX':
            keys.append(self.browser.get_localized_entity('searchFocusUnix.commandkey'))
        else:
            keys.append(self.browser.get_localized_entity('searchFocus.commandkey'))

        # CONTROL will only work on Linux and Windows. On OS X it is COMMAND.
        self.browser.send_keys(*keys)

        # TODO: Check that the right input box is focused
        # Located below searchbar as class="autocomplete-textbox textbox-input"
        # Anon locator has not been released yet (bug 1080764)
        def has_input_selected(mn):
            selection_name = mn.execute_script("""
                return window.document.activeElement.localName;
            """)
            return selection_name == "input"

        self.wait_for_condition(has_input_selected)
