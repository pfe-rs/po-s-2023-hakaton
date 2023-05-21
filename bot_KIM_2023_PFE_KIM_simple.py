#!/bin/python
import sys
import math
"""
0 - proizvodnja virusa
1 - pomeranje na gore
2 - pomeranje na desno
3 - pomeranje na dole
4 - pomeranje na levo
5 - stampanje novca
"""
daju = []
potez = -1
def nadji(cvor:tuple[int, int, int, int, int]):
	global daju
	for element in daju:
		if element == cvor:
			return True
	return False

"""
0 - cpu
1 - ram
2 - stampa
3 - tim
4 - virusi
"""
# Vaznost ~ tezinu zauzimanja jednog cvora
def computeWeight(cvor:tuple[int, int, int, int, int], current:tuple[int, int, int, int, int]):
	weight = cvor[4]**2 - int(math.sqrt(cvor[1]*cvor[0]))
	if current[3] != cvor[3]:
		weight = weight // 2
		if cvor[2] > 0:
			weight = weight // 2

	team = current[3]
	if cvor[3] == team:
		if cvor[4] == 0 and cvor[0] != 0:
			weight = sys.maxsize
		if cvor[1] == cvor[4]:
			weight = sys.maxsize
	return weight

def samostampaci(x,y,map):
	svi=True
	for i in range (len(map)):
		for j in range (len(map[0])):
			if map[i][j][3]==map[x][y][3] and map[i][j][2] == 0:
					svi=False
	return svi


def minVirus(susedni:list[tuple[int, int, int, int, int]], team:int, current:tuple[int, int, int, int, int])->int:
	minCvor = sys.maxsize
	notOwned = -1
	global daju
	minp = -1

	# minCvor - broj virusa u cvoru -> razlika broja virusa i rama
	# minp - pozicija cvora
	for i in range(0,4):
		if computeWeight(susedni[i], current) < minCvor and not nadji(susedni[i]) and susedni[i] != current:
			minCvor = computeWeight(susedni[i], current)
			minp = i
		
		if susedni[i][3] != team and susedni[i][3] != 0:
			if notOwned != -1:
				if computeWeight(susedni[i], current) < computeWeight(susedni[notOwned], current):
					notOwned = i
			else:
				notOwned = i

	if notOwned != -1:
		return notOwned + 1
	if susedni[minp][3] == team:
		daju.append(current)
	return minp + 1

def act(row: int, column: int, team: int, turn: int, mycash: int, opcash: int, map:list[list[tuple[int, int, int, int, int]]])->int:
	global potez
	global daju
	if potez != turn:
		potez = turn
		daju = []

	if map[row][column][4] == 0:
		return 0
	rownum = len(map)
	columnnum = len(map[0])
	susedni = []

	if row - 1 < 0:
		susedni.append(map[row][column])
	else:
		susedni.append(map[row-1][column])	# gore

	if column + 1 >= columnnum:
		susedni.append(map[row][column])
	else:
		susedni.append(map[row][column+1])	# desno

	if row + 1 >= rownum:
		susedni.append(map[row][column])
	else:
		susedni.append(map[row+1][column])	# dole

	if column - 1 < 0:
		susedni.append(map[row][column])
	else:
		susedni.append(map[row][column-1])	# levo

	if map[row][column][2] > 0:
		if not samostampaci(row, column, map):
			return 5
		okruzenStampacima = True
		for i in range(0,4):
			if susedni[i][3] != team:
				okruzenStampacima = False
		if okruzenStampacima:
			return 5

	akcija = minVirus(susedni, team, map[row][column])
	return akcija
	