# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.testcase import FirefoxTestCase
from marionette import By, errors


class TestAboutPrivateBrowsing(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.pb_url = self.marionette.absolute_url('private_browsing/about.html?')

    def tearDown(self):
        self.prefs.restore_pref('app.support.baseURL')

    def testCheckAboutPrivateBrowsing(self):
        self.assertFalse(self.browser.is_private)

        self.prefs.set_pref('app.support.baseURL', self.pb_url)

        self.marionette.set_context('content')
        self.marionette.navigate('about:privatebrowsing')

        description = self.browser.get_localized_entity(
            'aboutPrivateBrowsing.subtitle.normal')

        status_node = self.marionette.find_element(By.CSS_SELECTOR,
                                                   'p.showNormal')
        self.assertEqual(status_node.text, description)

        access_key = self.browser.get_localized_entity(
            'privatebrowsingpage.openPrivateWindow.accesskey')

        start_win = self.client.current_window_handle
        # Send keys to the top html element.
        top_html = self.marionette.find_element(By.TAG_NAME, 'html')
        top_html.send_keys(self.keys.SHIFT, self.keys.ACCEL, access_key)

        self.wait_for_condition(lambda mn: len(self.windows.all) == 2)

        windows = self.client.window_handles
        windows.remove(start_win)
        dest_pb_win = windows.pop()

        with self.marionette.using_context('chrome'):
            self.windows.switch_to(lambda win: win.is_private)
            self.browser_pb = self.windows.current
            self.assertTrue(self.browser_pb.is_private)

        def find_element(mn):
            try:
                link = self.client.find_element(By.ID, 'learnMore')
                link.click()
                return True
            except errors.NoSuchElementException:
                return False

        self.wait_for_condition(find_element)
        self.wait_for_condition(lambda mn: len(mn.window_handles) == 3)
        windows = self.client.window_handles
        windows.remove(start_win)

        target_url = self.pb_url + 'private-browsing'
        pb_win = windows.pop()
        self.client.switch_to_window(pb_win)
        self.assertIn(self.client.get_url(), target_url)

        self.client.close()
        self.client.switch_to_window(dest_pb_win)
        self.client.close()

        self.client.switch_to_window(start_win)
