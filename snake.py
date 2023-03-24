import numpy as np
import random
import turtle,time

size= 40

hlook = np.array([255,255])
flook = np.array([0,255])
blook=np.array([255,0])
blank=np.array([0,0])

if __name__ =="__main__":
    size=10
    fposy = [(5,5),(0,0),(6,6),(5,6),(6,7),(0,0)]

rf = 2*size -1

class InvalidInputError(Exception):
    print("Invalid Input val")
class player:
    def __init__(self,x=size//2 +1,y=size//2 + 1):
        self.cx = x
        self.cy = y
        self.px =x
        self.py =y

class snake_board:
    def elpepe(self)->tuple:
        m = self.fpos[0]
        self.fpos.pop(0)
        return m

    def pepe(self):
        m,k = random.randint(0,size-1),random.randint(0,size-1)
        while self.board[m][k][0]!=0:
            m,k = random.randint(0,size-1),random.randint(0,size-1)
        return m,k

    def __init__(self,fpos=None):
        self.h = player()
        self.board = np.zeros((size,size,2),dtype=np.int16)
        self.segs = [self.h]
        self.board[self.h.cx][self.h.cy][0]=255
        self.board[self.h.cx][self.h.cy][1]=255
        if fpos==None:
            self.getfrp = lambda:self.pepe() 
        else:
            self.fpos = fpos
            self.getfrp = lambda: self.elpepe()
        self.fx,self.fy = self.getfrp()
        self.board[self.fx][self.fy][1]=255
        self.ps=abs(self.fx-self.h.cx) + abs(self.fy-self.h.cy)
        self.size=1
        self.pd = -1
        self.timestep=0

    def check_death(self)->bool:
        cx = self.h.cx
        cy = self.h.cy
        for m in range(1,len(self.segs)):
            if self.segs[m].cx == cx and self.segs[m].cy == cy:
                return True
        return False
    
    def check_eat(self)->bool:
        m = bool(self.h.cx==self.fx and self.h.cy==self.fy)
        if m==True:
            self.fx,self.fy = self.getfrp()
            self.board[self.fx][self.fy][1]=255
            last = self.segs[-1]
            self.board[last.px][last.py][0]=255
            self.segs.append(player(last.px,last.py))
            self.size+=1
        return m
    
    #0 up,1 down 2 left 3 right
    def move(self,dd:int):
        if dd==0:
            dirx=1
            diry=0
        elif dd==1:
            dirx=-1
            diry=0
        elif dd==2:
            dirx=0
            diry=1
        elif dd==3:
            dirx=0
            diry=-1
        else:
            raise InvalidInputError
        self.h.px=self.h.cx
        self.h.py=self.h.cy
        self.h.cx-=dirx
        self.h.cy-=diry
        self.ps=abs(self.fx-self.h.cx) + abs(self.fy-self.h.cy)
        #check for border collision
        if self.h.cx>size-1:
            self.h.cx=0
        elif self.h.cy>size-1:
            self.h.cy=0
        elif self.h.cy<0:
            self.h.cy=size-1
        elif self.h.cx<0:
            self.h.cx=size-1
        #trailing segments occupy the preceeding ones place
        self.board[self.h.cx][self.h.cy][0]=255
        self.board[self.h.cx][self.h.cy][1]=255
        self.board[self.h.px][self.h.py][1]=0
        m=0
        for m in range(1,len(self.segs)):
            self.segs[m].px=self.segs[m].cx
            self.segs[m].py=self.segs[m].cy
            self.segs[m].cx = self.segs[m-1].px
            self.segs[m].cy = self.segs[m-1].py
        #set last ones position as free
        self.board[self.segs[-1].px][self.segs[-1].py][0]=0
    
    def step(self,action:int):
        self.move(action)
        eat = self.check_eat()
        self.timestep+=1
        d = self.check_death() 
        if eat==True:
            rew=200
            self.timestep=0
        elif d:
            rew=-100
        else:
            rew=(rf-self.ps)-(self.timestep/16)+(60/(10+np.exp(self.size-1)))
        return self.board,int(rew),d,self.size
    
    def reset(self,fpos:list=None):
        self.h = player()
        self.board = np.zeros((size,size,2),dtype=np.int16)
        self.segs = [self.h]
        self.board[self.h.cx][self.h.cy][0]=255
        self.board[self.h.cx][self.h.cy][1]=255
        if fpos==None:
            self.getfrp = lambda:self.pepe()
        else:
            self.fpos=fpos
            self.getfrp=lambda:self.elpepe()
        self.fx,self.fy = self.getfrp()
        self.board[self.fx][self.fy][1]=255
        self.ps=abs(self.fx-self.h.cx) + abs(self.fy-self.h.cy)
        self.size=1
        self.timestep=0
        return self.board
    
    def render(self,actions,fpos):
        k = size*10
        wn = turtle.Screen()
        wn.tracer(0)
        self.reset(fpos)
        wn.title("Snake Game")
        wn.bgcolor("white")
        # the width and height can be put as user's choice
        wn.setup(width=max(500,size*21), height=max(500,size*21))
        head=turtle.Turtle()
        head.penup()
        head.setpos((self.h.cy*20)-k,(-20*self.h.cx)+k)
        head.shape('square')
        head.color('black')
        segs=[head]
        food = turtle.Turtle()
        food.shape('square')
        food.color('blue')
        food.penup()
        food.setpos((self.fy*20)-k,(self.fx*-20)+k)
        def add_seg(x,y):
            seg1 = turtle.Turtle()
            seg1.shape('square')
            seg1.color('black')
            seg1.penup()
            seg1.goto(x,y)
            return seg1
        while True:
            for _ in range(len(actions)):
                self.step(actions[_])
                food.setpos((self.fy*20)-k,(self.fx*-20)+k)
                if len(self.segs)>len(segs):
                    segs.append(add_seg((self.segs[-1].cy*20)-k,(self.segs[-1].cx*-20)+k))
                for i,v in enumerate(self.segs):
                    segs[i].setpos((v.cy*20)-k,(v.cx*-20)+k)
                print((self.segs[-1].cx*20)-k,(self.segs[-1].cy*20)+k)
                time.sleep(0.5)
                wn.update()
            break
    
    def __str__(self)->str:

        tot = "\n    "
        for i in range(size):
            tot+=' '+str(i)
        tot+='\n     '
        for i in range(size):
            tot+=' #'
        tot+="\n"
        for i in range(size):
            r=str(i)+"# "
            for j in range(size):
                m = self.board[i][j]
                r+=' '
                if m[0]==0:
                    if m[1]==255:
                        r+='2'
                    else:
                        r+='0'
                else:
                    if m[1]==0:
                        r+='1'
                    else:
                        r+='H'
            tot+='\n'+r
        return tot+'\nSize: '+str(self.size)+'#'+str(self.h.cx)+'#'+str(self.h.cy)
    
if __name__ =="__main__":
    size=30
    board = snake_board()
    print(board)
    #0 up,1 down 2 left 3 right
    k =(0,2,0,2,0,2,0,2,0,2,0,2,2,0)
    board.render(k,fposy.copy())

    
