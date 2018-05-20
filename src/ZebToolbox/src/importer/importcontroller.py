from xml.sax import make_parser
from .zebfilehandler import ZebFileHandler
import os
#from qgis.core import QgsVectorLayer, QgsField, QgsMapLayerRegistry
from qgis.core import *
from PyQt5.QtCore import QVariant
#from qgis.core import QgsFeature, QgsGeometry, QgsPoint

class ImportController:

    def __init__(self):
        self.zebFileHandler = ZebFileHandler()

    def importZebFile(self,path):
        #get the filename
        filename = os.path.basename(path).split(".")[0]

        #create a new point- and line-layer
        lineLayer = QgsVectorLayer("LineString", filename + "_trajectory", "memory")
        pointLayer = QgsVectorLayer("Point", filename + "_positions", "memory")

        #show both layers in QGIS
        QgsProject.instance().addMapLayer(lineLayer)
        QgsProject.instance().addMapLayer(pointLayer)

        #start editing of the layers
        pointLayer.startEditing()
        lineLayer.startEditing()

        #create the attribute table for the point layer (line layer has no attributes, just one geometry)
        self.createAttributeTable(pointLayer)

        #add the point layer to the content handler
        self.zebFileHandler.setPointLayer(pointLayer)

        #parse the XML-file
        parser = make_parser()
        parser.setContentHandler(self.zebFileHandler)
        parser.parse(path)

        #create a trajectory with the coordinates of the point layer as vertices
        self.createTrajectoryFromPointLayer(pointLayer, lineLayer)

        #commit editing on layer
        pointLayer.commitChanges()
        lineLayer.commitChanges()

        #deselect all features from the new layers
        self.deselectFeatures(pointLayer)
        self.deselectFeatures(lineLayer)

        #update layer's extent
        pointLayer.updateExtents()

    def createAttributeTable(self, layer):
        layerData = layer.dataProvider()
        layerData.addAttributes([QgsField("lfdm", QVariant.Int),
                                 QgsField("x", QVariant.Double),
                                 QgsField("y", QVariant.Double),
                                 QgsField("z", QVariant.Double),
                                 QgsField("pictures", QVariant.String)])
        layer.updateFields()

    def createTrajectoryFromPointLayer(self, pointLayer, lineLayer):
        vertices = []
        pointFeatures = pointLayer.getFeatures()

        #extract all point coordinates from the point layer and inserts them into the list of vertices
        for pf in pointFeatures:
            vertices.append(pf.geometry().asPoint())

        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolylineXY(vertices))
        lineLayer.addFeatures([feature])

    def deselectFeatures(self, layer):
        layer.select([])
