# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time

from firefox_ui_harness.testcase import FirefoxTestCase

class TestAssertTutorial(FirefoxTestCase):
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

    def assertRaises(self, *args, **kwargs):
        # Here's the documentation for assertRaises from https://docs.python.org
        """
        Test that an exception is raised when callable is called with any positional or keyword arguments that are also passed to assertRaises(). The test passes if exception is raised, is an error if another exception is raised, or fails if no exception is raised. To catch any of a group of exceptions, a tuple containing the exception classes may be passed as exception.

        If only the exception argument is given, returns a context manager so that the code under test can be written inline rather than as a function:

        with self.assertRaises(SomeException):
            do_something()

        The context manager will store the caught exception object in its exception attribute. This can be useful if the intention is to perform additional checks on the exception raised:

        with self.assertRaises(SomeException) as cm:
            do_something()

        the_exception = cm.exception
        self.assertEqual(the_exception.error_code, 3)

        """
        # The goal of this excercise is to implement you own version of assertRaises
        # that meets this as a specifiction.
        pass

    # Everything from this point down is based on tests for the unittest
    # library in the cpython repository hosted at https://hg.python.org
    # If you get this running and passing, you're probably on the right
    # track!
    def test_assertRaises(self):
        def _raise(e):
            raise e
        self.assertRaises(KeyError, _raise, KeyError)
        self.assertRaises(KeyError, _raise, KeyError("key"))
        try:
            self.assertRaises(KeyError, lambda: None)
        except self.failureException as e:
            self.assertIn("KeyError not raised", e.args)
        else:
            self.fail("assertRaises() didn't fail")
        try:
            self.assertRaises(KeyError, _raise, ValueError)
        except ValueError:
            pass
        else:
            self.fail("assertRaises() didn't let exception pass through")
        with self.assertRaises(KeyError) as cm:
            try:
                raise KeyError
            except Exception, e:
                raise
        self.assertIs(cm.exception, e)

        with self.assertRaises(KeyError):
            raise KeyError("key")
        try:
            with self.assertRaises(KeyError):
                pass
        except self.failureException as e:
            self.assertIn("KeyError not raised", e.args)
        else:
            self.fail("assertRaises() didn't fail")
        try:
            with self.assertRaises(KeyError):
                raise ValueError
        except ValueError:
            pass
        else:
            self.fail("assertRaises() didn't let exception pass through")
