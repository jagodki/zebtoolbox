# ZEB Toolbox
A <a href="https://github.com/qgis/QGIS">QGIS</a>-plugin as a toolbox for data of road monitoring and assessment in Germany (ZEB)

## Goal of the project
The data of road monitoring and assessment in Germany are stored in a specific XML-schema, which cannot be read by different GI-systems. This plugin enables QGIS to extract the spatial information from the XML-files called <i>Georohdaten</i> and <i>Rasterrohdaten</i> and display them as temporary layers (directly in memory).

## Preliminary remarks
The plugin runs in QGIS 2 and uses PyQt4 and Python 3.

## Hints for developement
The plugin was created by the QGIS-plugin "plugin builder". All additional python files were created in the <i>src</i>-folder.

### Import of ZEB-files
The python-files for the data import are stored in <i>src/importer</i>. The class <b>ImportController</b> creates two layers (one point-layer for storing the GPS-positions, one line-layer for storing the trajectory). The names of the layers are the file name. The attribute table of the point layer will be initialised in the following function of the ImportController-class:
```python
def createAttributeTable(self, layer):
    layerData = layer.dataProvider()
    layerData.addAttributes([QgsField("lfdm", QVariant.Int),
    QgsField("x", QVariant.Double),
    QgsField("y", QVariant.Double),
    QgsField("z", QVariant.Double),
    QgsField("pictures", QVariant.String)])
```

