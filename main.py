import numpy as np
import numba
import random

#Create mutate

class player:
    def __init__(self,moves=None):
        self.moves = moves if moves is not None else np.random.randint(0,9,dtype=np.int8)
        self.pos = 0
        self.score=0
    
    def play(self):
        self.pos+=1
        return self.moves[self.pos-1]

class board:
    def __init__(self,pls:list):
        self.board = np.zeros((9,0),dtype=np.int8)
        self.pls=pls
        self.nfree=0

    def check_win(self,p):
        win_cond = [[0, 1, 2],
					[3, 4, 5],
					[6, 7, 8],
					[0, 3, 6],
					[1, 4, 7],
					[2, 5, 8],
					[0, 4, 8],
					[2, 4, 6]]
        for i in range(len(win_cond)):
            f=True
            for j in range(3):
                if not win_cond[i][j]==p:
                    f = False
                    break
            if f:
                return p
        return 0
    
    def start(self):
        cpn = 0
        while self.nfree < 9:
            k = self.pls[cpn].play()
            if self.board[k]!=0:
                return self.pls[int(not cpn)]
            else:
                self.borad[k]=cpn
            if self.check_win(cpn):
                return self.pls[cpn]
            cpn = int(not cpn)
            self.nfree+=1
        return self.pls[1],self.nfree


lol = []

def mutate(p1:player,p2:player)->player:
    return p1

def get_games(n:int):
    for i in range(n*2):
        lol.append(player())

    games = []
    j=0
    for i in range(n):
        games.append(board([lol[j],lol[j+1]]))
        j+=2

games= get_games(12)

for i in range(10):
    wins_scores = [],[]
    for p in games:
        w,s = p.start()
        wins_scores.append([w,s])
    wins_scores.sort(key=lambda x: x[1])