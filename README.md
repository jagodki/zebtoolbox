# ZEB Toolbox
A <a href="https://github.com/qgis/QGIS">QGIS</a>-plugin as a toolbox for data of road monitoring and assessment in Germany (ZEB)

## Goal of the project
The data of road monitoring and assessment in Germany are stored in a specific XML-schema, which cannot be read by different GI-systems. This plugin enables QGIS to extract the spatial information from the XML-files called <i>Georohdaten</i> and <i>Rasterrohdaten</i> and display them as temporary layers (directly in memory).

## Preliminary remarks
The plugin can be used in QGIS 2, i.e. it depends on PyQt4.
The extraction of data from XML is realised by using SAX.
