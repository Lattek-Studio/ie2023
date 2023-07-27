from pathfinding.spiral import get_spiral_traj


class Spiral:
    generated = False
    spiralData = []
    fullMap = ""
    xSize = 0
    ySize = 0
    homeX = 0
    homeY = 0

    def clear(self):
        self.spiralData = []

    def setHome(self, x, y):
        self.homeX = x
        self.homeY = y

    def setSize(self, x, y):
        self.xSize = x
        self.ySize = y

    def addMap(self, map, x, y):
        if (map == ""):
            return
        self.fullMap = map
        self.xSize = x
        self.ySize = y
        for point in self.spiralData:
            if point[0] < 0 or point[0] >= self.xSize or point[1] < 0 or point[1] >= self.ySize:
                self.spiralData.remove(point)
        for point in self.spiralData:
            if self.fullMap[point[1] * self.xSize + point[0]] == 'B':
                # delete everything that comes before point in spiral
                i = 0
                while (i <= len(self.spiralData)-1):
                    if (self.spiralData[0] == point):
                        break
                    self.spiralData.pop(0)
                    i = i+1
                self.spiralData.pop(0)

        for point in self.spiralData:
            if not self.fullMap[point[1] * self.xSize + point[0]] == '?':
                i = 0
                while (i <= len(self.spiralData)-1):
                    if (self.spiralData[0] == point):
                        break
                    self.spiralData.pop(0)
                    i = i+1
                self.spiralData.pop(0)

    def createSpiral(self):
        print("ADD SPIRAL>>>>>>>>>>>>>>>")
        self.spiralData = get_spiral_traj(
            6, 6, self.homeX, self.homeY, self.xSize, self.ySize)

        for point in self.spiralData:
            i = 0
            while (i <= len(self.spiralData)-1):
                x = self.spiralData[i][0]
                y = self.spiralData[i][1]
                if (x < 0 or x >= self.xSize or y < 0 or y >= self.ySize):
                    self.spiralData.pop(i)

                i = i+1

        self.generated = True
