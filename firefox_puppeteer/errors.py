# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import MarionetteException


class InvalidValueError(MarionetteException):
    pass


class UnexpectedWindowTypeError(MarionetteException):
    pass


class UnknownTabError(MarionetteException):
    pass


class UnknownWindowError(MarionetteException):
    pass
