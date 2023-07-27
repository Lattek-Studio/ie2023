class Path:
    oldpath = []
    oldPosX = -1
    oldPosY = -1
    playerX = -1
    playerY = -1

    def setPlayerPos(self, x, y):
        self.playerX = x
        self.playerY = y

    def setPath(self, path):
        self.oldpath = path

    def setCoords(self, pointGoalX, pointGoalY):
        self.oldPosX = pointGoalX
        self.oldPosY = pointGoalY

    def updateRemove(self):
        if (self.playerX == -1 or self.playerY == -1):
            return
        if (not len(self.oldpath) > 0):
            return
        # if (not self.oldpath[0][0] == self.playerX and not self.oldpath[0][1] == self.playerY):
        self.oldpath.pop(0)
