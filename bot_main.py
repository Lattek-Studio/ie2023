from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

#function triggered by file creation
def funky():
    print("funky_sussy")

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if  event.src_path.split('/')[-1][0] == 's' and event.src_path.endswith('.txt'):
            funky()

if __name__ == "__main__":
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