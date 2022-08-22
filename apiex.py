import os
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import shutil

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "C:/Users/Andre/Downloads"
dest_sfx = "C:/Users/Andre/SFX"
dest_music = "C:/Users/Andre/Music"
dest_video = "C:/Users/Andre/Videos"
dest_image = "C:/Users/Andre/Photos"

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

class MoverHandler(FileSystemEventHandler):
     def on_change(self, event):
          print("detected change")
          with scandir(source_dir) as entries:
               for entry in entries: 
                    name = entry.name

                    if name.lower.endswith('.wav') or name.lower.endswith('.mp3'):
                         if entry.stat().st_size < 25000000 or "SFX" in name or "sfx" in name:
                              dest = dest_sfx
                              move(dest, entry, name)
                         else:
                              dest = dest_music
                         move(dest, entry, name)
                    elif name.lower.endswith('.mov') or name.lower.endswith('.mp4'):
                         dest = dest_video
                         move(dest, entry, name)
                    elif name.lower.endswith('.jpg') or name.lower.endswith('.jpeg') or name.lower.endswith('.png'):
                        dest = dest_image
                        move(dest, entry, name)




# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()