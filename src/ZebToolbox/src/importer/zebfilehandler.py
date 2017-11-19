from xml.sax import handler
import georohdata as gd
import rasterrohdata as rd

class ZebFileHandler(handler.ContentHandler):

    def __init__(self):
        self.fileType = " "
        self.georohData = gd.GeorohData()
        self.rasterrohData = rd.RasterrohData()
        self.currentPictures = []
        self.currentLfdm = ""
        self.currentContent = ""
        self.pointLayer = ""

    def startElement(self, name, attrs):
        if name == "":
            self.fileType = "geo"
        elif name == "":
            self.fileType = "raster"
        elif name == "Datenstrom":
            if "Lfdm" in attrs:
                self.currentLfdm = attrs["Lfdm"]
                if self.fileType == "geo":
                    self.georohData.addLfdm(self.currentLfdm)
                elif self.fileType == "raster":
                    self.rasterrohData.addLfdm(self.currentLfdm)
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

            if self.fileType == "geo" and self.currentLfdm != "":
                self.georohData.setCoordinates(self.currentLfdm, x + " " + y + " " + z)
            elif self.fileType == "raster" and self.currentLfdm != "":
                self.rasterrohData.setCoordinates(self.currentLfdm, x + " " + y + " " + z)
        #elif name == "B":

    def characters(self, content):
        self.currentContent += content.strip()

    def endElement(self, name):
        if name == "B":
            self.currentPictures.append(self.currentContent)
            self.currentContent = ""

        elif name == "Datenstrom":
            if self.fileType == "geo" and self.currentLfdm != "":
                self.georohData.setPicture(self.currentLfdm, self.currentPictures)
            elif self.fileType == "raster" and self.currentLfdm != "":
                self.rasterrohData.setCoordinates(self.currentLfdm, self.currentPictures)

            self.currentLfdm = ""
            self.currentContent = ""
            self.currentPictures = []

    def getFileType(self):
        return self.fileType

    def getGeorohData(self):
        return self.georohData

    def getRasterrohData(self):
        return self.rasterrohData

    def setPointLayer(self, pointLayer):
        self.pointLayer = pointLayer
