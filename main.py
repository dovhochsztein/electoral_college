from input_data.import_inputs import population, electoral_votes, maine_districts, nebraska_districts
import random
import itertools
import numpy as np
import time
import pandas as pd
import math


def brute_force(states, population, electoral_votes, special_states):

    # for special_state in special_states.keys():
    #     if special_state in states:
    #         states.remove(special_state)
    #     else:
    #         special_states.pop(special_state)

    number_checked = 0
    # vote_results = list()
    total_electoral_votes = sum([electoral_votes[state] for state in states])
    total_voters = sum([population[state] for state in states])
    min_voters_won = total_voters
    best_combination = None
    best_electoral_votes_won = None

    # for special_state_outcome in itertools.product(1):
    for special_state_outcome in [0]:


        for outcome in itertools.product([True, False], repeat=len(states)):
            number_checked += 1
            electoral_votes_won = sum([electoral_votes[states[ii]] for ii in range(len(states)) if outcome[ii]])
            if electoral_votes_won > total_electoral_votes / 2:
                voters_won = sum([math.ceil(population[states[ii]] / 2) for ii in range(len(states)) if outcome[ii]])
                # vote_results.append([outcome, voters_won / total_voters])
                if min_voters_won > voters_won:
                    best_electoral_votes_won = electoral_votes_won
                    min_voters_won = voters_won
                    best_combination = [states[ii] for ii in range(len(states)) if outcome[ii]]
    best_combination.sort()
    print(f'voters won: {min_voters_won} of {total_voters}\nPercentage: {min_voters_won / total_voters}')
    print(f'number checked: {number_checked}')
    print(f'combination of states: {best_combination}')
    print(f'electoral votes won: {best_electoral_votes_won} of {total_electoral_votes}   ({int(math.ceil(total_electoral_votes / 2))} needed)')
    return min_voters_won/total_voters, number_checked, best_combination, best_electoral_votes_won, total_electoral_votes


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


def algorithm_1(states, population, electoral_votes, special_states):
    """
    group states by number of ec votes

    """
    total_electoral_votes = sum([electoral_votes[state] for state in states])
    total_voters = sum([population[state] for state in states])

    new_special_states = special_states.copy()
    for special_state in special_states.keys():
        if special_state in states:
            states.remove(special_state)
        else:
            new_special_states.pop(special_state)
    special_states = new_special_states

    state_dict = generate_order(states, population, electoral_votes)
    electoral_votes_amounts = list(state_dict.keys())
    electoral_votes_amounts.sort()
    highest_vote_amount = max(electoral_votes_amounts)
    multiplicities = [len(state_dict[electoral_votes_amount]) for electoral_votes_amount in electoral_votes_amounts]


    min_voters_won = total_voters
    best_combination = None
    best_electoral_votes_won = None

    number_checked = 0
    # skipped_1 = 0
    # skipped_2 = 0
    special_state_electoral_votes = [len(special_state) for special_state in special_states.values()]
    special_states_order = {state: list(np.array(list(value))[np.argsort(list(value.values()))])
                            for state, value in special_states.items()}
    for special_state_outcome in itertools.product(*[range(len(special_state) + 1) for special_state in special_states.values()]):
        special_state_electoral_votes_won = sum(special_state_outcome) +\
                                            2 * np.sum(np.array(special_state_electoral_votes) == np.array(special_state_outcome))
        special_states_won = {state: districts[0:districts_won] for ((state, districts), districts_won) in zip(special_states_order.items(), special_state_outcome)}
        special_states_voters_won = sum([math.ceil(special_states[state][district] / 2) for state, districts in special_states_won.items() for district in districts])
        special_states_won = list(itertools.chain.from_iterable(list(special_states_won.values())))
        for outcome in itertools.product(*[range(multiplicity + 1) for multiplicity in multiplicities]):
            number_checked += 1
            electoral_votes_won = np.dot(outcome, electoral_votes_amounts)
            if special_state_electoral_votes_won + electoral_votes_won > total_electoral_votes / 2:
                lowest_vote_total_index = next((i for i, x in enumerate(outcome) if x > 0), None)
                if special_state_electoral_votes_won + electoral_votes_won > total_electoral_votes / 2 + highest_vote_amount:
                    # skipped_1 += 1
                    continue
                if lowest_vote_total_index is not None:
                    lowest_vote_total = electoral_votes_amounts[lowest_vote_total_index]
                    if special_state_electoral_votes_won + electoral_votes_won > total_electoral_votes / 2 + lowest_vote_total:
                        # skipped_2 += 1
                        continue
                states_won = [item for electoral_votes_amount, multiplicity in zip(electoral_votes_amounts, outcome)
                              for item in state_dict[electoral_votes_amount][0:multiplicity]]

                voters_won = sum([math.ceil(population[state] / 2) for state in states_won])
                if min_voters_won > special_states_voters_won + voters_won:
                    best_electoral_votes_won = special_state_electoral_votes_won + electoral_votes_won
                    min_voters_won = special_states_voters_won + voters_won
                    best_combination = special_states_won + states_won
    best_combination.sort()
    # print(skipped_1)
    # print(skipped_2)
    print(f'voters won: {min_voters_won} of {total_voters}\nPercentage: {min_voters_won / total_voters}')
    print(f'number checked: {number_checked}')
    print(f'combination of states: {best_combination}')
    print(f'electoral votes won: {best_electoral_votes_won} of {total_electoral_votes}   ({int(math.ceil(total_electoral_votes / 2))} needed)')
    return min_voters_won / total_voters, number_checked, best_combination, best_electoral_votes_won, total_electoral_votes


