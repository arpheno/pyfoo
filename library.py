import os
import cPickle as pickle
from os.path import join, getsize
from mutagen.id3 import ID3NoHeaderError,ID3
class Library:
    def __init__(self,path=None):
        #Initializing or loading of existing library missing
        if path==None:
            self.songs=[]
        else:
            pass
    def update(self):# TODO put this in a low level class
        # This method is part of the api to update song info
        temp=self._find_paths()
        self._build_library(temp)
        output = open('data.pkl', 'wb')
        # Pickle dictionary using protocol 0.
        pickle.dump(self.songs, output)
    def _build_library(self,paths):
        for path in paths:
            try:
                audio = ID3(path)
                self.songs.append(audio)
            except ID3NoHeaderError as e:
                print e
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
a=Library()
a.update()
