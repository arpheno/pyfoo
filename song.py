"""pyFoo, a foobar2000 replacement for GNU/Linux systems.
    Copyright (C) <year>  <name of author>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """
class Song:
    def __init__(self,path,obj):
        # Obj should be a mutagen.mp3.MP3 object
        self.path=path
        try:
            try:
                self.artist=obj['TPE1']
            except KeyError as e:
                self.artist=""
                print e
            try:
                self.title=obj['TIT2']
            except KeyError as e:
                self.title=""
                print e
            try:
                self.genre=obj['TCON']
            except KeyError as e:
                self.genre=""
                print e
        except TypeError:
            self.genre=""
            self.artist=""
            self.title=""
            pass
