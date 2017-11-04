#!/usr/bin/env python2.7

import sys
import time
from copy import deepcopy

# Global Variables
NFA = {
	"machineName": "",
	"alphabet": [],
	"states": [],
	"startState": "",
	"acceptingStates": [],
	"transferFunction": {}
}

DFA = {
	"machineName": "",
	"alphabet": [],
	"states": ["phi"],
	"startState": "",
	"acceptingStates": [],
	"transferFunction": {}
}

stateMap = {}

# Functions
def read_rules(line):
	global NFA
	rules = NFA["transferFunction"]
	lineList = line.split(',')
	initialState = lineList[0]
	inputSymbol = lineList[1]
	newState = lineList[2]
	if (inputSymbol not in rules[initialState]):
		rules[initialState][inputSymbol]= []
	rules[initialState][inputSymbol].append(newState)


def explore_individual(state, symbol):
	global NFA
	if(symbol in NFA["transferFunction"][state]):
		return NFA["transferFunction"][state][symbol]
	else:
		return ''


def explore(remainingStates):
	global NFA
	global DFA
	global newStates
	global statesToExplore
	global stateMap

	stateString = ''.join(remainingStates)
	if [i for i in NFA["acceptingStates"] if i in remainingStates]:
		DFA["acceptingStates"].append(stateString)
	if (stateString not in newStates):
		newStates.append(stateString)
		statesToExplore.append(stateString)
		stateMap[stateString] = remainingStates

	result = {}
	for symbol in NFA["alphabet"]:
		result[symbol] = ""
		tempStates = []
		for state in remainingStates:
			tempResult = explore_individual (state, symbol)
			if (tempResult != '' and (tempResult not in tempStates)):
				tempStates.append(tempResult) 

		tempList = []
		if (len(tempStates) == 0):
			result[symbol] = 'phi'
		else:
			for resultStates in tempStates:
				tempList.extend(resultStates)
			result[symbol] = ''.join(tempList)

		if (stateString not in  DFA["transferFunction"]):
			DFA["transferFunction"][stateString] = {}
		DFA["transferFunction"][stateString][symbol] = result[symbol]

		if (result[symbol] not in newStates):
			newStates.append(result[symbol])
			statesToExplore.append(result[symbol])
			stateMap[result[symbol]] = tempList

# Main Function

machine = sys.argv[1]
f = open(machine, "r")

for i, line in enumerate(f):
	line = line.rstrip()
	if i == 0:
		if ":" in line:
			colon = line.index(':')
			machineName = line[:colon]
			NFA["machineName"] = machineName
		else:
			machineName = line
			NFA["machineName"] = machineName

	elif i == 1:
		alphabet = line.split(',')
		NFA["alphabet"] = alphabet

	elif i == 2:
		states = line.split(',')
		NFA["states"] = states
		for state in states:
			NFA["transferFunction"][state] = {}
			stateMap[state] = [state]
	elif i == 3:
		startState = line
		NFA["startState"] = startState
	elif i == 4:
		acceptingStates = line.split(',')
		NFA["acceptingStates"] = acceptingStates
	else:
		read_rules(line)

f.close()


DFA["machineName"] = NFA["machineName"] + " to DFA"
DFA["alphabet"] = NFA["alphabet"]
DFA["startState"] = NFA["startState"]

statesToExplore = deepcopy(NFA["states"])
newStates = deepcopy(statesToExplore)
newStates.append('phi')

while (len(statesToExplore)>0):
	element = statesToExplore[0]
	statesToExplore.pop(0)
	explore(stateMap[element])

for key in stateMap:
	DFA["states"].append(key)

print(DFA["machineName"])
print(",".join(DFA["alphabet"]))
print(",".join(DFA["states"]))
print(DFA["startState"])
print(",".join(DFA["acceptingStates"]))

for item in DFA["transferFunction"].items():
	init = item[0]
	for states in item[1].items():
		print(init + "," + states[0] + "," + states[1])
