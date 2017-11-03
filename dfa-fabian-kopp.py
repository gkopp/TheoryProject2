#!/usr/bin/env python2.7

import sys

# File containing the finite automata to be simulated
FA = sys.argv[1]

# File containing multiple character strings to run against the machine
test_strings = sys.argv[2]

# Read in and process finite automata
line_num = 0
rule_num = 0
for line in open(FA, "r+"):
    line = line.strip()

    # Name of the FA Program
    if line_num == 0:
        machine_name = line.split(':')[0]
        print line

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

        # create another dictionary to translate back at the end of the program
        # for meaningful output purposes
        translate_back = {}
        for x in translate:
            i = translate[x]
            translate_back[i] = x

    # Start state
    elif line_num == 3:
        start_state = translate[line]

    # Accepting states
    elif line_num == 4:
        state_list = line.split(',')
        accepting_states = []
        for state_name in state_list:
            accepting_states.append(translate[state_name])

    # Transition rules
    else:
        transition = line.split(',')
        initial_state = translate[transition[0]]
        input_symbol = transition[1]
        new_state = translate[transition[2]]

        # assign sequential rule # and echo rule to stdout per instructions in 2.1
        rule_num += 1
        print str(rule_num) + ":" + line

        # For each rule read in of the form "initial state, input, new state," create
        # an adjacency matrix entry such that the row corresponds to the initial state,
        # the column corresponds to the new state, and the point where these 2 intersect
        # is a set containing the input characters that make the transition from initial
        # to new happen
        adj_matrix[initial_state][new_state].add(input_symbol)

        # added after the fact as a way to associate rule numbers with transitions which
        # is required for output
        transition_record = (input_symbol, rule_num)
        adj_matrix[initial_state][new_state].add(transition_record) 
    line_num += 1

# Read in file with character strings to run against machine and test strings
for line in open(test_strings, 'r+'):
    line = line.strip()
    print "String: " + line

    current_state = start_state
    visited = [current_state]

    found = False
    step_number = 0
    invalid = False
    for symbol in line:
        step_number += 1
        for possible_state in range(state_num):
            if symbol in adj_matrix[current_state][possible_state]:

                # find what rule number is associated with that transition
                for entry in adj_matrix[current_state][possible_state]:
                    if type(entry) == tuple:
                        if entry[0] == symbol:
                            rule_number = entry[1]

                print str(step_number) + "," + str(rule_number) + "," + translate_back[current_state]+ "," + symbol + "," + translate_back[possible_state]
                current_state = possible_state
                visited.append(current_state)
                found = True
                break

        # Check for invalid transitions
        if found == False:
            invalid = True
            break

    if current_state in accepting_states and invalid == False:    
        print "Accepted"
    
    else:
        print "Rejected"

