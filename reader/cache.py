class Cake:
    xSize = 0
    ySize = 0
    reading = ""
    map = ""

    def addReading(self, reading):
        self.reading = reading

        data = self.reading.read().split("\n")
