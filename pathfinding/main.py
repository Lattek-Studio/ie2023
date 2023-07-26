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
            self.cleanString = map.replace(" ", "").replace("\n", "")

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
            if (self.get(x, y) == '1'):
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
            options = [
                {
                    'x': x,
                    'y': y - 1,
                    'sum': memoryMap[y - 1][x]['g'] + memoryMap[y - 1][x]['h'],
                    'h': memoryMap[y - 1][x]['h'],
                },
                {
                    'x': x,
                    'y': y + 1,
                    'sum': memoryMap[y + 1][x]['g'] + memoryMap[y + 1][x]['h'],
                    'h': memoryMap[y + 1][x]['h'],
                },
                {
                    'x': x - 1,
                    'y': y,
                    'sum': memoryMap[y][x - 1]['g'] + memoryMap[y][x - 1]['h'],
                    'h': memoryMap[y][x - 1]['h'],
                },
                {
                    'x': x + 1,
                    'y': y,
                    'sum': memoryMap[y][x + 1]['g'] + memoryMap[y][x + 1]['h'],
                    'h': memoryMap[y][x + 1]['h'],
                }
            ]
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
        for i in range(0, 1000):

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

            if (bestPath[-1]['x'] == endX and bestPath[-1]['y'] == endY):
                break

        printMemoryMap2()
        print(bestPath)
        return bestPath


test = Grid("""
        .1.............
        ...............
        ......1........
        ...............
        ...............
        .....1.........
        ...............
        .....1111......
        ...............
        .........1.....
        ...............
        ...............
        ...............
        ...............
        ...............
        """)

test.AStarPathfinding({
    'startX': 0,
    'startY': 0,
    'endX': 10,
    'endY': 10,
})
