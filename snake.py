import numpy as np
import random
import turtle,time

size= 40
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
        self.getfrp = lambda:self.pepe() if fpos==None else lambda :(fpos.pop(0))
        self.fx,self.fy = 0,0
        self.board[self.fx][self.fy][1]=255
        self.ps=int(np.sqrt((self.fx-self.h.cx)**2 + (self.fy-self.h.cy)**2))
        self.size=1

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
            self.board[self.fx][self.fy][1]=0
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
        self.board[self.h.cx][self.h.cx][0]=255
        self.h.cx-=dirx
        self.h.cy-=diry
        self.ps=int(np.sqrt((self.fx-self.h.cx)**2 + (self.fy-self.h.cy)**2))
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
        m=0
        for m in range(1,len(self.segs)):
            self.segs[m].px=self.segs[m].cx
            self.segs[m].py=self.segs[m].cy
            self.segs[m].cx = self.segs[m-1].px
            self.segs[m].cy = self.segs[m-1].py
        #set last ones position as free
        self.board[self.segs[m].px][self.segs[m].py][0]=0
    
    def step(self,action:int):
        self.move(action)
        rew = ((0.6*rf)-self.ps)
        eat = self.check_eat()
        if eat:
            rew+=20
        d = self.check_death()
        return self.board,rew,d,self.size
    
    def reset(self):
        self.h = player()
        self.board = np.zeros((size,size,2),dtype=np.int16)
        self.segs = [self.h]
        self.board[self.h.cx][self.h.cy][0]=255
        self.getfrp = lambda:self.pepe()
        self.fx,self.fy = 0,0
        self.board[self.fx][self.fy][1]=255
        self.ps=int(np.sqrt((self.fx-self.h.cx)**2 + (self.fy-self.h.cy)**2))
        self.size=1
        return self.board
    
    def render(self,actions,fpos):
        delay = 0.1
        wn = turtle.Screen()
        wn.title("Snake Game")
        wn.bgcolor("blue")
        # the width and height can be put as user's choice
        wn.setup(width=size*20, height=size*20)
        wn.tracer(0)
        head = turtle.Turtle()
        head.shape("square")
        head.color("white")
        head.penup()
        head.goto(0, 0)
        head.direction = "Stop"
        food = turtle.Turtle()
        colors = random.choice(['red', 'green', 'black'])
        shapes = 'square'
        food.speed(0)
        food.shape(shapes)
        food.color(colors)
        food.penup()
        food.goto(0, 100)
        
        pen = turtle.Turtle()
        pen.speed(0)
        pen.shape("square")
        pen.color("white")
        pen.penup()
        pen.hideturtle()
        pen.goto(0, 250)
        pen.write("Score : 0  High Score : 0", align="center",
                font=("candara", 24, "bold"))
        return
    
    def __str__(self)->str:
        tot = ""
        for i in range(size):
            r=""
            for j in range(size):
                m = self.board[i][j]
                r+=' '
                if m[0]==0:
                    if m[1]!=0:
                        r+='2'
                    else:
                        r+='0'
                else:
                    r+='1'
            tot+='\n'+r
        return tot

    
if __name__ =="__main__":
    board = snake_board()
    #0 up,1 down 2 left 3 right
    print(board)
    board.step(0)
    board.step(2)
    print(board)