state_list = list(population.keys())

time_brute = list()
number_checked_brute = list()
time_algorithm_1 = list()
number_checked_algorithm_1 = list()

numbers_to_consider = [5, 10, 15, 20, 25, 30, 51]
numbers_to_consider = [5, 6, 7, 8, 9, 10, 15, 20, 51]
for number_to_consider in numbers_to_consider:
    states = random.sample(state_list, number_to_consider)
    for special_states in [{}, {'Maine': maine_districts,
                                'Nebraska': nebraska_districts}]:

        # special_states = {'Maine': maine_districts,
        #                   'Nebraska': nebraska_districts}

        if 'Nebraska' not in states:
            states[0] = 'Nebraska'
        if 'Maine' not in states:
            states[1] = 'Maine'

        if number_to_consider <= 10:
            now = time.time()
            fraction, number_checked, best_combination, electoral_votes_won,\
            total_electoral_votes = brute_force(states,
                                                population,
                                                electoral_votes,
                                                special_states)
            # print(fraction, number_checked, best_combination)
            # print(f'won {electoral_votes_won} of {total_electoral_votes}')
            time_taken = time.time() - now
            print(f'time for {number_to_consider} states by brute force: {time_taken}\n')

            time_brute.append(time_taken)
            number_checked_brute.append(number_checked)

        now = time.time()
        fraction, number_checked, best_combination, electoral_votes_won,\
        total_electoral_votes = algorithm_1(states,
                                           population,
                                           electoral_votes,
                                           special_states)
        # print(fraction, number_checked, best_combination)
        # print(f'won {electoral_votes_won} of {total_electoral_votes}')
        time_taken = time.time() - now
        print(f'time for {number_to_consider} states by algorithm 1: {time_taken}\n')
        time_algorithm_1.append(time_taken)
        number_checked_algorithm_1.append(number_checked)

df = pd.DataFrame(columns=['number of states', 'number_checked_brute_force', 'time_brute_force',
                           'number_checked_algorithm_1', 'time_algorithm_1'])
df['number of states'] = [kk for jj in [[ii, ii] for ii in numbers_to_consider] for kk in jj]
df['number_checked_brute_force'].iloc[0:len(number_checked_brute)] = number_checked_brute
df['time_brute_force'].iloc[0:len(time_brute)] = time_brute
df['number_checked_algorithm_1'] = number_checked_algorithm_1
df['time_algorithm_1'] = time_algorithm_1
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)
df.to_clipboard()
