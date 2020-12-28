from input_data.import_inputs import population, electoral_votes
import random
import itertools
import numpy as np
import time
from collections import Counter




def brute_force(states, population, electoral_votes):
    number_checked = 0
    # vote_results = list()
    total_electoral_votes = sum([electoral_votes[state] for state in states])
    total_voters = sum([population[state] for state in states])
    min_voters_won = total_voters
    best_combination = None
    for outcome in itertools.product([True, False], repeat=len(states)):
        number_checked += 1
        electoral_votes_won = sum([electoral_votes[states[ii]] for ii in range(len(states)) if outcome[ii]])
        if electoral_votes_won > total_electoral_votes / 2:
            voters_won = sum([population[states[ii]] / 2 for ii in range(len(states)) if outcome[ii]])
            # vote_results.append([outcome, voters_won / total_voters])
            if min_voters_won > voters_won:
                min_voters_won = voters_won
                best_combination = [states[ii] for ii in range(len(states)) if outcome[ii]]
    return min_voters_won/total_voters, number_checked, best_combination

def generate_order(states, population, electoral_votes):
    state_dict = dict()
    for state in states:
        if electoral_votes[state] in state_dict:
            state_dict[electoral_votes[state]].append(state)
        else:
            state_dict[electoral_votes[state]] = [state]
    for electoral_votes_amount, states_at_that_amount in state_dict.items():
        state_populations = [population[state] for state in states_at_that_amount]
        order = np.argsort(state_populations)
        state_dict[electoral_votes_amount] = list(np.array(states_at_that_amount)[order])
    return state_dict

def algorithm_1(states, population, electoral_votes):
    """
    group states by number of ec votes

    """
    state_dict = generate_order(states, population, electoral_votes)
    electoral_votes_amounts = list(state_dict.keys())
    electoral_votes_amounts.sort()
    multiplicities = [len(state_dict[electoral_votes_amount]) for electoral_votes_amount in electoral_votes_amounts]

    total_electoral_votes = sum([electoral_votes[state] for state in states])
    total_voters = sum([population[state] for state in states])
    min_voters_won = total_voters
    best_combination = None

    number_checked = 0
    for outcome in itertools.product(*[range(multiplicity + 1) for multiplicity in multiplicities]):
        number_checked += 1
        electoral_votes_won = np.dot(outcome, electoral_votes_amounts)
        if electoral_votes_won > total_electoral_votes / 2:
            states_won = [state_dict[electoral_votes_amount][0:multiplicity] for electoral_votes_amount, multiplicity in zip(electoral_votes_amounts, outcome)]
            states_won = [item for sublist in states_won for item in sublist]
            voters_won = sum([population[state] / 2 for state in states_won])
            if min_voters_won > voters_won:
                min_voters_won = voters_won
                best_combination = states_won
    return min_voters_won / total_voters, number_checked, best_combination


state_list = list(population.keys())

number_to_consider = 20

states = random.sample(state_list, number_to_consider)
now = time.time()
print(brute_force(states, population, electoral_votes))
print(f'time for {number_to_consider} states {time.time() - now}')

now = time.time()
print(algorithm_1(states, population, electoral_votes))
print(f'time for {number_to_consider} states {time.time() - now}')

print('hi')
print('there')