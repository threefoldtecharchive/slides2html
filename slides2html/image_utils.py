import sys
import os
from concurrent.futures import ThreadPoolExecutor, wait
from PIL import Image


def resize_image(path, newsize):
    """resize image to a new size

    Arguments:
        path {str} -- Image path

    Keyword Arguments:
        newsize {tuple} -- new size (width,height)
    """
    img = Image.open(path)
    img.thumbnail(newsize)
    img.save(path)


def resize_images(destdir, newsize):
    """resize batch of images in destdir to a new size 
    
    Arguments:
        destdir {str} -- directory of google slides exported images
        newsize {tuple} -- tuple of width, height of the new size
    """

    files = [x for x in os.listdir(destdir) if "png" in x and "_" in x and "background_" not in x]
    files.sort(key=lambda k: int(k.split("_")[0]))
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for f in files:
            fullpath = os.path.join(destdir, f)
            future = executor.submit(resize_image, fullpath, newsize)
            results.append(future)
    wait(results)


def to_transparent_background_image(path, newpath):
    """convert image to image with transparent background
    
    Arguments:
        path {str} -- old image
        newpath {str} -- new image
    """

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
    """layer foregroundimg on top of backgroundimg
    
    Arguments:
        foregroundimg {str} -- path of foreground image
        backgroundimg {str} -- path of background image
    """

    background = Image.open(backgroundimg)
    foreground = Image.open(foregroundimg)

    background.paste(foreground, (0, 0), foreground)
    background.save(foregroundimg)


def images_to_transparent_background(destdir):
    """convert batch of images to transparent background images
    
    Arguments:
        destdir {str} -- path of a directory with google slides exported images
    """

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
    """Apply background to all images in destdir
    
    Arguments:
        destdir {str} -- directory with exported google slides as images
        bgpath {str} -- background path
    """

    files = [x for x in os.listdir(destdir) if x.endswith("png") and "_" in x and "background_" not in x]
    files.sort(key=lambda k: int(k.split("_")[0]))
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for f in files:
            fullpath = os.path.join(destdir, f)
            future = executor.submit(layer_image, fullpath, bgpath)
            results.append(future)
    wait(results)
