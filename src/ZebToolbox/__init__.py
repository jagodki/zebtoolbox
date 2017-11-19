# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZebToolbox
                                 A QGIS plugin
 toolbox for data of survey and evaluation of road conditions in Germany (ZEB)
                             -------------------
        begin                : 2017-11-17
        copyright            : (C) 2017 by https://github.com/jagodki
        email                : https://github.com/jagodki/zebtoolbox
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ZebToolbox class from file ZebToolbox.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .zeb_toolbox import ZebToolbox
    return ZebToolbox(iface)
