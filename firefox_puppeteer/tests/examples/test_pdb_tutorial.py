# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette import By

from firefox_ui_harness.testcase import FirefoxTestCase

class TestPDBExample(FirefoxTestCase):
    """This is a test class containing stubs of example tests designed to
    demonstrate fundamentals of marionette based tests and the Firefox Puppeteer
    libraries.
    """

    def setUp(self):
        # Set up runs before every test method.
        FirefoxTestCase.setUp(self)


    def tearDown(self):
        # Tear down runs after every test method.
        # Anything about the browser that's changed in a test should be
        # reverted to its original state either in a test method or in
        # tearDown.
        FirefoxTestCase.tearDown(self)

    def test_pdb_execute(self):
        # Sometimes tests lie by failing to fail when you expect them to.
        # I want to write a test that opens the awesomebar autocomplete dropdown.
        # How can I make sure this is working as I expect?
        # Seeing is believing, let's run this in the debugger
        popup = self.marionette.find_element(By.ID,
                                             'PopupAutoCompleteRichResult')
        urlbar = self.marionette.find_element(By.ID,
                                              'urlbar')
        import pdb; pdb.set_trace()
