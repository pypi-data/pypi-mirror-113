from pm.charts.melon import Melon
import datetime

now = datetime.datetime.now()
day_time = str(now.year) + "{:02d}".format(now.month) + "{:02d}".format(now.day) + "{:02d}".format(now.hour) + '00'
melon = Melon(time=day_time, song_code='GN0100')

assert melon.time == day_time
assert melon.song_code == 'GN0100'
assert melon.songs_count == len(melon.songs)
assert type(melon.songs) == list