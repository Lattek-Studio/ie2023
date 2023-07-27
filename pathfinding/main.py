class Grid:
    xSize = 15
    ySize = 15
    xCoord = 0
    yCoord = 0
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
        """.replace(" ", "").replace("\n", "")
    array = []

    def __init__(self, map, xSize=15, ySize=15):
        if (map != None):
            self.setMap(map, xSize, ySize)

    def setPlayer(self, x, y):
        self.xCoord = x
        self.yCoord = y

    def setMap(self,  map, xSize=15, ySize=15):
        if (map == None):
            return
        self.map = map.replace(" ", "").replace("\n", "")
        self.xSize = xSize
        self.ySize = ySize

    def get(self, x, y):
        if (x < 0 or y < 0 or x >= self.xSize or y >= self.ySize):
            return None
        return self.map[y * self.xSize + x]

    def set(self, x, y, value):
        if (x < 0 or y < 0 or x >= self.xSize or y >= self.ySize):
            return None
        position = y * self.xSize + x
        self.map = self.map[:position] + value[0] + self.map[position+1:]

    def isSolid(self, x, y):

        item = self.get(x, y)

        if (self.map[self.yCoord*self.xSize+self.xCoord] == 'F'):
            if (item == "F"):
                return True
        # if (item == 'X'):
        #     return True
        # if (item == 'A'):
        #     return True
        if (item == 'B'):
            return True
        # if (item == '?'):
        #     return True
        if (item == 'F'):
            return True

        if (self.get(x-1, y) == 'F' or self.get(x, y-1) == 'F' or self.get(x+1, y) == 'F' or self.get(x, y+1) == 'F'):
            return True

        # if (item == "0" or item == "1" or item == "2" or item == "3" or item == "4"):
        #     return True
        # if (self.get(x-1, y) == '0' or self.get(x, y-1) == '0' or self.get(x+1, y) == '0' or self.get(x, y+1) == '0'):
        #     return True
        # if (self.get(x-1, y) == '1' or self.get(x, y-1) == '1' or self.get(x+1, y) == '1' or self.get(x, y+1) == '1'):
        #     return True
        # if (self.get(x-1, y) == '2' or self.get(x, y-1) == '2' or self.get(x+1, y) == '2' or self.get(x, y+1) == '2'):
        #     return True
        # if (self.get(x-1, y) == '3' or self.get(x, y-1) == '3' or self.get(x+1, y) == '3' or self.get(x, y+1) == '3'):
        #     return True
        # if (self.get(x-1, y) == '4' or self.get(x, y-1) == '4' or self.get(x+1, y) == '4' or self.get(x, y+1) == '4'):
        #     return True

        return False

    def print(self):
        for y in range(0, self.ySize):
            for x in range(0, self.xSize):
                item = self.get(x, y)
                print(item, end='')
            print("")

    def AStarPathfinding(self, data={
        'startX': 0,
        'startY': 0,
        'endX': 0,
        'endY': 0,
    }):
        startX = data['startX']
        startY = data['startY']
        endX = data['endX']
        endY = data['endY']
        # create memory map
        memoryMap = []
        for y in range(0, self.ySize):
            memoryMap.append([])
            for x in range(0, self.xSize):
                memoryMap[y].append({
                    'g': 10000000,
                    'h': 10000000,
                })

        def calculateH(x, y):
            return abs(endX - x) + abs(endY - y)

        def exists(x, y):
            if (self.isSolid(x, y)):
                return False
            return x >= 0 and y >= 0 and x < self.xSize and y < self.ySize

        def printMemoryMap():
            for y in range(0, self.ySize):
                for x in range(0, self.xSize):
                    if (exists(x, y) == False):
                        print('[  not  ]', end='')
                        continue
                    item = memoryMap[y][x]
                    sum = item['g']
                    if (sum >= 10000000):
                        sum = '0'
                    extra = ' ' * (3 - len(str(sum)))

                    sum2 = item['h']
                    if (sum2 >= 10000000):
                        sum2 = '0'
                    extra2 = ' ' * (3 - len(str(sum2)))
                    sum = '[' + str(sum) + extra + ' ' + \
                        str(sum2) + extra2 + ']'
                    print(sum, end='')
                print("")

        def printMemoryMap2():
            for y in range(0, self.ySize):
                for x in range(0, self.xSize):
                    if (exists(x, y) == False):
                        print('[   ]', end='')
                        continue
                    item = memoryMap[y][x]
                    sum = item['g'] + item['h']
                    if (sum >= 10000000):
                        sum = '0'
                    extra = ' ' * (3 - len(str(sum)))

                    sum = '[' + str(sum) + extra + ']'
                    print(sum, end='')
                print("")

        memoryMap[startY][startX] = {
            'g': 0,
            'h': calculateH(startX, startY),
        }

        def setParentProp(x, y, parentX, parentY):
            memoryMap[y][x]['parent'] = {
                'x': parentX,
                'y': parentY,
            }

        def expand(x, y):
            parent = memoryMap[y][x]['parent']
            parentX = parent['x']
            parentY = parent['y']
            newG = memoryMap[parentY][parentX]['g'] + 1
            newH = calculateH(x, y)
            if (newG + newH < memoryMap[y][x]['g'] + memoryMap[y][x]['h']):
                memoryMap[y][x] = {
                    'g': newG,
                    'h': newH,
                }
                setParentProp(x, y, parentX, parentY)
            elif (newG + newH == memoryMap[y][x]['g'] + memoryMap[y][x]['h']):
                if (newH < memoryMap[y][x]['h']):
                    memoryMap[y][x] = {
                        'g': newG,
                        'h': newH,
                    }
                    setParentProp(x, y, parentX, parentY)

        def check(x, y):
            currentPosition = memoryMap[y][x]
            if exists(x, y - 1):
                setParentProp(x, y - 1, x, y)
                expand(x, y - 1)
            if exists(x, y + 1):
                setParentProp(x, y + 1, x, y)
                expand(x, y + 1)

            if exists(x - 1, y):
                setParentProp(x - 1, y, x, y)
                expand(x - 1, y)

            if exists(x + 1, y):
                setParentProp(x + 1, y, x, y)
                expand(x + 1, y)

        def findBestNextCheck(x, y):
            options = []
            if (not x == self.xSize-1):
                options.append(
                    {
                        'x': x + 1,
                        'y': y,
                        'sum': memoryMap[y][x + 1]['g'] + memoryMap[y][x + 1]['h'],
                        'h': memoryMap[y][x + 1]['h'],
                    }
                )
            if (not y == self.ySize-1):
                options.append(
                    {
                        'x': x,
                        'y': y + 1,
                        'sum': memoryMap[y + 1][x]['g'] + memoryMap[y + 1][x]['h'],
                        'h': memoryMap[y + 1][x]['h'],
                    }
                )
            if (not x == 0):
                options.append(
                    {
                        'x': x - 1,
                        'y': y,
                        'sum': memoryMap[y][x - 1]['g'] + memoryMap[y][x - 1]['h'],
                        'h': memoryMap[y][x - 1]['h'],
                    }
                )

            if (not y == 0):
                options.append(
                    {
                        'x': x,
                        'y': y - 1,
                        'sum': memoryMap[y - 1][x]['g'] + memoryMap[y - 1][x]['h'],
                        'h': memoryMap[y - 1][x]['h'],
                    }
                )

            filtered_options = [
                option for option in options if exists(option['x'], option['y'])]

            filtered_options.sort(key=lambda x: int(x['sum']))
            filtered_options.sort(key=lambda x: int(x['h']))

            return filtered_options

        bestPath = []
        bestPath.append({
            'x': startX,
            'y': startY,
        })
        for i in range(0, 100):

            check(bestPath[-1]['x'], bestPath[-1]['y'])
            matches = findBestNextCheck(bestPath[-1]['x'], bestPath[-1]['y'])
            # print(matches)
            matches = [match for match in matches if not bestPath.count(
                {'x': match['x'], 'y': match['y']})]

            # print(matches)
            if (len(matches) > 0):
                bestPath.append({
                    'x': matches[0]['x'],
                    'y': matches[0]['y'],
                })
            else:
                bestPath.pop()

            if (len(bestPath) == 0):
                print("No path found")
                return []
            if (bestPath[-1]['x'] == endX and bestPath[-1]['y'] == endY):
                break

        # printMemoryMap2()
        print(bestPath)
        return bestPath


# test = Grid("""
#         .B.............
#         .B.............
#         ......B........
#         ...............
#         BBBB...........
#         ....BB.........
#         ...............
#         .....BBBB......
#         ...............
#         .........1.....
#         ...............
#         ...............
#         ...............
#         ...............
#         ...............
#         """)

# test.AStarPathfinding({
#     'startX': 0,
#     'startY': 0,
#     'endX': 10,
#     'endY': 10,
# })
