# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import MarionetteException

from ..base import BaseLib


class Preferences(BaseLib):
    archive = {}

    def clear_user_pref(self, pref_name):
        """Clear a user set preference.

        :param pref_name: The preference to clear
        """
        with self.marionette.using_context('chrome'):
            return self.marionette.execute_script("""
              Cu.import("resource://gre/modules/Services.jsm");
              let prefBranch = Services.prefs.QueryInterface(Ci.nsIPrefBranch);

              let pref_name = arguments[0];

              if (prefBranch.prefHasUserValue(pref_name)) {
                prefBranch.clearUserPref(pref_name);
                return true;
              }
              else {
                return false;
              }
            """, script_args=[pref_name])

    def get_pref(self, pref_name, default_branch=False, interface=None):
        """
        Retrieve a preference.

        :param pref_name: The preference name to retrieve the value from
        :param default_branch: Read from the default branch (default False)
        :param interface: Interface to use for the complex value (default None)
                          Possible values are: nsILocalFile, nsISupportsString,
                          and nsIPrefLocalizedString

        :returns: The value of the specified preference.
        """
        assert pref_name

        # Bug 1118825 - None is causing an exception to be raised
        interface = interface or ''

        with self.marionette.using_context('chrome'):
            value = self.marionette.execute_script("""
              Cu.import("resource://gre/modules/Services.jsm");

              let pref_name = arguments[0];
              let default_branch = arguments[1];
              let interface = arguments[2];

              let prefBranch = undefined;
              if (default_branch) {
                prefBranch = Services.prefs.getDefaultBranch("");
              }
              else {
                prefBranch = Services.prefs.QueryInterface(Ci.nsIPrefBranch);
              }

              // If an interface has been set, handle it differently
              if (interface != '') {
                return prefBranch.getComplexValue(pref_name,
                                                  Ci[interface]).data;
              }

              let type = prefBranch.getPrefType(pref_name);

              switch (type) {
                case prefBranch.PREF_STRING:
                  return prefBranch.getCharPref(pref_name);
                case prefBranch.PREF_BOOL:
                  return prefBranch.getBoolPref(pref_name);
                case prefBranch.PREF_INT:
                  return prefBranch.getIntPref(pref_name);
                case prefBranch.PREF_INVALID:
                  return null;
              }
            """, script_args=[pref_name, default_branch, interface])

        return value

    def set_pref(self, pref_name, value):
        """Sets a preference to a specified value.

        Also archives the old value so that the preference can be restored with
        `restore_pref`.

        :param pref_name: Name of the preference to set.
        :param value: The value to set the preference to.
        """
        assert pref_name is not None
        assert value is not None

        with self.marionette.using_context('chrome'):
            # Backup original value only once
            if pref_name not in self.archive:
                self.archive[pref_name] = self.get_pref(pref_name)

            retval = self.marionette.execute_script("""
              Cu.import("resource://gre/modules/Services.jsm");
              let prefBranch = Services.prefs.QueryInterface(Ci.nsIPrefBranch);

              let pref_name = arguments[0];
              let value = arguments[1];

              let type = prefBranch.getPrefType(pref_name);

              // If the pref does not exist yet, get the type from the value
              if (type == prefBranch.PREF_INVALID) {
                switch (typeof value) {
                  case "boolean":
                    type = prefBranch.PREF_BOOL;
                    break;
                  case "number":
                    type = prefBranch.PREF_INT;
                    break;
                  case "string":
                    type = prefBranch.PREF_STRING;
                    break;
                  default:
                    type = prefBranch.PREF_INVALID;
                }
              }

              switch (type) {
                case prefBranch.PREF_BOOL:
                  prefBranch.setBoolPref(pref_name, value);
                  break;
                case prefBranch.PREF_STRING:
                  prefBranch.setCharPref(pref_name, value);
                  break;
                case prefBranch.PREF_INT:
                  prefBranch.setIntPref(pref_name, value);
                  break;
                default:
                  return false;
              }

              return true;
            """, script_args=[pref_name, value])

        assert retval

    def restore_all_prefs(self):
        """Restore all previously set preferences to their original value."""
        while len(self.archive):
            self.restore_pref(self.archive.keys()[0])

    def restore_pref(self, pref_name):
        """Restore a previously set preference to its original value.

        If the preference is not a default preference and has been newly
        created, it will be removed.

        :param name: The name of the preference to restore.
        """
        assert pref_name

        try:
            if self.archive[pref_name] is None:
                self.clear_user_pref(pref_name)
            else:
                self.set_pref(pref_name, self.archive[pref_name])

            del self.archive[pref_name]
        except KeyError:
            raise MarionetteException('Nothing to restore for preference "%s"',
                                      pref_name)
