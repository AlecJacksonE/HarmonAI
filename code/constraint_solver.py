import sys
sys.path.append('C:/Users/rodri/')
import time
import random
import pyGM as gm

"""
# future changes using constraint-python

def create_variables(freq_list, t_interval, agents):
    # Variables: each note (i) 
    # ? X = [i for i in range(t_total)] # one variable for each t
    # Domain: list of each agents (a note must be played by one of the agents
    #

# first t: assign agent to note one-by-one.
# every iteration afterwards:
#   agent should be assigned to the note with min distance from previous note (min abs value)

# OR

# Variables: total list of notes per agent
"""


def create_variables(freq_list):  # pre-processing variables
    note_order = []
    for t in freq_list:  # for each t
        notes = [n[0] if 0 <= n[0] <= 24 else None for n in t]  # just collect the number of note to play, ignore out of bounds
        note_order.append(notes)
    return note_order


def min_constraint(x, prev):
    diff = [abs(i - prev) for i in x]
    if diff:
        return x[diff.index(min(diff))]
    return -1


# returns list for 1st agent
def note_list(notes):
    # notes = create_variables(freq_list) # should already be variables
    t_total = len(notes)
    order = [-1 for _ in range(t_total)]
    if notes:
        order[0] = notes[0][0] if len(notes[0]) != 0 else -1  # for t == 0, automatically choose the first one
    for t in range(1, t_total):
        order[t] = min_constraint(notes[t], order[t-1])
    return order


# hard-coded to get 2nd agent solution
def complement_solution(solution, notes):
    complement = [[] for _ in solution]
    for i in range(len(solution)):
        update = [n for n in notes[i] if n != solution[i]]
        complement[i] = update[0] if update else -1  # take next option after first choice from agent
    return complement


def update_variables(solution, notes):
    update = [[] for _ in solution]
    for i in range(len(solution)):
        update[i] = [n for n in notes[i] if n != solution[i]]
    return update


def get_solutions(freq_list, num_agents):
    # create_variables: Pre-process freq list into list of variables N[t][i], where N[t] is a list of notes at time=t
    variables = create_variables(freq_list)

    solutions = []
    for a in range(num_agents):
        # note_list: solves for one agent's optimal choice based on proximity (search based on min distance)
        solutions.append(note_list(variables))
        variables = update_variables(solutions[-1], variables)
    return solutions


def print_solutions(solutions):
    for i in range(1, len(solutions)+1):
        print("Agent {}:".format(i), solutions[i-1])


def get_index(t, i, num_agents):
    return i+(num_agents*t)


def in_set(set, vi, vj):
    if vi in set:
        if vj in set:
            return True
    return False


def convert_variable_to_list(set, length, num_agents):
    notes = []
    for i in range(num_agents):
        # solutions.append([set[get_index(t, i)] for t in length])
        agent = []
        for t in range(length):
            agent.append(set[get_index(t, i, num_agents)])
        notes.append(agent)
    return notes


def score_function(notes, length, num_agents):
    # print_solutions(notes)
    total_sum = 0
    for n in range(num_agents):
        agent_sum = 0
        for t in range(length-1):
            if notes[n][t+1] and notes[n][t] and notes[n][t+1] != -1 and notes[n][t] != -1:
                agent_sum += abs(notes[n][t+1] - notes[n][t])
        total_sum+=agent_sum
    # print("score: ", total_sum)
    return total_sum


