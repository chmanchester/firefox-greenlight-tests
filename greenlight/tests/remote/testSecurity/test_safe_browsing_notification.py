# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.testcase import FirefoxTestCase
from marionette.errors import (
    NoSuchElementException,
    StaleElementException
)
import time

test_data = [
    # Phishing URL object
    ("safebrowsing.notAForgeryButton.label",
     "www.google.com/safebrowsing/report_error",
     "http://www.itisatrap.org/firefox/its-a-trap.html"),
    # Malware URL object
    ("safebrowsing.notAnAttackButton.label",
     "www.stopbadware.org",
     "http://www.itisatrap.org/firefox/its-an-attack.html"),
]


class TestSafeBrowsingNotificationBar(FirefoxTestCase):

    def __init__(self, *args, **kwargs):
        FirefoxTestCase.__init__(self, *args, **kwargs)

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.start_windows = self.client.window_handles
        # Give the browser a little time, because SafeBrowsing.jsm takes a
        # while between start up and adding the example urls to the db.
        time.sleep(2)

    def tearDown(self):
        self.perms.remove('www.itisatrap.org', 'safe-browsing')

    def close_tabs(self):
        # Close all but one tab.
        while len(self.tabstrip.tabs) > 1:
            self.tabstrip.tabs[-1].close()

    def test_notification_bar(self):
        self.client.set_context("content")
        for item in test_data:
            label, report_page, unsafe_page = item
            self.client.navigate(unsafe_page)
            self.check_ignore_warning_button(unsafe_page)
            self.check_no_phishing_button(label, report_page)

            # Go back to the notification bar
            self.client.navigate(unsafe_page)
            self.check_ignore_warning_button(unsafe_page)

            # Test the get me out of here button
            self.check_get_me_out_of_here_button()

            # Go back to the notification bar
            self.client.navigate(unsafe_page)
            self.check_ignore_warning_button(unsafe_page)

            self.client.set_context('chrome')
            self.check_x_button()
            self.client.set_context('content')

    def check_ignore_warning_button(self, unsafe_page):
        ignore_warning_button = self.client.find_element("id",
                                                         "ignoreWarningButton")

        # This isn't clickable by the time we get here and needs a
        # pretty significant delay.
        time.sleep(1)

        ignore_warning_button.click()

        def find_main_feature_el(mn):
            try:
                mn.find_element("id", "main-feature")
                return True
            except:
                return False

        self.wait_for_condition(find_main_feature_el)
        self.assertRaises(NoSuchElementException, self.client.find_element,
                          'id', 'ignoreWarningButton')

        self.assertEquals(self.client.get_url(), unsafe_page)
        self.perms.remove('www.itisatrap.org', 'safe-browsing')

    def find_button(self, element, label):
        buttons = element.find_elements('tag name', 'button')
        found_button = None
        for button in buttons:
            if button.get_attribute('label') == label:
                found_button = button
        self.assertTrue(found_button is not None, 'Could not find button')
        return found_button

    def check_no_phishing_button(self, label, report_page):
        button_label = self.browser.get_localized_property(label)
        with self.client.using_context('chrome'):
            tab_count = len(self.browser.tabbar.tabs)
            blocked_badware_page = (self.client.find_element('id', 'content')
                                               .find_element('anon attribute',
                                                             {'value': 'blocked-badware-page'}))
            self.find_button(blocked_badware_page, button_label).click()

            self.wait_for_condition(lambda _: len(self.browser.tabbar.tabs) == tab_count + 1)
            self.wait_for_condition(lambda _: report_page in self.browser.navbar.location)
            self.browser.tabbar.active_tab.close()

    def check_get_me_out_of_here_button(self):
        label = self.browser.get_localized_property(
            'safebrowsing.getMeOutOfHereButton.label')
        with self.client.using_context('chrome'):
            blocked_badware_page = (self.client.find_element('id', 'content')
                                               .find_element('anon attribute',
                                                             {'value': 'blocked-badware-page'}))
            self.find_button(blocked_badware_page, label).click()

        expected_homepage = self.prefs.get_pref('browser.startup.homepage',
                                                'nsIPrefLocalizedString')
        self.wait_for_condition(lambda mn: expected_homepage in mn.get_url())

    def check_x_button(self):
        x_button = (self.client.find_element('id', 'content')
                               .find_element('anon attribute',
                                             {'value': 'blocked-badware-page'})
                               .find_element('anon attribute',
                                             {'class': 'messageCloseButton close-icon tabbable'}))
        x_button.click()
        badware_page = (self.client.find_element('id', 'content')
                                   .find_element('anon attribute',
                                                 {'value': 'blocked-badware-page'}))

        def x_button_gone(mn):
            try:
                badware_page.find_element('anon attribute',
                                          {'class': 'messageCloseButton close-icon tabbable'})
                return False
            except StaleElementException:
                return True
            except:
                return False

        self.wait_for_condition(x_button_gone)
