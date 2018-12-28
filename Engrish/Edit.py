from googletrans import Translator
from desktopmagic.screengrab_win32 import getRectAsImage

from pynput.mouse import Controller
from collections import deque
from Data import *
from Display import *

import keyboard as key
import pytesseract as ts

from PIL import Image

def filterCapture():
    # make this more stable lol
    # maybe dynamic buffer bounds
    boundBuffer = 40
    saveImages = False

    # make matrix matching large image size
    im = getRectAsImage((dt.minx - boundBuffer, dt.miny - boundBuffer, dt.maxx + boundBuffer, dt.maxy + boundBuffer))
    omap = im.load()
    lw, lh = im.size[0], im.size[1]
    flag = [[False] * lh for _ in range(lw)]
    if saveImages:
        im.save('test0.png')

    im1 = Image.new(im.mode, im.size)
    nmap = im1.load()

    # loop over small image pixels using queue and select method, set flag on all pixels touched (set white to white still)
    q = deque()
    for x in range(boundBuffer, lw - boundBuffer):
        for y in range(boundBuffer, lh - boundBuffer):
            if not flag[x][y]:
                flag[x][y] = True
                q.append((x,y))
            while q:
                x, y = q.popleft()
                if sum(omap[x,y]) < 600:
                    nmap[x,y] = omap[x,y]
                    for c in [(x+1,y+1),(x,y+1),(x-1,y+1),(x+1,y),(x-1,y),(x+1,y-1),(x,y-1),(x-1,y-1)]:
                        x, y = c
                        if 0 <= x < lw and 0 <= y < lh:
                            if not flag[x][y]:
                                flag[x][y] = True
                                q.append(c)
                else:
                    nmap[x,y] = (255,255,255,255)
    if saveImages:
        im1.save('test1.png')

    # marke all large image pixels that are not flagged as white
    for x in range(lw):
        for y in range(lh):
            if not flag[x][y]:
                nmap[x,y] = (255,255,255,255)

    # maybe find a max range and extend randomly and combine ocr results?
    if saveImages:
        im1.save('test2.png')
    return im1