# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from firefox_ui_harness.testcase import FirefoxTestCase

class TestLibraryTutorial(FirefoxTestCase):
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

    # The goal of this tutorial is to write a library providing access to commonly
    # used UI elements in the area around the urlbar. So, from left to right, what can
    # we access?
    @property
    def back_button(self):
        pass

    @property
    def forward_button(self):
        pass

    @property
    def identity_box(self):
        pass

    @property
    def urlbar_input(self):
        pass

    @property
    def urlbar_dropmarker(self):
        pass

    @property
    def urlbar_reloadbutton(self):
        pass

    @property
    def searchbar_textbox(self):
        pass

    @property
    def addbookmark_button(self):
        pass

    @property
    def bookmarks_menu_button(self):
        pass

    @property
    def downloads_button(self):
        pass

    @property
    def home_button(self):
        pass

    @property
    def hello_button(self):
        pass

    @property
    def hamburger_menu(self):
        pass


    # These are some very basic tests for the above properties. These
    # provide tests that are necessary but not sufficient to establish
    # the correctness of the properties. Working with the inspector
    # and writing tests that interact with these elements will help
    # you understand whether they are correct.

    # Initially, these tests will all fail in uninteresting ways.
    # Uncomment them one by one as you work through elements.

    # def test_back_button(self):
    #     self.assertEqual(self.back_button.get_attribute('localName'),
    #                      'toolbarbutton')
    #     self.assertEqual(self.back_button.get_attribute('type'),
    #                      'menu')

    # def test_forward_button(self):
    #     self.assertEqual(self.forward_button.get_attribute('localName'),
    #                      'toolbarbutton')
    #     self.assertEqual(self.forward_button.get_attribute('type'),
    #                      'menu')

    # def test_identity_box(self):
    #     self.assertEqual(self.identity_box.get_attribute('localName'),
    #                      'box')
    #     self.assertEqual(self.identity_box.get_attribute('role'),
    #                      'button')

    # def test_urlbar_input(self):
    #     self.assertEqual(self.urlbar_input.get_attribute('localName'),
    #                      'input')
    #     self.assertEqual(self.urlbar_input.get_attribute('type'),
    #                      'text')

    # def test_urlbar_dropmarker(self):
    #     self.assertEqual(self.urlbar_dropmarker.get_attribute('localName'),
    #                      'dropmarker')
    #     self.assertIn('urlbar-history-dropmarker',
    #                   self.urlbar_dropmarker.get_attribute('class'))

    # def test_urlbar_reloadbutton(self):
    #     self.assertEqual(self.urlbar_reloadbutton.get_attribute('localName'),
    #                      'toolbarbutton')

    # def test_searchbar_textbox(self):
    #     self.assertEqual(self.searchbar_textbox.get_attribute('localName'),
    #                      'textbox')
    #     self.assertEqual(self.searchbar_textbox.get_attribute('type'),
    #                      'autocomplete')

    # def test_addbookmarks_button(self):
    #     self.assertEqual(self.addbookmark_button.get_attribute('localName'),
    #                      'toolbarbutton')

    # def test_bookmarks_menu_button(self):
    #     self.assertEqual(self.bookmarks_menu_button.get_attribute('localName'),
    #                      'dropmarker')

    # def test_downloads_button(self):
    #     self.assertEqual(self.downloads_button.get_attribute('localName'),
    #                      'toolbarbutton')
    #     self.assertEqual(self.downloads_button.get_attribute('label'),
    #                      'Downloads')

    # def test_home_button(self):
    #     self.assertEqual(self.home_button.get_attribute('localName'),
    #                      'toolbarbutton')
    #     self.assertEqual(self.home_button.get_attribute('label'),
    #                      'Home')

    # def test_hello_button(self):
    #     self.assertEqual(self.hello_button.get_attribute('localName'),
    #                      'toolbarbutton')
    #     self.assertEqual(self.hello_button.get_attribute('label'),
    #                      'Hello')

    # def test_hamburger_menu(self):
    #     self.assertEqual(self.hamburger_menu.get_attribute('localName'),
    #                      'toolbaritem')
