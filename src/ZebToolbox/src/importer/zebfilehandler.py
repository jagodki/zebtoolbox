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
        elif name == "Datenstrom":
            if "Lfdm" in attrs:
                self.currentLfdm = attrs["Lfdm"]
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
        #elif name == "B":

    def characters(self, content):
        self.currentContent += content.strip()

    def endElement(self, name):
        if name == "B":
            if self.currentPictures == "":
                self.currentPictures = self.currentContent
            else:
                self.currentPictures += ";" + self.currentContent
            self.currentContent = ""

        elif name == "Datenstrom":
            self.addFeature(self.currentPosition.split(" ")[0],
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

    def addFeature(self, x, y, z, lfdm, pictures):
        #init the new feature
        feat = QgsFeature(self.pointLayer.pendingFields())
        feat.initAttributes(5)

        #insert the attributes of the new feature
        feat.setAttributes(["x", x])
        feat.setAttributes(["y", y])
        feat.setAttributes(["z", z])
        feat.setAttributes(["lfdm", lfdm])
        feat.setAttributes(["pictures", pictures])

        #create the geometry of the new feature
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(float(x), float(y))))

        #add the feature to the layer
        self.pointLayer.startEditing()
        self.pointLayer.addFeature(feat, True)
        self.pointLayer.commitChanges()
