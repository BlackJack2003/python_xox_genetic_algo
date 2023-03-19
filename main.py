#python genetic algorith for xox game
#by blackjack2003

import numpy as np
import random
import os
from numba import jit

class player:
    def __init__(self,moves:np.ndarray=None,u=0.05):
        self.moves = moves if moves is not None else np.random.randint(0,8,dtype=int,size=5)
        self.pos = 0
        self.u =u
        self.movesplayed=[]
    
    def play(self):
        k = self.moves[self.pos]
        self.pos+=1
        self.movesplayed.append([self.pos-1,k])
        return k

class board:
    def __init__(self,pls:list):
        self.board=np.zeros(9,dtype=int)
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
                if not self.board[win_cond[i][j]]==p:
                    f = False
                    break
            if f:
                return p
        return 0

    def start(self)->tuple:
        cpn = 0
        while self.nfree < 9:
            k = self.pls[cpn].play()
            if self.board[k]==0:
                self.board[k]=cpn+1
            else:
                return np.array([self.pls[int(not cpn)],self.nfree])
                
            if self.check_win(cpn+1)==cpn+1:
                return np.array([self.pls[cpn],self.nfree])
            cpn = 0 if cpn else 1
            self.nfree+=1
        return np.array([self.pls[1],self.nfree])

def make_baby(p1:player,p2:player,s1:int,s2:int)->player:
    s=[]
    for i in range(5):
        if random.randint(0,5)%2==0:
            s.append(p1.moves[i])
        else:
            s.append(p2.moves[i])
    uc=(1-((s1+s2)/18))
    return player(moves=np.array(s),u=uc)


def mutate(p1:player)->player:
    k = random.randint(0,101)
    if k <=p1.u*100:
        p1.moves[random.randint(0,4)] = random.randint(0,8)
    return p1

def get_games(n:int)->list:
    lol = []
    for i in range(n*2):
        m = player()
        lol.append(m)
    games = []
    j=0
    for i in range(n):
        games.append(board([lol[j],lol[j+1]]))
        j+=2
    return games


if __name__=="__main__":
    os.system("clc")
    games= get_games(20)

    for i in range(1000):
        wins_scores = []
        for p in games:
            w,s = p.start()[0],p.start()[1]
            wins_scores.append([w,s])
        wins_scores.sort(key=lambda x: x[1])
        print(wins_scores[0][1],"#",wins_scores[0][0].moves,'#',wins_scores[0][0].u)
        yo=[]
        games=[]
        for i in range(5):
            for j in range(4):
                yo.append(mutate(make_baby(wins_scores[i][0],wins_scores[j][0],wins_scores[i][1],wins_scores[j][1])))
        nyo = len(yo)
        for i in range(0,nyo,2):
            games.append(board([yo[i],yo[nyo-(i+1)]]))

    for i in wins_scores:
        print('#',i[1],"#",i[0].moves,'#',i[0].u)