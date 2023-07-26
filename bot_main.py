from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

#function triggered by file creation
def funky(read_file_path,tura):
    print(tura, "\n\n\n")
    read_input = open(read_file_path, "r")
    print(read_input.read())

def send_command(move,action,action_m,upgrade,tura):
    return

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        inp_file_name = event.src_path.split('\\')[-1]
        if  inp_file_name.startswith('s') and inp_file_name.endswith('.txt') and inp_file_name[1] == str(my_id):
            funky(event.src_path,int(inp_file_name.split('.')[0].split('_')[-1]))

if __name__ == "__main__":

    while True:
        try:
            my_id = int(input("Enter ID:\n"))
            break
        except ValueError:
            print("Error: Invalid number")


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