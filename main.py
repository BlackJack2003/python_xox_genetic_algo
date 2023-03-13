import numpy as np
import numba
import random

#Create mutate

class player:
    def __init__(self,moves:np.ndarray=None,u=0.05):
        self.moves = moves if moves is not None else np.random.randint(0,9,dtype=int,size=5)
        self.pos = 0
        self.u =u
    
    def play(self):
        self.pos+=1
        return self.moves[self.pos-1]

class board:
    def __init__(self,pls:list):
        self.board = np.zeros((9,),dtype=int)
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
    
    def start(self)->tuple:
        cpn = 0
        while self.nfree < 9:
            k = self.pls[cpn].play()
            if self.board[k]!=-1:
                return (self.pls[int(not cpn)],self.nfree)
            else:
                self.board[k]=cpn+1
            if self.check_win(cpn+1):
                return self.pls[cpn]
            cpn = int(not cpn)
            self.nfree+=1
        return (self.pls[1],self.nfree)

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
    k = random.randint(101)
    if k <=p1.u*100:
        p1.moves[random.randint(0,5)] = random.randint(0,9)

def get_games(n:int)->list:
    lol = []
    for i in range(n*2):
        m = player()
        print(m.moves)
        lol.append(m)
    games = []
    j=0
    for i in range(n):
        games.append(board([lol[j],lol[j+1]]))
        j+=2
    return games

games= get_games(16)

for i in range(100):
    wins_scores = []
    for p in games:
        (w,s) = p.start()
        wins_scores.append([w,s])
    wins_scores.sort(key=lambda x: x[1])
    yo=[]
    games=[]
    for i in range(5):
        for j in range(4):
            yo.append(make_baby(wins_scores[i][0],wins_scores[j][0],wins_scores[i][1],wins_scores[j][1]))
    nyo = len(yo)
    for i in range(nyo):
        games.append(board([yo[i],yo[nyo-i-1]]))

for i in wins_scores:
    print(i[1],"#",i[0].moves)