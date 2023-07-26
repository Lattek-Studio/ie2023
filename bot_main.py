from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

from reader.player import Perseus
from reader.goals import Goal
from pathfinding.main import Grid


player = Perseus()
player.goals.addGoal(Goal("goOffset", {"x": -1, "y": 0}))
grid = Grid("")
# function triggered by file creation


def funky(read_file_path, tura):
    read_input = open(read_file_path, "r")
    player.setTura(tura)
    input = read_input.read()
    player.addReading(input)
    grid.setMap(player.fullMap, player.xSize, player.ySize)

    pointGoalX = player.xCoord - 2
    pointGoalY = player.yCoord - 1

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

        print(indexes_dict)
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
    # player.printFullMap()

    message = player.goals.executeGoals()
    send_command(message + " m " + message, tura)
    read_input.close()


def send_command(actions_string,tura):
    out = open(os.path.join("simulator","game","c{}_{}.txt".format(my_id,tura)), "a")
    out.write(actions_string)
    out.close()
    return

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        inp_file_name = event.src_path.split('\\')[-1]
        if inp_file_name.startswith('s') and inp_file_name.endswith('.txt') and inp_file_name[1] == str(my_id):
            funky(event.src_path, int(
                inp_file_name.split('.')[0].split('_')[-1]))


def get_spiral_traj(width,spirals,x,y):
    correction_x = x
    correction_y = y
    x = 0
    y= 0
    prx=0
    pry=0

    coord_list = []

    for i in range (spirals):
        x=0-width-abs(prx)
        coord_list.append((x+correction_x,y+correction_y))
        y=0+width+abs(pry)
        coord_list.append((x+correction_x,y+correction_y))
        x=abs(x)
        coord_list.append((x+correction_x,y+correction_y))
        y=0-y
        coord_list.append((x+correction_x,y+correction_y))
        prx=x
        pry=y

    return coord_list
  
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