def brute_force(freq_list, num_agents):
    freq_list=create_variables(freq_list)
    # Variables
    X = []
    for t in range(len(freq_list)):
        for i in range(num_agents):
            X.append(gm.Var(get_index(t, i, num_agents), 25))

    # Factors (Constraints)
    # print("freq_list: ", freq_list)
    factors = []
    for t in range(len(freq_list)):
        # print("t: ", t)
        if len(freq_list[t]) < 2 :
            fi = gm.Factor([X[get_index(t, 0, num_agents)]], 1.0)
            factors.append(fi)
            continue
        for i in range(len(freq_list[t])):
            for j in range(i+1, len(freq_list[t])):
                fij = gm.Factor([X[get_index(t, i, num_agents)], X[get_index(t, j, num_agents)]], 1.0)  # creates factor
                # print("\ti: ", i)
                # print("\tj: ", j)
                # print("\tget_index: ", get_index(t, i, num_agents))
                for vi in range(25):                                          # rules out if same note played on t
                    for vj in range(25):                                      # or if not in set of possible notes
                        fij[vi, vj] = 1 if (vi!=vj and in_set(freq_list[t], vi, vj)) else 0
                factors.append(fij)
                # print(fij.table)

    # create graph model based on input
    model = gm.GraphModel(factors)
    # print("X:", model.X)
    # print("check solution: ", model.value([8, 2, 9, 3, 10, 4]))

    allX = gm.VarSet(model.X)
    nr = allX.nrStates()
    solutions = []
    num_solutions = 0
    for idx in range(nr):
        tup = allX.ind2sub(idx)
        # print(tup)
        if model.value(tup) == 1.0:
            print("Solution found: ", tup)
            solutions.append(tup)
            num_solutions += 1

    print("Number of solutions: ", num_solutions)

    min_sample = []
    min_sample_score = float('inf')
    for solution in solutions:
        sample = convert_variable_to_list(solution, len(freq_list), num_agents)
        score = score_function(sample, len(freq_list), num_agents)
        if score < min_sample_score:
            # print("Found new min score: ", score)
            min_sample = sample
            min_sample_score = score
    print("Best solution found with minimum distance score: ", min_sample_score)
    # print_solutions(min_sample)

    return min_sample


def convert_to_sample(freq_list, num_agents):
    sample = []
    length = len(freq_list)
    for i in range(num_agents):
        agent = []
        for t in range(length):
            agent.append(freq_list[t][i])
        sample.append(agent)
    return sample


def get_random_swap(sample, num_agents):
    if num_agents < 2:  # Just one agent cannot swap
        return sample

    # random choices
    t = random.randint(0, len(sample)-1)
    agent_options = [i for i in range(num_agents)]
    agent1 = random.choice(agent_options)
    agent_options.remove(agent1)
    agent2 = random.choice(agent_options)

    # print("sample before swapping at time {}: ".format(t), sample)

    # swap
    copy = sample[agent1][t]
    sample[agent1][t] = sample[agent2][t]
    sample[agent2][t] = copy

    # print("swapped agent {} and agent {} at time {}".format(agent1+1, agent2+1, t))
    # print("sample after swapping: at time {}".format(t), sample)
    return sample


def random_swapping(freq_list, num_agents, numIter=100, maxAttempts=10000000):
    # update list to variables
    freq_list = create_variables(freq_list)

    # Create into solution
    sample = convert_to_sample(freq_list, num_agents)
    # print("sample: ", sample)
    # while iterations or no new productive change
    # find random swap
    # test if lower score, then update

    iterations = 0
    attempts = 0
    min_sample = sample
    min_sample_score = score_function(sample, len(sample), num_agents)
    print("initial min score: ", min_sample_score)
    while iterations < numIter and attempts < maxAttempts:
        sample = get_random_swap(sample, num_agents)
        score = score_function(sample, len(freq_list), num_agents)
        attempts += 1
        if score < min_sample_score:
            attempts = 0
            iterations += 1
            print("Found new min score: ", score)
            min_sample = sample
            min_sample_score = score
    if attempts == maxAttempts:
        print("reached max attempts. exited loop")
    print("Best solution found with minimum distance score: ", min_sample_score)
    print("Number of swaps until solution found: ", iterations)
    print_solutions(min_sample)

    return min_sample


def swapping_versus_search(test_freq_list, num_agents):
    print("original test_freq_list: ", test_freq_list)

    print("Testing random method")
    start = time.time()
    swap_solutions = random_swapping(test_freq_list, num_agents)
    end = time.time()
    print("total elapsed time: ", end - start)
    print_solutions(swap_solutions)

    print("Testing heuristic search method")
    start = time.time()
    search_solutions = get_solutions(test_freq_list, num_agents)
    end = time.time()
    print("total elapsed time: ", end - start)
    print_solutions(search_solutions)


def make_test_freq(total_time, num_agents):
    test_freq_list = []
    for i in range(total_time):
        t = []
        for a in range(num_agents):
            t.append((random.randint(-1,24), 100))
        test_freq_list.append(t)
    return test_freq_list


