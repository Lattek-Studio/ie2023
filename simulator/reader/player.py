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
    xSize = 0
    ySize = 0
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

    def getBlock(self, x, y):
        return self.fullMap[y * self.xSize + x]

    def isRobot(self, x, y):
        if (self.fullMap[y*self.xSize+x] == "0"):
            return True
        if (self.fullMap[y*self.xSize+x] == "1"):
            return True
        if (self.fullMap[y*self.xSize+x] == "2"):
            return True
        if (self.fullMap[y*self.xSize+x] == "3"):
            return True
        if (self.fullMap[y*self.xSize+x] == "4"):
            return True
        return False

    def hasBedrockNearby(self):
        if (self.getBlock(self.xCoord+1, self.yCoord) == "B"):
            return True
        if (self.getBlock(self.xCoord-1, self.yCoord) == "B"):
            return True
        if (self.getBlock(self.xCoord, self.yCoord+1) == "B"):
            return True
        if (self.getBlock(self.xCoord, self.yCoord-1) == "B"):
            return True
        # if (self.getBlock(self.xCoord+1, self.yCoord+1) == "B"):
        #     return True
        # if (self.getBlock(self.xCoord-1, self.yCoord-1) == "B"):
        #     return True
        # if (self.getBlock(self.xCoord+1, self.yCoord-1) == "B"):
        #     return True
        # if (self.getBlock(self.xCoord-1, self.yCoord+1) == "B"):
        #     return True
        return False

    def hasLavaNearby(self):
        if (self.getBlock(self.xCoord+1, self.yCoord) == "B"):
            return True
        if (self.getBlock(self.xCoord-1, self.yCoord) == "B"):
            return True
        if (self.getBlock(self.xCoord, self.yCoord+1) == "B"):
            return True
        if (self.getBlock(self.xCoord, self.yCoord-1) == "B"):
            return True
        if (self.getBlock(self.xCoord+1, self.yCoord+1) == "F"):
            return True
        if (self.getBlock(self.xCoord-1, self.yCoord-1) == "F"):
            return True
        if (self.getBlock(self.xCoord+1, self.yCoord-1) == "F"):
            return True
        if (self.getBlock(self.xCoord-1, self.yCoord+1) == "F"):
            return True
        return False

    def setZone(self, x, y):
        zone_width = min(abs(x-0), abs(x-self.xSize),
                         abs(y-0), abs(y-self.ySize))

        def setblocked(x, y):
            i = y*self.xSize+x
            self.fullMap = self.fullMap[:i] + \
                "F" + self.fullMap[i+1:]

        for x in range(0, zone_width):
            for y in range(0, self.ySize):
                setblocked(x, y)
        for x in range(zone_width, self.xSize):
            for y in range(self.ySize-zone_width, self.ySize):
                setblocked(x, y)
        for x in range(self.xSize-zone_width, self.xSize):
            for y in range(0, self.ySize-zone_width):
                setblocked(x, y)
        for x in range(zone_width, self.xSize-zone_width):
            for y in range(0, zone_width):
                setblocked(x, y)

        """self.fullMap
        ring = 0
        if (x > self.xSize // 2):
            ring = 2 * self.xSize - x
            return
        else:
            ring = x"""
        # fill ring
