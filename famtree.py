import sqlite3
from sqlite3 import Error

dbname = 'gedcom.db'

class Famnode:
    def Famnode(h='', w='', c=[]):
        self.husband = h
        self.wife = w
        self.children = c

class Famtree:
    def Famtree(h='', w='', c=[]):
        self.root = Famnode(h,w,c)
    def create_Famtree

