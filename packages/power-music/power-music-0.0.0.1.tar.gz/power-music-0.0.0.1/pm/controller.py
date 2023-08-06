# from .charts.bugs import Bugs
# from .charts.genie import Genie
from .charts.melon import Melon

import json

class Controller(object):
    """
    time : d (day), m (month), w (week)
    genre : ballad, ost, etc ...
    """
    def __init__(self, time=None, song_code=None, site=None):
        
        self.time = time
        self.song_code = song_code
        self.site = site
        self.__refactoring()

    def __refactoring(self):
        if self.site == 'bugs':
            if self.time == 'd': self.time = 'day'
            elif self.time == 'w': self.time = 'week'
            elif self.time == 'm': self.time = 'month'
        if self.site == 'genie': return 0
        if self.site == 'melon': return 0

    def get_songs(self):
        if self.site == 'bugs':
            return 'Currently {} site is not supported'.format(self.site)
        elif self.site == 'genie':
            return 'Currently {} site is not supported'.format(self.site)
        elif self.site == 'melon':
            melon = Melon(time=self.time, song_code=self.song_code)
            return melon.get_songs()
        else:
            return 'Currently {} site is not supported'.format(self.site)

    def get_ytdata(self):
        if self.site == 'bugs':
            return 'Currently {} site is not supported'.format(self.site)
        elif self.site == 'genie':
            return 'Currently {} site is not supported'.format(self.site)
        elif self.site == 'melon':
            melon = Melon(time=self.time, song_code=self.song_code)
            return melon.get_yt_data()
        else:
            return 'Currently {} site is not supported'.format(self.site)