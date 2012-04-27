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
class Song:

    def __init__(self,path,obj):
        # Obj should be a mutagen.mp3.MP3 object
        self.path=path
        self.info={}
        self.info['TPE1']=set()
        self.info['TIT2']=set()
        self.info['TCON']=set()
        try:
            try:
                self.info['TPE1']=set(obj['TPE1'].text)
            except KeyError as e:
                print "Missing key:",e
            try:
                self.info['TIT2']=set(obj['TIT2'].text)
            except KeyError as e:
                print "Missing key:",e
            try:
                self.info['TCON']=set(obj['TCON'].text)
            except KeyError as e:
                print "Missing key:",e
        except TypeError as e:
            print "Type error:",e

    def __getitem__(self,key):
        if not self.info.has_key(key):
            raise KeyError
        else:
            return self.info[key]
    def __repr__(self,order):
        return " ".join(self.info['TPE1']).encode("utf-8")+" - "+" ".join(self.info['TPE2']).encode('utf-8')
    def represent(self,order):
        response=""
        while order:
            o=order.pop(0)
            response+=" ".join(self.info[o]).encode('utf-8')
            response+=" "
        return response
