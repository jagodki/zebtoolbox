# ZEB Toolbox
A <a href="https://github.com/qgis/QGIS">QGIS</a>-plugin as a toolbox for data of road monitoring and assessment in Germany (ZEB)

## Goal of the project
The data of road monitoring and assessment in Germany are stored in a specific XML-schema, which cannot be read by different GI-systems. This plugin enables QGIS to extract the spatial information from the XML-files called <i>Georohdaten</i> and <i>Rasterrohdaten</i> and display them as temporary layers (directly in memory).

## Change log
0.3.0 store the last selected filename for the next file dialog, usage of message bar of QGIS<br>
0.2.0 add new plugin icon<br>
0.1.2 remove ZIP from plugin<br>
0.1.1 remove error while installing plugin in QGIS<br>
0.1.0 import of one single ZEB-file realised<br>

## Preliminary remarks
The plugin runs in QGIS 2 and uses PyQt4 and Python 3.<br>
Just ZEB-files of the type <b>Rohdaten[...]Geo</b> can be displayed in QGIS.

## Hints for developement
The plugin was created by the QGIS-plugin "plugin builder". All additional python files were created in the <i>src</i>-folder.

### Import of ZEB-files
The python-files for the data import are stored in <i>src/importer</i>. The class <b>ImportController</b> creates two layers (one point-layer for storing the GPS-positions, one line-layer for storing the trajectory). The names of the layers are the file name. The attribute table of the point layer will be initialised in the following function of the <b>ImportController</b>-class:
```python
def createAttributeTable(self, layer):
    layerData = layer.dataProvider()
    layerData.addAttributes([QgsField("lfdm", QVariant.Int),
    QgsField("x", QVariant.Double),
    QgsField("y", QVariant.Double),
    QgsField("z", QVariant.Double),
    QgsField("pictures", QVariant.String)])
```
Each feature represents one <i>Datenstrom</i>-element from the XML-file. The attribute <i>lfdm</i> is the identifier of each feature, the attributes <i>x, y, z</i> contains the coordinates of the feature. The attribute <i>pictures</i> stores all path of pictures within one <i>Datenstrom</i>-element.

The class <b>ZebFileHandler</b> contains the SAX-implementation for extracting the data from the XML-file. Member variables are defind to store data until the end tag is find. The functions <i>startElement</i>, <i>characters</i> and <i>endElement</i> extracting the data and store them in the member variables. At the end of each <i>Datenstrom</i>-element, the following function for creating a new point feature will be called:
```python
def insertFeature(self, x, y, z, lfdm, pictures):
    #init the new feature
    feat = QgsFeature(self.pointLayer.pendingFields())

    #insert the attributes of the new feature
    feat.setAttribute("x", float(x))
    feat.setAttribute("y", float(y))
    feat.setAttribute("z", float(z))
    feat.setAttribute("lfdm", int(lfdm))
    feat.setAttribute("pictures", str(pictures))

    #create the geometry of the new feature
    feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(x), float(y))))

    #add the feature to the layer
    self.pointLayer.addFeatures([feat])
```
