# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZebToolbox
                                 A QGIS plugin
 toolbox for data of road monitoring and assessment in Germany (ZEB)
                              -------------------
        begin                : 2017-11-17
        git sha              : $Format:%H$
        copyright            : (C) 2017 by https://github.com/jagodki
        email                : https://github.com/jagodki/zebtoolbox
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from qgis.gui import QgsMessageBar
from qgis.core import *
import sys, traceback
from .zeb_toolbox_dialog import ZebToolboxDialog
import os.path
from .src.importer.importcontroller import ImportController


class ZebToolbox:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ZebToolbox_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ZebToolboxDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ZEB Toolbox')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ZebToolbox')
        self.toolbar.setObjectName(u'ZebToolbox')
        self.dlg.lineEditSelectZebFile.clear()
        self.dlg.pushButtonSelectZebFile.clicked.connect(self.selectZebFileFromFileDialog)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ZebToolbox', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ZebToolbox/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'ZEB Toolbox'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ZEB Toolbox'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            try:
                zebFilePath = self.dlg.lineEditSelectZebFile.text()
                importController = ImportController()
                importController.importZebFile(zebFilePath)
                self.iface.messageBar().pushMessage("Info", "ZEB-file imported.", level=Qgis.Success, duration=10)
            except:
                e = sys.exc_info()[0]
                self.iface.messageBar().pushMessage("Error", "Import of ZEB-file failed. Look into the python console for the stack trace.", level=Qgis.Critical)
                QgsMessageLog.logMessage(traceback.print_exc(), level=Qgis.Critical)


    def selectZebFileFromFileDialog(self):
        s = QSettings()
        filename, _filter = QFileDialog.getOpenFileName(self.dlg, "Select ZEB file ", s.value("qgis_zebtoolbox_input_file", ""), '*.xml')
        self.dlg.lineEditSelectZebFile.setText(filename)
        s.setValue("qgis_zebtoolbox_input_file", filename)
