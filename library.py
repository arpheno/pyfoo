"""pyFoo, a foobar2000 replacement for GNU/Linux systems.
    Copyright (C) 2012 Sebastian 'arphen' Wozny

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
import copy
import cPickle as pickle
from os.path import join, getsize
from mutagen.id3 import ID3NoHeaderError,ID3
from mutagen.mp3 import MP3,HeaderNotFoundError
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from song import Song
import random
class TreeNode:
    def __init__(self):
        self.data=None
        self.key=""
        self.children=[]
        self.parent=None
        self.row=0
        self.column=0
    def addChild(self,child):
        self.children.append(child)
    def setData(self,data):
        self.data=data
    def setKey(self,key):
        self.key=key

class LibraryModel(QAbstractItemModel):
    def __init__(self,path=None):
        QAbstractItemModel.__init__(self)
        self.root=QModelIndex()
        self.tree=TreeNode()
        if path==None:
            # No path supplied for initialization, build a new library
            print "No path provided for Library, building a new one..."
            self.songs=set()
            self.update()
        else:
            # Load existing library from provided path
            try:
                print "Trying to load library..."
                output = open(path, 'rb')
            except IOError:
                print "Sorry could not load the library"
                return
            self.songs=pickle.load(output)
            print "Library loaded\nNumber of songs in the library:",len(self.songs)
            print "Building Tree..."
            self.build(['TCON','TPE1','TIT2'])
            print "Tree built"

    def data(self,index,role):
        if role==Qt.DisplayRole:
            if index.internalPointer().data:
                return index.internalPointer().data.represent(['TPE1','TIT2'])
            else:
                return index.internalPointer().key.encode('utf-8')
        if role==32:
            if index.internalPointer().data:
                return index.internalPointer().data.represent(['TPE1','TIT2','TCON'])
            else:
                return ""
    def columnCount(self,parent):
        return 1

    def rowCount(self, parent):
        if parent == self.root:
            return len(self.tree.children)
        elif parent.isValid():
            return len(parent.internalPointer().children)
        else:
            return 0

    def index(self,row,column,parent):
        if parent==self.root:
            return self.createIndex(row, column, self.tree.children[row])
        elif parent.isValid():
            return self.createIndex(row,column,parent.internalPointer().children[row])
        else:
            return QModelIndex()

    def parent(self, index):
        if index.isValid():
            parent = index.internalPointer().parent
            if parent == self.tree:
                 return self.root
            else:
                 return self.createIndex(parent.row, 0, parent)
        return QModelIndex()

    def build(self,order):
        self.tree=TreeNode()
        for song in self.songs:
            self._insert_node(song,self.tree,order)

    def __repr__(self):
        print self.print_tree(self.tree,"" )
        return ""

    def print_tree(self,root,prefix):
        if root.data==None:
            return prefix + root.key +"\n"+ "\n".join([prefix+self.print_tree(x,prefix+"   ") for x in root.children])
        else:
            return "         "+" ".join(root.data['TPE1'])+"   "+" ".join(root.data['TIT2'])

    def _insert_node(self,item,root,origorder):
        order=copy.deepcopy(origorder)
        filt=order.pop(0)
        terminal=False
        if not order:
            terminal=True
        tags=copy.deepcopy(item[filt])
        if len(root.children):
            for child in root.children:
                if child.key in item[filt]:
                    # Remove tag from array to prevent duplicate categories.
                    tags.remove(child.key)
                    if terminal:
                        child.setData(item)
                    else:
                        self._insert_node(item,child,order)
        # Insert all the tags that have not been accounted for.
        # Note that this is the only place where new nodes are created.
        while tags:
            tag=tags.pop()
            newTreeItem=TreeNode()
            newTreeItem.setKey(tag)
            newTreeItem.parent=root
            newTreeItem.row=len(root.children)
            root.children.append(newTreeItem)
            if terminal:
                newTreeItem.setData(item)
            else:
                self._insert_node(item,newTreeItem,order)

    def update(self):# TODO put this in a low level class
        # This method is part of the api to update song info
        temp=self._find_paths()
        self._read_files(temp)
        print "Done"
        output = open('data.pkl', 'wb')
        pickle.dump(self.songs, output,protocol=2)

    def _read_files(self,paths):
        for path in paths:
            try:
                audio = MP3(path)
                self.songs.add(Song(path,audio.tags))
            except HeaderNotFoundError:
                pass

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

    def search(self,keyword):
        return [x for x in self.songs if keyword in "".join("".join(x.info))]
class Filter(QSortFilterProxyModel):
    def __init__(self,source):
        QSortFilterProxyModel.__init__(self)
        self.setSourceModel(source)
        self.exp=""
    def change_exp(self,new):
        self.exp=new
        self.invalidateFilter()
    def filterAcceptsRow(self,row,parent):
        pt=self.sourceModel().index(row,0,parent)
        key=pt.data(32).toString()
        if key=="":
            if any([self.filterAcceptsRow(i,pt) for i in range(self.sourceModel().rowCount(pt))]):
                return True
            return False
        elif self.exp in key:
            return True
        return False