def main():
    # TEST
    # test_freq_list = [[(8, 100), (2, 100)], [(3, 100), (9, 100)], [(10, 100), (4, 100)], [], [(11, 100)]]
    # num_agents = 2
    # solutions = get_solutions(test_freq_list, num_agents)
    # print_solutions(solutions)
    # print()
    #
    # test_freq_list = [[(8, 100), (2, 100), (10, 90)], [(3, 100), (9, 100)], [(10, 100), (4, 100), (20, 100)], [], [(11, 100)]]
    # num_agents = 3
    # solutions = get_solutions(test_freq_list, num_agents)
    # print_solutions(solutions)

    # Brute Force
    # print("Four notes: ")
    # test_freq_list = [[(8, 100), (2, 100)], [(3, 100), (9, 100)]]
    # num_agents = 2
    # print("test_freq_list: ", test_freq_list)
    # print("Testing brute force")
    # start = time.time()
    # solutions = brute_force(test_freq_list, num_agents)
    # end = time.time()
    # print("total elapsed time: ", end - start)
    # print_solutions(solutions)
    #
    # # print()
    # # print("Five notes: ")
    # # test_freq_list = [[(8, 100), (2, 100)], [(3, 100), (9, 100)], [(10, 100)]]
    # # num_agents = 2
    # # print("test_freq_list: ", test_freq_list)
    # # print("Testing brute force")
    # # start = time.time()
    # # solutions = brute_force(test_freq_list, num_agents)
    # # end = time.time()
    # # print("total elapsed time: ", end - start)
    # # print_solutions(solutions)
    #
    # print()
    # print("Six notes: ")
    # test_freq_list = [[(8, 100), (2, 100)], [(3, 100), (9, 100)], [(10, 100), (4, 100)]]
    # num_agents = 2
    # print("test_freq_list: ", test_freq_list)
    # print("Testing brute force")
    # start = time.time()
    # solutions = brute_force(test_freq_list, num_agents)
    # end = time.time()
    # print("total elapsed time: ", end - start)
    # print_solutions(solutions)

    # Random Testing
    # test_freq_list = [[(8, 100), (2, 100)], [(3, 100), (9, 100)], [(10, 100), (4, 100)]]
    # num_agents = 2
    # print("test_freq_list: ", test_freq_list)
    # print("Testing random testing")
    # start = time.time()
    # solutions = random_swapping(test_freq_list, num_agents)
    # end = time.time()
    # print("total elapsed time: ", end - start)
    # print_solutions(solutions)


    total_time = 3
    num_agents = 3
    test_freq_list = []
    for i in range(total_time):
        t = []
        for a in range(num_agents):
            t.append((random.randint(-1,24), 100))
        test_freq_list.append(t)

    swapping_versus_search(test_freq_list, num_agents)

    # test_freq_list = [[(8, 100), (2, 100), (10, 90)], [(3, 100), (9, 100), (11, 100)], [(10, 100), (4, 100), (20, 100)], [(-1, 100), (-1, 100), (-1,100)], [(11, 100), (-1, 100), (-1, 100)]]
    # num_agents = 3
    # print("test_freq_list: ", test_freq_list)
    # print("Testing random testing")
    # start = time.time()
    # solutions = random_swapping(test_freq_list, num_agents)
    # end = time.time()
    # print("total elapsed time: ", end - start)
    # print_solutions(solutions)

    test_freq_list = []
    total_time = 4
    num_agents = 3
    for i in range(total_time):
        t = []
        for a in range(num_agents):
            t.append((random.randint(-1, 24), 100))
        test_freq_list.append(t)

    swapping_versus_search(test_freq_list, num_agents)
    # test_freq_list = [[(8, 100), (2, 100), (10, 90)], [(3, 100), (9, 100), (11, 100)], [(10, 100), (4, 100), (20, 100)], [(-1, 100), (-1, 100), (-1,100)], [(11, 100), (-1, 100), (-1, 100)]]
    # num_agents = 3
    # print("test_freq_list: ", test_freq_list)
    # print("Testing random testing")
    # start = time.time()
    # solutions = random_swapping(test_freq_list, num_agents)
    # end = time.time()
    # print("total elapsed time: ", end - start)
    # print_solutions(solutions)



if __name__ == '__main__':
    main()
