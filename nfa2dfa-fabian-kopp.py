#!/usr/bin/env python2.7

import sys
from copy import deepcopy
from itertools import combinations

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
reachableStates = []
foundStates = []


# Functions
def readRules(line):
	
	global NFA

	# process each element of rule for transfer function
	rules = NFA["transferFunction"]
	lineList = line.split(',')
	initialState = lineList[0]
	inputSymbol = lineList[1]
	newState = lineList[2]

	# add rule if not included already
	if (inputSymbol not in rules[initialState]):
		rules[initialState][inputSymbol] = []
	rules[initialState][inputSymbol].append(newState)


def exploreState(state, symbol):

	global NFA

	# search for path in transfer function with specific char
	if(symbol in NFA["transferFunction"][state]):
		return NFA["transferFunction"][state][symbol]
	else:
		return "null"


def explore(remainingStates):

	global NFA
	global DFA
	global newStates
	global statesToExplore
	global stateMap
	global reachableStates
	global foundStates

	stateString = ''.join(remainingStates)

	# check if state string has been used, if not, add to states
	if (stateString not in newStates):
		newStates.append(stateString)
		statesToExplore.append(stateString)
		stateMap[stateString] = remainingStates

	# iterate over every symbol in alphabet
	result = {}
	for symbol in NFA["alphabet"]:
		result[symbol] = ""
		tempStates = []

		# Check state for valid path to next state
		for state in remainingStates:
			tempResult = exploreState(state, symbol)
			# add result if valid path was found
			if(tempResult != "null" and (tempResult not in tempStates)):
				tempStates.append(tempResult) 

		tempList = []
		# If no states to go to, go to trap state
		if (len(tempStates) == 0):
			result[symbol] = 'phi' 
		else:
			# add each state to list of reachable states
			for resultStates in tempStates:
				tempList.extend(resultStates)
			tempList = list(set(tempList)) # need to get rid of duplicates
			reachableStates = deepcopy(tempList)

			foundStates = []
			checkStates(reachableStates)
			finalReachableStates = deepcopy(reachableStates)
			finalReachableStates.sort()
			result[symbol] = ''.join(finalReachableStates)

		# add state to transfer function if needed
		if (stateString not in DFA["transferFunction"]):
			DFA["transferFunction"][stateString] = {}
		DFA["transferFunction"][stateString][symbol] = result[symbol]

		# add result to states
		if (result[symbol] not in newStates):
			newStates.append(result[symbol])
			statesToExplore.append(result[symbol])
			stateMap[result[symbol]] = finalReachableStates

def getReachableStates(state):

	global NFA
	global reachableStates
	global foundStates

	# if value on path is epsilon, take next state into account
	foundStates.append(state)
	if('~' in NFA["transferFunction"][state]):
		originalStates = NFA["transferFunction"][state]['~']
		newStates = list(set(originalStates).difference(set(reachableStates)))
		reachableStates.extend(newStates)
		statesToCheck = list(set(originalStates).difference(set(foundStates)))
		# if there are new states, check them
		if(len(statesToCheck) > 0):
			checkStates(statesToCheck)

def checkStates(states):

	global reachableStates
	global foundStates

	for state in states:
		getReachableStates(state)

def getAcceptingStates(states):

    global NFA 
    global DFA
    
    acceptingStates = ''.join(states)
    for state in states:
    	# If state was an accepting state and is not already included, add to accepting states
        if (state in NFA["acceptingStates"] and (acceptingStates not in DFA["acceptingStates"])):
            DFA["acceptingStates"].append(acceptingStates)
            break

# Main Function

# Parse machine rules, first three lines
machine = sys.argv[1]
f = open(machine, "r")

for i, line in enumerate(f):
	line = line.rstrip()
	if i == 0:
		if ":" in line:
			stop = line.index(':')
			machineName = line[:stop]
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
		readRules(line)

f.close()

# add labels to DFA
DFA["machineName"] = NFA["machineName"] + " - converted to  DFA"
DFA["alphabet"] = NFA["alphabet"]


# create initieal state list
statesToExplore = deepcopy(NFA["states"])
newStates = deepcopy(statesToExplore)

newStates.append("phi")

for i in range(1,len(NFA["states"])+1):
    comboList = list(combinations(NFA["states"],i))
    for state in comboList:
        state = list(state)
        state.sort()
        newState = ''.join(state)
        DFA["states"].append(newState)

# add trap state if needed
DFA["transferFunction"]["phi"] = {}
for char in NFA["alphabet"]:
	DFA["transferFunction"]["phi"][char] = "phi"

# check each state that hasn't been traversed
while (len(statesToExplore) > 0):
	element = statesToExplore[0]
	statesToExplore.pop(0)

	reachableStates = deepcopy(stateMap[element])
	foundStates = []
	checkStates(stateMap[element])

	reachableStates.sort()

	if(len(DFA["startState"]) == 0):
		DFA["startState"] = ''.join(reachableStates)
	getAcceptingStates(reachableStates)
	explore(reachableStates)

# send output to csv file
outputName = sys.argv[1].replace(".txt","-DFA.csv")
outputFile = open(outputName, "w")

outputFile.write(DFA["machineName"] + "\n")
outputFile.write(",".join(DFA["alphabet"]) + "\n")
outputFile.write(",".join(DFA["states"]) + "\n" )
outputFile.write(DFA["startState"]+ "\n")
outputFile.write(",".join(DFA["acceptingStates"])+ "\n")

for item in DFA["transferFunction"].items():
	init = item[0]
	for states in item[1].items():
		outputFile.write(init + "," + states[0] + "," + states[1]+ "\n")

outputFile.close()