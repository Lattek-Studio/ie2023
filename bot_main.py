from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

#function triggered by file creation
def funky(read_file_path,tura):
    read_input = open(read_file_path, "r")
    print(read_input.read())

    print("TURA", tura)

    send_command("U M U",tura)
    read_input.close()

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        inp_file_name = event.src_path.split('\\')[-1]
        if  inp_file_name.startswith('s') and inp_file_name.endswith('.txt') and inp_file_name[1] == str(my_id):
            funky(event.src_path,int(inp_file_name.split('.')[0].split('_')[-1]))





def send_command(actions_string,tura):
    out = open(os.path.join("simulator","game","c{}_{}.txt".format(my_id,tura)), "a")
    out.write(actions_string)
    out.close()
    return




#Helper for drawing spiral paths
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


    #wait for game to start
    while not os.path.isfile(os.path.join("simulator","game","s{}_{}.txt".format(my_id,0))):
        continue
    funky(os.path.join("simulator","game","s{}_{}.txt".format(my_id,0)),0)

    path_to_watch = os.path.join("simulator","game") 
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