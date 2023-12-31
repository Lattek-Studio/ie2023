from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import random
from reader.player import Perseus
from reader.goals import Goal
from pathfinding.main import Grid
from pathfinding.spiralmemory import Spiral
from pathfinding.path import Path

player = Perseus()
player.goals.addGoal(Goal("goOffset", {"x": -1, "y": 0}))
grid = Grid("")
pathManager = Path()
spiralMemory = Spiral()
# function triggered by file creation


def funky(read_file_path, tura):
    # system lines
    read_input = open(read_file_path, "r")
    input = read_input.read()

    # update storage
    player.setTura(tura)
    player.addReading(input)
    grid.setPlayer(player.xCoord, player.yCoord)
    grid.setMap(player.fullMap, player.xSize, player.ySize)
    pathManager.setPlayerPos(player.xCoord, player.yCoord)

    # pathManager.updateRemove()

    # update spiral engine
    spiralMemory.setHome(player.homeX, player.homeY)
    spiralMemory.setSize(player.xSize, player.ySize)
    if (not spiralMemory.generated):
        spiralMemory.createSpiral()
        pathManager.setPath([])

    spiralMemory.addMap(player.fullMap, player.xSize, player.ySize)

    # update zone long term memory

    if (player.map.count("F")):
        indexes_dict = {'F': []}
        for i, char in enumerate(player.map):
            if char in indexes_dict:
                indexes_dict[char].append(i)
        for index in indexes_dict['F']:
            xZone = index % player.xSize
            yZone = index // player.xSize
            player.setZone(xZone, yZone)

    # default variables
    randomPosibilities = [-4, -3, -2, -2, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          1, 1, 1, 2, 2, 3, 4]
    randomPosibilities = [0, 0, 0]
    pointGoalX = player.xSize // 2
    pointGoalY = player.ySize // 2
    positionSource = "first middle"

    # get middle direction optimized path

    middleX = player.xSize // 2
    middleY = player.ySize // 2
    randomDistance = random.randint(0, 1)
    if (player.getBlock(middleX, middleY) == '?'):
        xOffset = middleX - player.xCoord
        yOffset = middleY - player.yCoord
        if (xOffset > 0):
            xOffset = 1
        elif (xOffset < 0):
            xOffset = -1
        if (yOffset > 0):
            yOffset = 1
        elif (yOffset < 0):
            yOffset = -1
        pointGoalX = player.xCoord + xOffset * randomDistance
        pointGoalY = player.yCoord + yOffset * randomDistance
    positionSource = "random middle"

    # old spiral magic
    # spiral = get_spiral_traj(
    #     6, 4, player.homeX, player.homeY, player.xSize, player.ySize)
    # # print(spiral)
    # if (player.fullMap[player.homeY * player.xSize + player.homeX] == 'F'):
    #     spiral = []
    # filtered = []
    # # remove spiral point that are ? in player.fullMap
    # if (not player.fullMap == ""):

    #     for point in spiral:
    #         if point[0] < 0 or point[0] >= player.xSize or point[1] < 0 or point[1] >= player.ySize:
    #             spiral.remove(point)
    #         elif not player.fullMap[point[1] * player.xSize + point[0]] == '?':
    #             spiral.remove(point)
    #         elif player.fullMap[point[1] * player.xSize + point[0]] == 'B':
    #             spiral.remove(point)
    #         elif player.fullMap[point[1] * player.xSize + point[0]] == 'F':
    #             spiral.remove(point)
    #         else:
    #             filtered.append(point)
    #     if (len(filtered) > 0):
    #         pointGoalX = filtered[0][0]
    #         pointGoalY = filtered[0][1]
    #         positionSource = "SPIRAL"
    #         print(
    #             "BLOCK: ", player.fullMap[filtered[0][1] * player.xSize + filtered[0][0]])
    #         print(
    #             "BLOCK PLAYER: ", player.fullMap[player.yCoord * player.xSize + player.xCoord])
    #         print("SPIRAL: ", filtered[0][0], filtered[0][1])
    # print(filtered)
    if (not player.hasBedrockNearby()):
        randomPosibilities = [0, 0, 0]
    print(spiralMemory.spiralData)
    if (len(spiralMemory.spiralData) > 0):

        pointGoalX = spiralMemory.spiralData[0][0] + \
            randomPosibilities[random.randint(0, len(randomPosibilities) - 1)]
        pointGoalY = spiralMemory.spiralData[0][1] + \
            randomPosibilities[random.randint(0, len(randomPosibilities) - 1)]
        positionSource = "SPIRAL"
        print(
            "BLOCK: ", player.fullMap[spiralMemory.spiralData[0][1] * player.xSize + spiralMemory.spiralData[0][0]])
        print(
            "BLOCK PLAYER: ", player.fullMap[player.yCoord * player.xSize + player.xCoord])
        print("SPIRAL: ",
              spiralMemory.spiralData[0][0], spiralMemory.spiralData[0][1])

    if (player.map.count("C") or player.map.count("D")):
        # find ore coords
        map = player.map
        indexes_dict = {'C': [], 'D': []}

        for i, char in enumerate(map):
            if char in indexes_dict:
                indexes_dict[char].append(i)

        allOres = indexes_dict['C'] + indexes_dict['D']

        # find closest ore
        minOre = 10000000
        for ore in allOres:
            # find x and y
            oreX = ore % player.xSize
            oreY = ore // player.xSize

            # find distance
            distance = len(grid.AStarPathfinding({
                'startX': player.xCoord,
                'startY': player.yCoord,
                'endX': oreX,
                'endY': oreY,
            }))

            if (distance < minOre):
                minOre = distance
                pointGoalX = oreX
                pointGoalY = oreY
                positionSource = "ORE"

        print(indexes_dict)
    buy = ""
    if (player.iron > 0 and player.osmium > 0 and not player.battery):
        pointGoalX = player.homeX
        pointGoalY = player.homeY
        positionSource = "HOME BUY BATTERY"

        if (abs(player.xCoord - pointGoalX) <= 1 and abs(player.yCoord - pointGoalY) <= 1):
            buy = " b b"
    if (player.iron >= 3 and player.battery == 1):
        buy = " b a"
    if (player.health < 5 and player.osmium):
        buy = " b h"
    if (player.health < 10 and player.battery and player.osmium):
        buy = " b h"

    if (player.battery):
        spiralMemory.clear()
    # atack

    # pointGoalX = player.xSize // 2
    # pointGoalY = player.ySize // 2
    if (player.fullMap.count("F")):
        spiralMemory.clear()
        pointGoalX = player.xSize // 2
        pointGoalY = player.ySize // 2
    if (player.fullMap[player.yCoord * player.xSize + player.xCoord] == 'F'):
        pointGoalX = player.xSize // 2 + [-1, 0, 1][random.randint(0, 2)]
        pointGoalY = player.ySize // 2 + [-1, 0, 1][random.randint(0, 2)]
        positionSource = "middle IM IN ZONE"

    path = grid.AStarPathfinding({
        'startX': player.xCoord,
        'startY': player.yCoord,
        'endX': pointGoalX,
        'endY': pointGoalY,
    })
    if (player.hasLavaNearby()):
        pathManager.setPath(path)
    pathManager.setCoords(pointGoalX, pointGoalY)
    if (pathManager.oldPosX == pointGoalX and pathManager.oldPosY == pointGoalY):
        if (len(pathManager.oldpath) > 0 and pathManager.oldPosX > 0 and pathManager.oldPosY > 0):
            pathManager.updateRemove()
            path = pathManager.oldpath
    pathManager.setPath(path)

    print(path)
    if (len(path) >= 2):
        player.goals.removeGoal()
        print(path[1]['x'] - player.xCoord, path[1]['y'] - player.yCoord)
        player.goals.addGoal(Goal("goOffset", {
                             "x": path[1]['x'] - player.xCoord, "y": path[1]['y'] - player.yCoord}))
    elif (len(path) == 1 or len(path) == 0):
        pointGoalX = player.xSize // 2
        pointGoalY = player.ySize // 2
        positionSource = "SECOND middle"
        path = grid.AStarPathfinding({
            'startX': player.xCoord,
            'startY': player.yCoord,
            'endX': pointGoalX,
            'endY': pointGoalY,
        })
        pathManager.setCoords(pointGoalX, pointGoalY)
        if (pathManager.oldPosX == pointGoalX and pathManager.oldPosY == pointGoalY):
            if (len(pathManager.oldpath) > 0 and pathManager.oldPosX > 0 and pathManager.oldPosY > 0):
                pathManager.updateRemove()
                path = pathManager.oldpath
        pathManager.setPath(path)

        if (len(path) > 1):
            player.goals.removeGoal()
            print(path[1]['x'] - player.xCoord, path[1]['y'] - player.yCoord)
            player.goals.addGoal(Goal("goOffset", {
                "x": path[1]['x'] - player.xCoord, "y": path[1]['y'] - player.yCoord}))

    print("TURA", tura)
    print("COORDS: ", player.xCoord, player.yCoord)
    # player.printFullMap()
    print("GOAL: ", pointGoalX, pointGoalY)
    print("SURSA: ", positionSource)
    player.printFullMap()
    message = player.goals.executeGoals()
    # prediction mining
    print('PATH LENGTH IN FUTURE: ', len(path))
    mineDirection = message
    if (len(path) >= 2):
        futureRobotX = path[0]['x']
        futureRobotY = path[0]['y']
        futureBlockX = path[1]['x']
        futureBlockY = path[1]['y']
        futureBlock = player.getBlock(futureBlockX, futureBlockY)

        futureGoal = Goal("goOffset", {
            "x": path[1]['x'] - path[0]['x'], "y": path[1]['y'] - path[0]['y']})
        direction = futureGoal.getDirectionLetter()
        print("direction letter: ", direction)
        if (not direction == False):
            mineDirection = direction
        if (not futureBlock == "X" or not futureBlock == "A" or not futureBlock == "C" or not futureBlock == "D"):
            options = ["l", "r", "u", "d"]
            cantMine = ["B", ".", "0", "1", "2", "3", "4"]
            if (cantMine.count(player.getBlock(futureBlockX + 1, futureBlockY))):
                options.remove("r")
            if (cantMine.count(player.getBlock(futureBlockX - 1, futureBlockY))):
                options.remove("l")
            if (cantMine.count(player.getBlock(futureBlockX, futureBlockY + 1))):
                options.remove("d")
            if (cantMine.count(player.getBlock(futureBlockX, futureBlockY - 1))):
                options.remove("u")
            if (len(options) > 0):
                mineDirection = options[random.randint(0, len(options) - 1)]
            print(len(options))
    print('MINE DIRECTION: ', mineDirection)
    action = " m " + mineDirection
    if (player.isRobot(player.xCoord - 1, player.yCoord)):
        action = " a " + "l"
    if (player.isRobot(player.xCoord + 1, player.yCoord)):
        action = " a " + "r"
    if (player.isRobot(player.xCoord, player.yCoord + 1)):
        action = " a " + "d"
    if (player.isRobot(player.xCoord, player.yCoord - 1)):
        action = " a " + "u"
    print("ACTION: ", action)

    print('PATH MANAGER ', pointGoalX, pathManager.oldPosX,
          pointGoalY, pathManager.oldPosY, pathManager.oldpath)
    send_command(message + action + buy, tura)
    read_input.close()


def send_command(actions_string, tura):
    out = open(os.path.join("game",
               "c{}_{}.txt".format(my_id, tura)), "a")
    out.write(actions_string)
    out.close()
    return


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        inp_file_name = event.src_path.split('\\')[-1]
        if inp_file_name.startswith('s') and inp_file_name.endswith('.txt') and inp_file_name[1] == str(my_id):
            funky(event.src_path, int(
                inp_file_name.split('.')[0].split('_')[-1]))


if __name__ == "__main__":

    while True:
        try:
            my_id = int(input("Enter ID:\n"))
            break
        except ValueError:
            print("Error: Invalid number")

    # wait for game to start
    while not os.path.isfile(os.path.join("game", "s{}_{}.txt".format(my_id, 0))):
        continue
    funky(os.path.join("game", "s{}_{}.txt".format(my_id, 0)), 0)

    path_to_watch = os.path.join("game")
    event_handler = MyHandler()

    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
