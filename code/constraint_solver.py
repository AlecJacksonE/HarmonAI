# import constraint

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


# hard-coded for 2 agents only, returns list for 1st agent
def note_list(notes):
    # notes = create_variables(freq_list) # should already be variables
    t_total = len(notes)
    order = [-1 for _ in range(t_total)]
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
        print("Agent {}:".format(i), solutions[i])


def main():
    # TEST
    test_freq_list = [[(8, 100), (2, 100)], [(3, 100), (9, 100)], [(10, 100), (4, 100)], [], [(11, 100)]]
    num_agents = 2
    solutions = get_solutions(test_freq_list, num_agents)
    print_solutions(solutions)
    print()

    test_freq_list = [[(8, 100), (2, 100), (10, 90)], [(3, 100), (9, 100)], [(10, 100), (4, 100), (20, 100)], [], [(11, 100)]]
    num_agents = 3
    solutions = get_solutions(test_freq_list, num_agents)
    print_solutions(solutions)


if __name__ == '__main__':
    main()
