# Copyright 2013 Raihan Kibria
#
# This file is part of Pyco https://github.com/rkibria/Pyco
#
# Pyco is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyco is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyco.  If not, see <http://www.gnu.org/licenses/>.

import kivy.config

_appname = "pyco"
_configfile = None

def open():
    global _configfile
    global _appname
    _configfile = kivy.config.ConfigParser()
    _configfile.read(_appname + ".ini")
    _configfile.adddefaultsection(_appname)
    
def get_int(varname, defaultvalue = 0):
    storedvalue = int(_configfile.getdefault(_appname, varname, defaultvalue))
    _configfile.set(_appname, varname, str(storedvalue))
    _configfile.write()
    return storedvalue
    
def set_int(varname, value):
    global _configfile
    global _appname
    _configfile.set(_appname, varname, str(value))
    _configfile.write()
