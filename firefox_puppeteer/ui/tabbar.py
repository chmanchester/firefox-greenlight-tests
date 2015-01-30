# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import (
    HTMLElement,
    Wait,
)

from marionette.errors import NoSuchElementException, StaleElementException

import firefox_puppeteer.errors as errors

from .. import DOMElement
from ..base import UIBaseLib


class TabBar(UIBaseLib):

    @property
    def tabs(self):
        """Returns a list of all :class:`Tab` elements

        :returns: List of :class:`Tab`'s
        """
        tabs = self.toolbar.find_elements('tag name', 'tab')
        return [Tab(lambda: self.marionette, self.window, tab) for tab in tabs]

    @property
    def toolbar(self):
        """ Returns the toolbar element

        :returns: Reference to the toolbar
        """
        return self.marionette.find_element('id', 'tabbrowser-tabs')

    @property
    def newtab_button(self):
        """ Returns the new tab button element

        :returns: Reference to the button
        """
        return self.toolbar.find_element('anon attribute', {'anonid': 'tabs-newtab-button'})

    @property
    def active_tab(self):
        """
        :returns: The :class:`TabElement` corresponding to the currently active
                  tab.
        """
        for tab in self.tabs:
            if tab.is_active():
                return tab

    @property
    def menupanel(self):
        """
        Provides access to the menu popup. This is the menu opened after
        clicking the settings button on the right hand side of the browser.

        See the :class:`~ui.menu.MenuPanel` reference.
        """
        return MenuPanel(lambda: self.marionette)

    def get_tab(self, target):
        """
        Get a reference to the specified tab.

        :param target: Either an index of `tabs` or a substring of the label.
        :returns: A :class:`TabElement` corresponding to the specified tab.
        """
        if isinstance(target, int):
            return self.tabs[target]

        if isinstance(target, basestring):
            for tab in self.tabs:
                if target in tab.get_attribute('label'):
                    return tab

            raise NoSuchElementException('Tab with a label containing "{}"" not'
                                         ' found'.format(target))

        raise TypeError("Invalid type for 'target': {}".format(type(target)))


class Tab(UIBaseLib):
    """Wraps a tab element."""

    def __init__(self, marionette_getter, window, tab_element):
        UIBaseLib.__init__(self, marionette_getter, window)

        self._tab = tab_element
        self._handle = self.marionette.execute_script("""
          var win = arguments[0].linkedBrowser.contentWindowAsCPOW;
          var id = win.QueryInterface(Ci.nsIInterfaceRequestor)
                        .getInterface(Ci.nsIDOMWindowUtils)
                        .outerWindowID.toString();
          return id;
        """, script_args=[tab_element])

    @property
    def handle(self):
        """Returns the `tab handle` of the content window

        :returns: `window handle`
        """
        return self._handle

    @property
    def selected(self):
        """Returns `True` if the tab is currently selected
        """
        # self.marionette.switch_to_window(self._handle)
        return self.marionette.execute_script("""
            let tab = arguments[0];
            return tab.getAttribute('selected');
        """, script_args=[self._tab])

    def close(self):
        """
        Closes this tab.
        """
        close_button = (self.find_element('anon', None)
                            .find_element('class name',
                                          'tab-close-button'))
        ret = close_button.click()

        def im_gone(m):
            try:
                self.tag_name
                return False
            except StaleElementException:
                return True
        Wait(self.marionette).until(im_gone)
        return ret

    def switch_to(self):
        """Switch to (activate) the specified tab.
        """
        self.marionette.switch_to(self._handle)
        return tab.click()


class MenuPanel(UIBaseLib):

    @property
    def popup(self):
        """
        :returns: The :class:`MenuPanelElement`.
        """
        popup = self.marionette.find_element('id', 'PanelUI-popup')
        return self.MenuPanelElement(popup)

    class MenuPanelElement(DOMElement):
        """
        Wraps the menu panel.
        """
        _buttons = None

        @property
        def buttons(self):
            """
            :returns: A list of all the clickable buttons in the menu panel.
            """
            if not self._buttons:
                self._buttons = (self.find_element('id', 'PanelUI-multiView')
                                     .find_element('anon attribute',
                                                   {'anonid': 'viewContainer'})
                                     .find_elements('tag name',
                                                    'toolbarbutton'))
            return self._buttons

        def click(self, target=None):
            """
            Overrides HTMLElement.click to provide a target to click.

            :param target: The label associated with the button to click on,
             e.g 'New Private Window'.
            """
            if not target:
                return DOMElement.click(self)

            for button in self.buttons:
                if button.get_attribute('label') == target:
                    return button.click()
            raise NoSuchElementException('Could not find "{}"" in the '
                                         'menu panel UI'.format(target))
