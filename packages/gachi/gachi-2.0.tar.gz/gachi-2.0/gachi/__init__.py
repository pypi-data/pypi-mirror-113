import os
import random
import time
import pathlib

import pyglet.media


def main():
    path = pathlib.Path(__file__).parent / "data"
    files = os.listdir(path)
    random.shuffle(files)
    for file in files:
        mp3 = pyglet.media.load(os.path.join(path, file))
        mp3.play()
        time.sleep(mp3.duration)


if __name__ == '__main__':
    main()
