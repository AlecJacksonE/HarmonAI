import csv
import constraint_solver as cs
import music_translator as mt
import alignment as al
'''
As a guide (according to AnthemScore): (An octave higher is basically x2 the frequency)
0) F#3 = 184.997Hz     12)F#4 = 369.994Hz       24)F#5 = 739.988Hz
1) G3 = 195.998Hz      13)G4 = 391.995Hz
2) G#3 = 207.652Hz     14)G#4 = 415.304Hz
3) A3 = 220Hz          15)A4 = 439.999Hz
4) A#3 = 233.082Hz     16)A#3 = 466.163Hz
5) B3 = 246.941Hz      17)B4 = 493.883Hz
6) C4 = 261.625Hz      18)C5 = 523.25Hz
7) C#4 = 277.182Hz     19)C#5 = 554.365Hz
8) D4 = 293.664Hz      20)D5 = 587.329Hz
9) D#4 = 311.127Hz     21)D#5 = 622.253Hz
10)E4 = 329.627Hz      22)E5 = 659.254Hz
11)F4 = 349.228Hz      23)F5 = 698.455Hz
'''


def using_constraint_solver(original_csv, output_csv, tempo=120, threshold=7000, offset=0.00, leniency=0.3, num_agents=2):
    original_freq_list = mt.create_note_list(original_csv, tempo, threshold, offset=-0.08)
    # print(original_freq_list)
    original_freq_list = mt.number_converter(original_freq_list)
    original_solutions = cs.get_solutions(original_freq_list, num_agents)
    print("Original :", original_solutions[0])

    # May need to change threshold for output freq list
    output_freq_list = mt.create_note_list(output_csv, tempo, threshold=500, offset=-0.08)
    output_freq_list = mt.number_converter(output_freq_list)
    output_solutions = cs.get_solutions(output_freq_list, num_agents)
    for agent, output_solution in enumerate(output_solutions):
        index = 0
        while index < len(output_solution) and output_solution[index] == -1:
            index += 1
        output_solutions[agent] = output_solution[index:]

    # print("Output: ", output_solutions[0][20:25])
    # for output_solution in output_solutions:
    #     while output_solution[0] == -1:
    #         output_solution = output_solution[1:]
    print("Output:", output_solutions[0])
    print("Test: ")
    tester = al.Alignment()
    a, b = al.Hirschberg.align(tester, seq_a=list(original_solutions[0]), seq_b=list(output_solutions[0]))
    print(a)
    print(b)
    num_errors = 0.0

    for i in range(len(original_solutions)):
        for j in range(len(original_solutions[0])):
            if original_solutions[i][j] != output_solutions[i][j]:
                num_errors += 1

    if original_solutions and original_solutions[0]:
        return num_errors / float(len(original_solutions)*len(original_solutions[0]))
    else:
        return -1


def raw_csv_comparisons(original_csv, output_csv, difference=0.25):  # tempo=120
    cell_difference = 0
    empty_threshold = 250
    row_count = 0.0
    column_count = 0.0
    # frequency_list = []
    # interval_list = []
    # beats = round(1 / (tempo / 30.0), 2)  # changed 60 to 30 to take account of eight notes

    with open(original_csv, 'rb') as original_csv_file, open(output_csv, 'rb') as output_csv_file:
        original_reader = csv.reader(original_csv_file)
        output_reader = csv.reader(output_csv_file)

        # get frequencies
        frequency_list = original_reader.next()
        output_reader.next()  # same fields in output_csv
        column_count += len(frequency_list)

        # get time intervals
        # interval_list = [float(interval) for interval in original_reader.next()]

        # set max/min list
        # max_list = [0] * len(frequency_list)
        # min_list = [1000000] * len(frequency_list)

        for original_row, output_row in zip(original_reader, output_reader):
            row_count += 1
            for original_cell, output_cell in zip(original_row, output_row):
                # for now, skip empty output cells
                if output_cell < empty_threshold:
                    continue
                if abs(float(original_cell) - float(output_cell) / float(original_cell)) > difference:
                    cell_difference += 1
    return float(cell_difference) / float(row_count*column_count)


def main():
    print("Using our solver to compare: ")
    print(using_constraint_solver("Twinkle_Twinkle_Little_Star.csv", "Twinkle_Twinkle_Little_Star_MC.csv"))


if __name__ == '__main__':
    main()