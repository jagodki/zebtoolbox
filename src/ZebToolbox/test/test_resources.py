# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'https://github.com/jagodki/zebtoolbox'
__date__ = '2017-11-17'
__copyright__ = 'Copyright 2017, https://github.com/jagodki'

import unittest

from PyQt4.QtGui import QIcon



class ZebToolboxDialogTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    def test_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/ZebToolbox/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())

if __name__ == "__main__":
    suite = unittest.makeSuite(ZebToolboxResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)



