#!/usr/bin/env python2.7

import sys

# File containing the finite automata to be simulated
FA = sys.argv[1]

# File containing multiple character strings to run against the machine
test_strings = sys.argv[2]

# Read in and process finite automata
line_num = 0
for line in open(FA, "r+"):
    line = line.strip()

    # Name of the FA Program
    if line_num == 0:
        machine_name = line.split(':')[0]
        print "Machine name: " + machine_name

    # Alphabet to be used
    elif line_num == 1:
        alphabet = line.split(',')

    # Names of states
    elif line_num == 2:
        states = line.split(',')
        state_num = len(states)

        # initialize graph adjacency matrix representation of machine
        adj_matrix = []
        for i in range(state_num):
            adj_matrix.append([])
            for j in range(state_num):
                adj_matrix[i].append(set()) # use set to avoid duplicates

        # create dictionary to assign sequential int values to given state names
        # (this will making indexing the adjacency matrix easier)
        i = 0
        translate = {}
        for state in states:
            translate[state] = i
            i = i + 1

    # Start state
    elif line_num == 3:
        start_state = translate[line]

    # Accepting states
    elif line_num == 4:
        accepting_states = line.split(',')

    # Transition rules
    else:
        transition = line.split(',')
        initial_state = translate[transition[0]]
        input_symbol = transition[1]
        new_state = translate[transition[2]]

        # For each rule read in of the form "initial state, input, new state," create
        # an adjacency matrix entry such that the row corresponds to the initial state,
        # the column corresponds to the new state, and the point where these 2 intersect
        # is a set containing the input characters that make the transition from initial
        # to new happen
        adj_matrix[initial_state][new_state].add(input_symbol)
       
    line_num += 1

# Read in file with character strings to run against machine and test strings
for line in open(test_strings, 'r+'):
    line = line.strip()
    current_state = start_state
    visited = [current_state]

    found = False
    for symbol in line:
        for possible_state in range(state_num):
            if symbol in adj_matrix[current_state][possible_state]:
                current_state = possible_state
                visited.append(current_state)
                found = True
                break
        if found == False:
            print "Impossible Transition"
    print visited

