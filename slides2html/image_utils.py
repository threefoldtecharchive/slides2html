import sys
import os
from concurrent.futures import ThreadPoolExecutor, wait
from PIL import Image


def to_transparent_background_image(path, newpath):
    img = Image.open(path)
    img = img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)

    img.save(newpath)


def layer_image(foregroundimg, backgroundimg):
    background = Image.open(backgroundimg)
    foreground = Image.open(foregroundimg)

    background.paste(foreground, (0, 0), foreground)
    background.save(foregroundimg)


def images_to_transparent_background(destdir):
    files = [x for x in os.listdir(destdir) if "png" in x and "_" in x and "background_" not in x]
    files.sort(key=lambda k: int(k.split("_")[0]))
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for f in files:
            fullpath = os.path.join(destdir, f)
            future = executor.submit(to_transparent_background_image, fullpath, fullpath)
            results.append(future)
    wait(results)


def set_background_for_images(destdir, bgpath):
    files = [x for x in os.listdir(destdir) if x.endswith("png") and "_" in x and "background_" not in x]
    files.sort(key=lambda k: int(k.split("_")[0]))
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for f in files:
            fullpath = os.path.join(destdir, f)
            future = executor.submit(layer_image, fullpath, bgpath)
            results.append(future)
    wait(results)
