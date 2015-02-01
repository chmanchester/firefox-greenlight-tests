# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.testcase import FirefoxTestCase


class TestTabs(FirefoxTestCase):

    def test_tabbar_basics(self):
        tabbar = self.browser.tabbar

        self.assertEqual(tabbar.window, self.browser)

        self.assertEqual(len(tabbar.tabs), 1)
        self.assertEqual(tabbar.tabs[0].handle, self.marionette.current_window_handle)

    def test_tabbar_open_close(self):
        tabbar = self.browser.tabbar

        self.assertEqual(len(tabbar.tabs), 1)
        self.assertTrue(tabbar.tabs[0].selected)

        # Open and close a new tab by menu
        # TODO we may have to auto switch to this tab?
        tabbar.open_tab()
        self.assertEqual(len(tabbar.tabs), 2)
        self.assertEqual(tabbar.tabs[0].handle, self.marionette.current_window_handle)
        self.assertFalse(tabbar.tabs[0].selected)
        self.assertTrue(tabbar.tabs[1].selected)

        tab = tabbar.close_tab()
        self.assertEqual(len(tabbar.tabs), 1)
        self.assertEqual(tab.handle, tabbar.tabs[0].handle)
        self.assertEqual(tab.handle, self.marionette.current_window_handle)
        self.assertTrue(tabbar.tabs[0].selected)

        # Open and close a new tab by shortcut
        tabbar.open_tab(trigger='shortcut')
        self.assertEqual(len(tabbar.tabs), 2)
        tab = tabbar.close_tab(trigger='shortcut')
        self.assertEqual(len(tabbar.tabs), 1)
        self.assertEqual(tab.handle, tabbar.tabs[0].handle)
        self.assertEqual(tab.handle, self.marionette.current_window_handle)
        self.assertTrue(tabbar.tabs[0].selected)

    def test_switch_to_tab(self):
        tabbar = self.browser.tabbar

        # Open a new tab in the foreground
        # TODO we may have to auto switch to this tab?
        new_tab = tabbar.open_tab()

        # Switch to new tab
        tabbar.tabs[1].switch_to()
        self.assertEqual(new_tab.handle, self.marionette.current_window_handle)
        self.assertEqual(new_tab, tabbar.tabs[1])
        self.assertFalse(tabbar.tabs[0].selected)
        self.assertTrue(tabbar.tabs[1].selected)

        # Focus the first tab
        tabbar.tabs[0].select()
        self.assertEqual(tabbar.tabs[0].handle, self.marionette.current_window_handle)
        self.assertFalse(tabbar.tabs[1].selected)
        self.assertTrue(tabbar.tabs[0].selected)

        tabbar.close_tab(tabbar.tabs[1])
