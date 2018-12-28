from googletrans import Translator
from desktopmagic.screengrab_win32 import getRectAsImage

from pynput.mouse import Controller
from Data import *
from Display import *
from Edit import *

import keyboard as key
import pytesseract as ts

trans = Translator()

def getScreenText(area):
    ret = ts.image_to_string(filterCapture(), lang = 'chi_sim')
    return ret.strip()

def doTranslation():
    dt.prText = getScreenText((dt.minx, dt.miny, dt.maxx, dt.maxy))
    dt.frText = dt.prText.replace('\n', '').replace(' ', '')
    translation = trans.translate(dt.frText)
    dt.trText = translation.text

key.add_hotkey('e', doTranslation, suppress=True)

initDisplay()