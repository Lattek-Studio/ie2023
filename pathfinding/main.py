class Grid:
    xSize = 15
    ySize = 15
    map = """
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        000000000000000
        """
    cleanString = map.replace(" ", "").replace("\n", "")
    array = []

    def __init__(self, map):
        if (map != None):
            self.map = map
        self.generateArrayfromMapString()

    def setMap(self, map):
        self.map = map
        self.generateArrayfromMapString()

    def generateArrayfromMapString(self):
        for y in range(0, self.xSize):
            for x in range(0, self.ySize):
                self.array.append(self.cleanString[y * self.xSize + x])

    def get(self, x, y):
        if (x < 0 or y < 0 or x >= self.xSize or y >= self.ySize):
            return None
        return self.array[y * self.xSize + x]

    def set(self, x, y, value):
        if (x < 0 or y < 0 or x >= self.xSize or y >= self.ySize):
            return None
        self.array[y * self.xSize + x] = value


test = Grid("""
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        ...............
        """)


print(len(test.array))
