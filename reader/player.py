from reader.goals import Goal, GoalSystem


class Perseus:
    tura = 0
    map = ""
    reading = ""
    fullMap = ""
    homeX = ""
    homeY = ""
    xCoord = ""
    yCoord = ""
    goals = GoalSystem()

    def generateUnknown(self):
        unknown = ""
        for i in range(0, self.xSize * self.ySize):
            unknown += "?"
        return unknown

    def combineMaps(self):
        if (self.fullMap == ""):
            self.fullMap = self.generateUnknown()

        for i in range(0, len(self.map)):
            if (self.map[i] != "?"):
                self.fullMap = self.fullMap[:i] + \
                    self.map[i] + self.fullMap[i+1:]

    def addReading(self, reading):
        if (len(reading) == 0):
            return
        self.reading = reading.strip().lstrip()
        file = reading.strip().lstrip().split("\n")
        size = file[0]
        self.xSize = int(size.split(" ")[0])
        self.ySize = int(size.split(" ")[1])

        self.map = ''
        for i in range(1, self.ySize + 1):
            self.map += file[i].replace(" ", "")

        coords = file[self.ySize + 1]

        self.xCoord = int(coords.split(" ")[0])
        self.yCoord = int(coords.split(" ")[1])

        if (self.tura == 0):
            self.setHome(self.xCoord, self.yCoord)

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

        # update dependency
        self.combineMaps()

    def printFullMap(self):
        if (self.fullMap == ""):
            return
        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                item = self.fullMap[y * self.xSize + x]
                print(item, end='')
            print("")
        if (self.homeX == "" or self.homeY == ""):
            return
        print('HOME: ', self.homeX, self.homeY)
        if (self.xCoord == "" or self.yCoord == ""):
            return
        print('COORDS: ', self.xCoord, self.yCoord)

    def setTura(self, tura):
        self.tura = tura

    def setHome(self, x, y):
        self.homeX = x
        self.homeY = y
