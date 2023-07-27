from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

from reader.player import Perseus
from reader.goals import Goal
from pathfinding.main import Grid
from pathfinding.spiral import get_spiral_traj


player = Perseus()
player.goals.addGoal(Goal("goOffset", {"x": -1, "y": 0}))
grid = Grid("")
# function triggered by file creation


def funky(read_file_path, tura):
    read_input = open(read_file_path, "r")
    player.setTura(tura)
    input = read_input.read()
    player.addReading(input)
    positionSource = "NONE"
    # update zone

    if (player.map.count("F")):
        indexes_dict = {'F': []}

        for i, char in enumerate(player.map):
            if char in indexes_dict:
                indexes_dict[char].append(i)
        for index in indexes_dict['F']:
            xZone = index % player.xSize
            yZone = index // player.xSize
            player.setZone(xZone, yZone)

    grid.setMap(player.fullMap, player.xSize, player.ySize)
    pointGoalX = player.xSize // 2
    pointGoalY = player.ySize // 2
    positionSource = "first middle"
    # spiral magic
    spiral = get_spiral_traj(
        6, 6, player.homeX, player.homeY, player.xSize, player.ySize)
    # print(spiral)
    if (player.fullMap[player.homeY * player.xSize + player.homeX] == 'F'):
        spiral = []
    filtered = []
    # remove spiral point that are ? in player.fullMap
    if (not player.fullMap == ""):

        for point in spiral:
            if point[0] < 0 or point[0] >= player.xSize or point[1] < 0 or point[1] >= player.ySize:
                spiral.remove(point)
            elif not player.fullMap[point[1] * player.xSize + point[0]] == '?':
                spiral.remove(point)
            elif player.fullMap[point[1] * player.xSize + point[0]] == 'B':
                spiral.remove(point)
            elif player.fullMap[point[1] * player.xSize + point[0]] == 'F':
                spiral.remove(point)
            else:
                filtered.append(point)
        if (len(filtered) > 0):
            pointGoalX = filtered[0][0]
            pointGoalY = filtered[0][1]
            positionSource = "SPIRAL"
            print(
                "BLOCK: ", player.fullMap[filtered[0][1] * player.xSize + filtered[0][0]])
            print(
                "BLOCK PLAYER: ", player.fullMap[player.yCoord * player.xSize + player.xCoord])
            print("SPIRAL: ", filtered[0][0], filtered[0][1])
    print(filtered)

    if (player.fullMap.count("C") or player.fullMap.count("D")):
        # find ore coords
        map = player.fullMap
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
    if (player.health < 5 and player.osmium):
        buy = " b h"
    if (player.health < 10 and player.battery and player.osmium):
        buy = " b h"

    # atack

    # pointGoalX = player.xSize // 2
    # pointGoalY = player.ySize // 2
    # if (player.fullMap.count("F")):
    #     pointGoalX = player.xSize // 2
    #     pointGoalY = player.ySize // 2
    if (player.fullMap[player.yCoord * player.xSize + player.xCoord] == 'F'):
        pointGoalX = player.xSize // 2
        pointGoalY = player.ySize // 2
        positionSource = "middle IM IN ZONE"
    path = grid.AStarPathfinding({
        'startX': player.xCoord,
        'startY': player.yCoord,
        'endX': pointGoalX,
        'endY': pointGoalY,
    })

    if (len(path) > 1):
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
    send_command(message + " m " + message + buy, tura)
    read_input.close()


def send_command(actions_string, tura):
    out = open(os.path.join("simulator", "game",
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
    while not os.path.isfile(os.path.join("simulator", "game", "s{}_{}.txt".format(my_id, 0))):
        continue
    funky(os.path.join("simulator", "game", "s{}_{}.txt".format(my_id, 0)), 0)

    path_to_watch = os.path.join("simulator", "game")
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
