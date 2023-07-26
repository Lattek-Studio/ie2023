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

    path = grid.AStarPathfinding({
        'startX': player.xCoord,
        'startY': player.yCoord,
        'endX': player.xCoord - 8,
        'endY': player.yCoord - 3,
    })

    if (len(path) > 0):
        player.goals.removeGoal()
        print(path[1]['x'] - player.xCoord, path[1]['y'] - player.yCoord)
        player.goals.addGoal(Goal("goOffset", {
                             "x": path[1]['x'] - player.xCoord, "y": path[1]['y'] - player.yCoord}))
    print("TURA", tura)
    # player.printFullMap()

    message = player.goals.executeGoals()
    send_command(message, tura)
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
