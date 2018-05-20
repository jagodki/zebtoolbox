from xml.sax import handler
from qgis.core import *

class ZebFileHandler(handler.ContentHandler):

    def __init__(self):
        self.fileType = ""
        self.currentPictures = ""
        self.currentLfdm = ""
        self.currentContent = ""
        self.pointLayer = ""
        self.currentPosition = ""

    def startElement(self, name, attrs):
        if "Rohdaten" in name:
            if "Typ" in attrs:
                if "Geoorientiert" in attrs["Typ"]:
                    self.fileType = "geo"
                elif "Rasterorientiert" in attrs["Typ"]:
                    self.fileType = "raster"
        #elif name == "Datenstrom":

        elif name == "WGS":
            x = ""
            y = ""
            z = ""

            if "L" in attrs:
                x = attrs["L"]
            if "B" in attrs:
                y = attrs["B"]
            if "H_WGS" in attrs:
                z = attrs["H_WGS"]

            self.currentPosition = x + " " + y + " " + z

            if "LfdM" in attrs:
                self.currentLfdm = attrs["LfdM"]
        elif name == "B":
            if "D" in attrs:
                if self.currentPictures == "":
                    self.currentPictures = attrs["D"]
                else:
                    self.currentPictures += ";" + attrs["D"]

    def characters(self, content):
        self.currentContent += content.strip()

    def endElement(self, name):
        if name == "Datenstrom":
            self.insertFeature(self.currentPosition.split(" ")[0],
                               self.currentPosition.split(" ")[1],
                               self.currentPosition.split(" ")[2],
                               self.currentLfdm,
                               self.currentPictures)

            self.currentLfdm = ""
            self.currentContent = ""
            self.currentPictures = ""

    def getFileType(self):
        return self.fileType

    def setPointLayer(self, pointLayer):
        self.pointLayer = pointLayer

    def insertFeature(self, x, y, z, lfdm, pictures):
        #init the new feature
        feat = QgsFeature(self.pointLayer.fields())

        #insert the attributes of the new feature
        feat.setAttribute("x", float(x))
        feat.setAttribute("y", float(y))
        feat.setAttribute("z", float(z))
        feat.setAttribute("lfdm", int(lfdm))
        feat.setAttribute("pictures", str(pictures))

        #create the geometry of the new feature
        feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(x), float(y))))

        #add the feature to the layer
        self.pointLayer.addFeatures([feat])
