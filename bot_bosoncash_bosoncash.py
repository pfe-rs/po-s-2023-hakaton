from random import randrange
import time
import numpy as np
a=100 # Prioritet stampaca
b=1 # Prioritet kapaciteta
c=1 # Prioritet vojnika_pravi
d=1 # Prioritet neprijatelja
e=1 # Prioritet losih suseda
f=0.1 # Prioritet vaznosti
g=8 # vrednost u pozeljnosti
pd=1 # opasnost u pozeljnosti
po=1 # nopasnost u pozeljnosti
pp=1 # neutralnih vojnika u pozeljnosti
tp=1 # turn
sp=1 # stampanje

N=10
nasevojske=0
ukvojske=0
vojske=np.zeros((N,N))
tim=np.zeros((N,N))
ukapacitet=0
kapacitet=np.zeros((N,N))
upravi=0
pravi=np.zeros((N,N))
ustampa=0
stampa=np.zeros((N,N))
snaga=np.zeros((N,N))
n_snaga=np.zeros((N,N))
val=np.zeros((N,N))
opasnost=np.zeros((N,N))
nopasnost=np.zeros((N,N))
pozeljenost=np.zeros((N,N))

heatmap=[[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1]] #Popuni vrednostima
normalna=[[1,0.67032,0.201897,0.0273237,0.00166156,0.00099,0.0008,0.0007],
    [0.67032,0.201897,0.0273237,0.00166156,0.00099,0.0008,0.0007,0.0006],
    [0.201897,0.0273237,0.00166156,0.00099,0.0008,0.0007,0.0006,0.0005],
    [0.0273237,0.00166156,0.00099,0.0008,0.0007,0.0006,0.0005,0.0004],
    [0.00166156,0.00099,0.0008,0.0007,0.0006,0.0005,0.0004,0.0003],
    [0.00099,0.0008,0.0007,0.0006,0.0005,0.0004,0.0003,0.0002],
    [0.0008,0.0007,0.0006,0.0005,0.0004,0.0003,0.0002,0.0001],
    [0.0007,0.0006,0.0005,0.0004,0.0003,0.0002,0.0001,0.00005]]
def zbir_suseda(x:int,y:int):
    rez=0
    if(x!=1):
        rez+=(tim[x-1][y]!=1)
    if(x!=N):
        rez+=(tim[x+1][y]!=1)
    if(y!=1):
        rez+=(tim[x][y-1]!=1)
    if(y!=N):
        rez+=(tim[x][y+1]!=1)
    return rez
def nasa_vojska():
    global snaga
    for x in range(1,N+1):
        for y in range(1,N+1):
            for i in range(1,N+1):
                for j in range(1,N+1):
                    if(tim[i][j]==1):
                        snaga[x][y]+=normalna[abs(x-i)][abs(y-j)]*vojske[i][j]/ukvojske
def neprijateljska_vojska():
    global n_snaga
    for x in range(1,N+1):
        for y in range(1,N+1):
            for i in range(1,N+1):
                for j in range(1,N+1):
                    if(tim[i][j]==-1):
                        n_snaga[x][y]+=normalna[abs(x-i)][abs(y-j)]*vojske[i][j]/ukvojske
def napravi_value():
    global val
    for i in range (1,N+1):
        for j in range (1,N+1):
         #   print(i,j)
            val[i][j] = (stampa[i][j]*a/ustampa + kapacitet[i][j]*b/ukapacitet + pravi[i][j]*c/upravi)*heatmap[i][j]
def prop_value():
    #print("B")
    global val
    #print("B")
    pommat = np.zeros((N+2,N+2))
    #print("B")
   # print(pommat)
   # print(N)
    #print("ABC")
    for x in range(1,N+1):
        for y in range(1,N+1):
            for i in range(1,N+1):
                for j in range(1,N+1):
                    #print(x,y,i,j)
                    #print(val[i][j])
                    #print(normalna[abs(x-i)][abs(y-j)])
                    #print(pommat[x][y])
                    pommat[x][y]+=val[i][j]*normalna[abs(x-i)][abs(y-j)]
    for i in range(1,N+1):
        for j in range(1,N+1):
           # print(i,j)
            val[i][j]=pommat[i][j]
def get_opasnost():
    global opasnost
    for i in range (1,N+1):
        for j in range (1,N+1):
            opasnost[i][j]=((n_snaga[i][j]-snaga[i][j])*d+(-zbir_suseda(i,j))*e)*val[i][j]*f
def nep_get_opasnost():
    global nopasnost
    for i in range (1,N+1):
        for j in range (1,N+1):
            nopasnost[i][j]=(snaga[i][j]-n_snaga[i][j]-pp*neutralnih(i,j)/ukvojske)*d+(zbir_suseda(i,j))*e+val[i][j]*f
def prop_opasnost():
    global opasnost
    pommat = np.zeros((N+2,N+2))
    for x in range(1,N+1):
        for y in range(1,N+1):
            for i in range(1,N+1):
                for j in range(1,N+1):
                    pommat[x][y]+=opasnost[i][j]*normalna[abs(x-i)][abs(y-j)]
    for i in range(1,N+1):
        for j in range(1,N+1):
            opasnost[i][j]=pommat[i][j]
