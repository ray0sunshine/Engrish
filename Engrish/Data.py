from pynput.mouse import Controller
from PyQt5.QtCore import *

import keyboard as key

class Data:
    def __init__(self):
        self.mouse = Controller()

        # constants
        self.MIN_DIST_SQ = 25        # keep the square of the minimum dist for creating a new poly point (avoid doing sqrt)

        # flags
        self.poly_clear = True       # clear the polygon data on release
        self.state_poly = False      # holding down polygon button

        # controls
        self.mpos = (0,0)            # current mouse position

        # data
        self.resetData()

        # language
        self.source_lang = 'chi_sim'
        self.target_lang = 'en'

    def resetData(self):
        self.new_poly = None         # only has data when the newest point is far enough
        self.old_poly = None         # track old poly data to only update new poly when the point is far enough
        
        # updated for the rect bounds of the widget
        self.minx = 9999
        self.miny = 9999
        self.maxx = -9999
        self.maxy = -9999
        self.w = 1
        self.h = 1

        # text
        self.prText = '?????'
        self.frText = '.....'
        self.trText = '?????'

    def sqDist(p1, p2):
        dx, dy = p1[0] - p2[0], p1[1] - p2[1]
        return dx * dx + dy * dy

    def getNewPoly(self):
        if not self.new_poly:
            return None
        if not self.old_poly or sqDist(self.new_poly, self.old_poly) >= self.MIN_DIST_SQ:
            self.old_poly = self.new_poly
            self.new_poly = None
            return self.old_poly
        return None

    def update(self):
        self.mpos = self.mouse.position
        self.state_poly = key.is_pressed('q')
        if self.state_poly:
            x, y = self.mpos
            if self.poly_clear:
                self.poly_clear = False
                self.resetData()
            self.new_poly = self.mpos
            self.minx = min(self.minx, x)
            self.miny = min(self.miny, y)
            self.maxx = max(self.maxx, x)
            self.maxy = max(self.maxy, y)
            self.w = self.maxx - self.minx
            self.h = self.maxy - self.miny
        elif not self.poly_clear:
            self.poly_clear = True

dt = Data()