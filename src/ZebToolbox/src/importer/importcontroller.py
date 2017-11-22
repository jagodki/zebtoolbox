from xml.sax import make_parser
import zebfilehandler as zfh
import os
from qgis.core import QgsVectorLayer, QgsField, QgsMapLayerRegistry
from PyQt4.QtCore import QVariant
from qgis.core import QgsFeature, QgsGeometry, QgsPoint

class ImportController:

    def __init__(self):
        self.zebFileHandler = zfh.ZebFileHandler()

    def importZebFile(self,path):
        #get the filename
        filename = os.path.basename(path).split(".")[0]

        #create a new point- and line-layer
        lineLayer = QgsVectorLayer("LineString", filename + "_trajetory", "memory")
        pointLayer = QgsVectorLayer("Point", filename + "_positions", "memory")

        #show both layers in QGIS
        QgsMapLayerRegistry.instance().addMapLayer(lineLayer)
        QgsMapLayerRegistry.instance().addMapLayer(pointLayer)

        #start editing of the layer
        pointLayer.startEditing()

        #create the attribute table for the point layer (line layer has no attributes, just one geometry)
        self.createAttributeTable(pointLayer)

        #add the point layer to the content handler
        self.zebFileHandler.setPointLayer(pointLayer)

        #parse the XML-file
        parser = make_parser()
        parser.setContentHandler(self.zebFileHandler)
        parser.parse(path)


        feat = QgsFeature(pointLayer.pendingFields())
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(10.0, 10.0)))

        #commit editing on layer
        pointLayer.commitChanges()

        #update layer's extent
        pointLayer.updateExtents()

        print("Fertig")

    def createAttributeTable(self, layer):
        #layer.startEditing()
        layerData = layer.dataProvider()
        layerData.addAttributes([QgsField("lfdm", QVariant.Int),
                                 QgsField("x", QVariant.Double),
                                 QgsField("y", QVariant.Double),
                                 QgsField("z", QVariant.Double),
                                 QgsField("pictures", QVariant.String)])
        layer.updateFields()
        #layer.commitChanges()
