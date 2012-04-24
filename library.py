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
import os
import cPickle as pickle
from os.path import join, getsize
from mutagen.id3 import ID3NoHeaderError,ID3
from mutagen.mp3 import MP3,HeaderNotFoundError
from song import Song
class Library:
    def __init__(self,path=None):
        #Initializing or loading of existing library missing
        if path==None:
            self.songs=[]
            self.update()
        else:
            output = open(path, 'rb')
            self.songs=pickle.load(output)
            print len(self.songs)
    def update(self):# TODO put this in a low level class
        # This method is part of the api to update song info
        temp=self._find_paths()
        self._build_library(temp)
        print "Done"
        output = open('data.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self.songs, output,protocol=2)
    def _build_library(self,paths):
        for path in paths:
            try:
                audio = MP3(path)
                self.songs.append(Song(path,audio.tags))
            except HeaderNotFoundError:
                pass
                #print "No header"
    def _find_paths(self):
        tlist=[]
        with open("library.cfg") as f:
            data = f.read()
        self.data=data.split("\n")
        for root, dirs, files in os.walk(self.data[0]):
            for f in files:
                if ".mp3" in f:
                    tlist.append(os.path.join(root,f))
        return tlist
    def __repr__(self):
        response=str(self.data)
        return response
    def search_by_title(self,title):
        return [x for x in self.songs if title in x.title]
    def search_by_artist(self,artist):
        return [x for x in self.songs if artist in x.artist]
    def search_by_genre(self,genre):
        return [x for x in self.songs if genre in x.genre]

