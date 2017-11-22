from xml.sax import handler
from qgis.core import QgsFeature, QgsGeometry, QgsPoint

class ZebFileHandler(handler.ContentHandler):

    def __init__(self):
        self.fileType = ""
        self.currentPictures = ""
        self.currentLfdm = ""
        self.currentContent = ""
        self.pointLayer = ""
        self.currentPosition = ""

    def startElement(self, name, attrs):
        if name == "":
            self.fileType = "geo"
        elif name == "":
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
        feat = QgsFeature(self.pointLayer.pendingFields())

        #insert the attributes of the new feature
        feat.setAttributes(["x", float(x)])
        feat.setAttributes(["y", float(y)])
        feat.setAttributes(["z", float(z)])
        feat.setAttributes(["lfdm", int(lfdm)])
        feat.setAttributes(["pictures", str(pictures)])

        #create the geometry of the new feature
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(x), float(y))))

        #add the feature to the layer
        print("F:", feat.id(), feat.attributes(), feat.geometry().asPoint())
        self.pointLayer.addFeatures([feat])