def prop_nopasnost():
    global nopasnost
    pommat = np.zeros((N+2,N+2))
    for x in range(1,N+1):
        for y in range(1,N+1):
            for i in range(1,N+1):
                for j in range(1,N+1):
                    pommat[x][y]+=nopasnost[i][j]*normalna[abs(x-i)][abs(y-j)]
    for i in range(1,N+1):
        for j in range(1,N+1):
            nopasnost[i][j]=pommat[i][j]
def neutralnih(x:int,y:int):
    if(tim[x][y]==0):
        return vojske[x][y]
    else:
        return 0   
def get_pozeljenost():
    global pozeljenost
    for i in range (1,N+1):
        for j in range (1,N+1):
            pozeljenost[i][j]=val[i][j]*g+opasnost[i][j]*pd+nopasnost[i][j]*po-neutralnih(i,j)*pp/nasevojske
def podela(matrix,timm):
    global ukvojske
    global upravi
    global ustampa
    global ukapacitet
    global pravi
    global kapacitet
    global stampa
    global tim
    global vojske
    global nasevojske
    for i in range (1,N+1):
        for j in range (1,N+1):
            #print(i,j)
            pravi[i][j]=matrix[i-1][j-1][0]
            upravi+=pravi[i][j]
            kapacitet[i][j]=matrix[i-1][j-1][1]
            ukapacitet+=kapacitet[i][j]
            stampa[i][j]=matrix[i-1][j-1][2]
            ustampa+=stampa[i][j]
            tim[i][j]=matrix[i-1][j-1][3]*timm
            vojske[i][j]=matrix[i-1][j-1][4]
            ukvojske+=vojske[i][j]
            if(tim[i][j]==1):
                nasevojske+=vojske[i][j]
def mozevojske(x:int,y:int):
    if(x<1 or x>N):
        return False
    if(y<1 or y>N):
        return False
    if(vojske[x][y]==kapacitet[x][y] and tim[x][y]==1):
        return False
    return True
def dummydo(row:int,column:int):
    roll = True
    while roll:
        out = randrange(4)
        roll = False
        if out == 1 and row == 1:
            roll = True
        if out == 2 and column == N:
            roll = True
        if out == 3 and row == N:
            roll = True
        if out == 4 and column == 1:
            roll = True
    return out
def act(row: int, column: int, team: int, turn: int, mycash: int, opcash: int, map:list[list[tuple[int, int, int, int, int]]])->int:
    #print(team)
    global N
    N=len(map[0])
    podela(map,team)
    row+=1
    column+=1
    #print("A")
    napravi_value()
    #print(val)
   # return 0
   # print("A")
    prop_value()
   # print("A")
    nasa_vojska()
   # print("A")
    neprijateljska_vojska()
   # print("A")
    get_opasnost()
  #  print("A")
    nep_get_opasnost()
   # print("A")
    prop_opasnost()
  #  print("A")
    prop_nopasnost()
   # print("A")
    get_pozeljenost()
   # print("DOSTA VISE SA AOVIMA")
    #Odluka
    #print(vojske)
  #  print(tim)
  #  print(val)
  #  print(opasnost)
  #  print(nopasnost)
  #  print(pozeljenost)

    susedi=[0,0,0,0,0]
    susedi[0]=pozeljenost[row][column]
    if(vojske[row][column]==kapacitet[row][column] or pravi[row][column]==-1):
        susedi[0]=-1000000
    if(mozevojske(row-1,column) and vojske[row][column]!=0):
        susedi[1]=pozeljenost[row-1][column]
    else:
        susedi[1]=-1000000
    if(mozevojske(row+1,column) and vojske[row][column]!=0):
        susedi[3]=pozeljenost[row+1][column]
    else:
        susedi[3]=-1000000
    if(mozevojske(row,column-1) and vojske[row][column]!=0):
        susedi[4]=pozeljenost[row][column-1]
    else:
        susedi[4]=-1000000
    if(mozevojske(row,column+1) and vojske[row][column]!=0):
        susedi[2]=pozeljenost[row][column+1]
    else:
        susedi[2]=-1000000
    best=0
    for i in range(1,5):
        if(susedi[i]>susedi[best]):
            best=i
  #  print(row,column)
  #  print(susedi)
    #print(best)
   # print(susedi)
    if((stampa[row][column]*sp>=susedi[best] and stampa[row][column]!=0) or (best==0 and (pravi[row][column]==0 or kapacitet[row][column]==vojske[row][column]))):
        if(stampa[row][column]==0):
            if(susedi[best]!=-1000000):
                return best
            else:
                dummydo(row,column) # Ako nema sta pametno da radi, nek radi nesto random, mozda uspe
        else:
            return 5
    return best

#act(1,1,1,1,0,0,[[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],
 #                [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],
 #                [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],
 #                [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],
 #                [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],
 #                [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],
 #               [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]],
  #              [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]])