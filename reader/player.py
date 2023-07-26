class Perseus:
    reading = ""

    def addReading(self, reading):
        self.reading = reading

        file = self.reading.read().split("\n")

        size = file[0]

        self.xSize = int(size.split(" ")[0])
        self.ySize = int(size.split(" ")[1])

        self.map = ''
        for i in range(1, self.ySize):
            self.map += file[i]

        coords = file[self.ySize + 1]

        self.xCoord = int(coords.split(" ")[0])
        self.yCoord = int(coords.split(" ")[1])

        abilities = file[self.ySize + 2]

        self.health = int(abilities.split(" ")[0])
        self.dig = int(abilities.split(" ")[1])
        self.attack = int(abilities.split(" ")[2])
        self.move = int(abilities.split(" ")[3])
        self.vision = int(abilities.split(" ")[4])
        self.scan = int(abilities.split(" ")[5])
        self.battery = int(abilities.split(" ")[6])

        resources = file[self.ySize + 3]

        self.cobblestone = int(resources.split(" ")[0])
        self.iron = int(resources.split(" ")[1])
        self.osmium = int(resources.split(" ")[2])
