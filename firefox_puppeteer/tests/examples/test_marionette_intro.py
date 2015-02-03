# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from marionette import (
    By,
    NoSuchElementException
)
from marionette.keys import Keys

from firefox_ui_harness.testcase import FirefoxTestCase

class TestMarionetteTutorial(FirefoxTestCase):
    """This is a test class containing stubs of example tests designed to
    demonstrate fundamentals of marionette based tests and the Firefox Puppeteer
    libraries.
    """

    def setUp(self):
        # Set up runs before every test method.
        FirefoxTestCase.setUp(self)
        self.marionette.set_context("content")


    def tearDown(self):
        # Tear down runs after every test method.
        # Anything about the browser that's changed in a test should be
        # reverted to its original state either in a test method or in
        # tearDown.
        FirefoxTestCase.tearDown(self)

    def test_navigate(self):
        # Navigation is a fundamental marionette interaction. It's a method
        # that takes one argument, a destination url. It returns after the
        # destination document has loaded (this means document.readyState ==
        # "complete", or "interactive" if it's an "about:" uri).

        # self.marionette.navigate("about:blank")
        # # Note: Adding arbitrary delays to a test is an ok way to see what's
        # # going on as it runs, but sleeping randomly to wait for events is
        # # generally a poor practice when writing tests.
        # time.sleep(2)
        # print "The current url is: %s" % self.marionette.get_url()
        # self.marionette.navigate("data:text/html,<h1>Hello, marionette!</h1>")
        # print "The current url is: %s" % self.marionette.get_url()

        # Tests generally will navigate to static files in the test environment
        # (although some mozmill tests hit the network). The marionette automation
        # harness runs a webserver to serve local files. Given a path relative to
        # a known docroot (firefox_ui_tests/resources in our case), marionette

        # has a method, "absolute_url", that will fill in the rest.

        # destination_url = self.marionette.absolute_url('layout/mozilla.html')
        # self.marionette.navigate(destination_url)

        # # You might be thinking, "Well, simulating regular web navigation isn't that
        # # fancy, don't we already have a way to navigate that ships with Gecko?"
        # # Ok, let's use a script to emulate this functionality:
        # def my_navigate(url):
        #     self.marionette.execute_script("""
        #       document.location = arguments[0];
        #     """, script_args=[url])

        # # Let's try our navigate method.
        # destination_url = "about:blank"
        # my_navigate(destination_url)
        # self.assertEqual(self.marionette.get_url(), destination_url)

        # # Ok, let's see what happens when we hit the network:
        # destination_url = "http://people.mozilla.org/~cmanchester"
        # my_navigate(destination_url) # self.marionette.navigate(destination_url)
        # self.assertEqual(self.marionette.get_url(), destination_url)
        pass

    def test_element(self):
        # This test works with the urlbar element, so unlike tests in the rest
        # of the file, we're going to run this test in chrome context. Because
        # we set context to content in setUp, the rest of the tests methods
        # will not be harmed by this, even if we do nothing at the end of the
        # method.
        self.marionette.set_context("chrome")

        # This test needs to interact with the awesomebar. The awesomebar is
        # just a xul element somewhere we need to select...

        # Getting a handle to an element is a matter of calling "find_element".
        # The first argument is a strategy (one of some constants defined in
        # Marionette.By, which are just strings). The second argument is a
        # "target" whose meaning depends on the strategy. A common strategy is
        # to retrieve an element by its id.

        # # How can we find the back button?
        # back_button = self.marionette.find_element(By.ID, "back-button")

        # If we had guessed wrong, we would have run into problems:
        # back_button = self.marionette.find_element(By.ID, "backbutton")

        # # Ok, we got lucky! What about the urlbar?
        # urlbar = self.marionette.find_element(By.ID, "urlbar")

        # # Once we have an element, we can simulate typical input interactions
        # # and inspect arbitrary properties. For instance:
        # print "Is the urlbar focused before our click? %s" % urlbar.get_attribute('focused')
        # urlbar.click()
        # print "Is the urlbar focused after our click? %s" % urlbar.get_attribute('focused')
        # data_uri = 'data:text/html,<h1>Marionette sent these keys</h1>'
        # urlbar.send_keys(data_uri)
        # print "The value of the urlbar is: %s" % urlbar.get_attribute('value')
        # urlbar.send_keys(Keys.ENTER)
        # with self.marionette.using_context("content"):
        #     current_url = self.marionette.get_url()
        #     print "The current url is: %s" % current_url

        # # As above, let's see what happens when we hit the network:
        # network_uri = "http://people.mozilla.org/~cmanchester"
        # urlbar.send_keys(network_uri + Keys.ENTER)
        # with self.marionette.using_context("content"):
        #     current_url = self.marionette.get_url()
        #     print "The current url is: %s" % current_url

        # # Note that there is a puppeteer library exposing a very similar functionality:
        # network_uri = "http://people.mozilla.org/~cmanchester"
        # self.browser.navbar.locationbar.load_url(network_uri)
        # with self.marionette.using_context("content"):
        #     current_url = self.marionette.get_url()
        #     print "The current url is: %s" % current_url

    def test_wait(self):
        # There's a simple builtin method exposed to test cases for waiting:
        # wait_for_condition.

        # def my_navigate(url):
        #     self.marionette.execute_script("""
        #       document.location = arguments[0];
        #     """, script_args=[url])

        # destination_url = "http://people.mozilla.org/~cmanchester/cov/"
        # my_navigate(destination_url)
        # self.assertEqual(self.marionette.get_url(), destination_url)

        # # A "Wait" object just needs access to marionette, and provides some more
        # # bells and whistles for specific uses:
        # from marionette import Wait
        # from marionette import errors
        # wait = Wait(self.marionette)
        # wait.until(lambda m: m.get_url() == destination_url)

        # wait = Wait(self.marionette, timeout=0.1, interval=0.01)
        # wait.until(lambda m: m.get_url() == destination_url)
        pass
