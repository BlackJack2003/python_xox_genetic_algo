import numpy as np
import random
import time

class player:
    def __init__(self,x=10,y=10):
        self.cx = x
        self.cy = y
        self.px =x
        self.py =y
    
class apple:
    def __init__(self):
        self.x = 15
        self.y = 15

class board:
    def __init__(self,fpos=None):
        self.h = player()
        self.board = np.zeros((20,20))
        self.segs = [self.h]
        self.board[self.h.cx][self.h.cy]=1
        self.getfrp = lambda:(random.randint(0,19),random.randint(0,19)) if fpos==None else lambda :(fpos.pop(0))
        self.fx,self.fy = self.getfrp()
        self.board[self.fx][self.fy]=2
        self.ps=np.sqrt((self.fx-self.h.cx)**2 + (self.fy-self.h.cy)**2)

    def check_death(self)->bool:
        cx = self.h.cx
        cy = self.h.cy
        for m in range(1,len(self.segs)):
            if self.segs[m].cx == cx and self.segs[m].cy == cy:
                return False
        return True
    
    def check_eat(self)->bool:
        m = bool(self.h.cx==self.fx and self.h.cy==self.fy)
        if m==True:
            self.ps=np.sqrt((self.fx-self.h.cx)**2 + (self.fy-self.h.cy)**2)
            self.fx,self.fy = self.getfrp()
            self.board[self.fx][self.fy]=2
            last = self.segs[-1]
            self.board[last.px][last.py]=1
            self.segs.append(player(last.px,last.py))
        return m
    
    #0 up,1 down 2 left 3 right
    def move(self,dd):
        if dd==0:
            dirx=1
            diry=0
        elif dd==1:
            dirx=-1
            diry=0
        elif dd==2:
            dirx=0
            diry=1
        else:
            dirx=0
            diry=-1
        self.h.px=self.h.cx
        self.h.py=self.h.cy
        self.board[self.h.cx][self.h.cx]=1
        self.h.cx+=dirx
        self.h.cy+=diry
        self.ps=np.sqrt((self.fx-self.h.cx)**2 + (self.fy-self.h.cy)**2)
        #check for border collision
        if self.h.cx>19:
            self.h.cx=0
        elif self.h.cy>19:
            self.h.cy=0
        elif self.h.cy<0:
            self.h.cy=19
        elif self.h.cx<0:
            self.h.cx=19
        #trailing segments occupy the preceeding ones place
        for m in range(1,len(self.segs)):
            self.segs[m].px=self.segs[m].cx
            self.segs[m].py=self.segs[m].cy
            self.segs[m].cx = self.segs[m-1].px
            self.segs[m].cy = self.segs[m-1].py
        #set last ones position as free
        self.board[self.segs[m].px][self.segs[m].py]=0
        return board

            
