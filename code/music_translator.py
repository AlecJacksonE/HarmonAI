'''
read csv file
go through list
if a note peaks, it's probably the note
Maybe we make it a hivemind AI, the highest peak gets AI 1, then
next peak is AI 2, and etc.
Need to find a way to make 2 notes that are half-steps (next to each other)
recognizable to the AI or else it thinks it's just a weird note.

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
import csv


def create_note_list(file_name,tempo,threshold=10000,offset = 0.00,leniency = .03):
    #Later, this will be tuples of frequencies with their amplitudes (loudness).
    #For now, tempo is actual BPM/4 since we'll deal with quarter notes (for now)
    #the offset is for just in case the song doesn't start at 0 sec
    #songs aren't always perfectly timed, so we use leniency to check the frequencies
    #around the beat (in frames rather than time)
    note_list = []
    interval_list = []
    frequency_list = [] #the list of frequencies checked
    csv_file = open(file_name,'r')
    time_list = []

    reader = csv.reader(csv_file)
    max_list = []
    within_bounds = False
    descent = False #we don't want to accidentally grab all frequencies on descending

    
    '''
    leniency_list = [0]
    for num in range(leniency):
        leniency_list.append(leniency+1)
        leniency_list.append(-leniency-1)
    '''
    
    for line, time in enumerate(reader):
        prev_amplitude = 0
        if(line == 0): #the list of all frequencies checked (also includes non-notes)
            for freq in time:
                frequency_list.append(float(freq))

        elif(line == 1): #the list of all timestamps (using AnthemScore, it's .01s intervals)
            for interval in time:
                interval_list.append(float(interval))
            beats = round(1/(tempo/60.0),2)
            
            #print(interval_list)
            
        elif(line > 2):
            #print(line)
            #print((interval_list[line-2]+offset) % beats, (interval_list[line-2]+offset), (beats-leniency))
            if((interval_list[line-2]+offset) == 0.0 or (interval_list[line-2]+offset) % beats <= leniency or (interval_list[line-2]+offset) % beats >= (beats-leniency)): #-2 because the csv has 2 offset
                '''
                if((interval_list[line-2]+offset) != 0):
                    print((interval_list[line-2]+offset) ,beats)
                    print((interval_list[line-2]+offset))
                    print((interval_list[line-2]+offset) % beats)
                    print(beats % (interval_list[line-2]+offset))
                    print()
                '''
                #print((interval_list[line-2]+offset))
                within_bounds = True
                max_list = [0]*len(time)
                #grab the max frequency
                for index, amp in enumerate(time):
                    #print(max_list)
                    if(float(amp) > max_list[index]):
                        max_list[index] = amp
                    
                #print(max_list)
                        
            elif(within_bounds):
                within_bounds = False
                for num, freq in enumerate(max_list):
                    freq = float(freq)
                    
                    if(freq > prev_amplitude): #the next freq has higher amplitude
                        descent = True
                        
                        
                    elif(freq <= prev_amplitude and descent):
                        descent = False
                        if(prev_amplitude > threshold):
                            time_list.append((frequency_list[num-1],prev_amplitude))

                    prev_amplitude = freq

                sorted(time_list, key=lambda x: x[1])# sort by biggest amplitude in interval
                #print(time_list)
                note_list.append(time_list)
                time_list = []
                max_list = [0]*len(time_list)

        #if(line == 3):   #checking first line only
        #    break
    csv_file.close

    #print(note_list)
    return note_list

def number_converter(list_of_freq):
    #this takes in the frequencies and then converts them into tuples of ints
    #list of freq is a list of list of tuples
    note_convert = {184.997:0,195.998:1,207.652:2,220:3,233.082:4,246.941:5,
                    261.625:6,277.182:7,293.664:8,311.127:9,329.627:10,
                    349.228:11,369.994:12,391.995:13,415.304:14,439.999:15,
                    466.163:16,493.883:17,523.25:18,554.365:19,587.329:20,
                    622.253:21,659.254:22,698.455:23,739.988:24}
    
    new_list = []
    inside_list = []
    for interval in list_of_freq:
        for freq in interval:
            if(freq[0] in note_convert):
                inside_list.append((note_convert[freq[0]],freq[1]))
        new_list.append(inside_list)
        inside_list = []

    return new_list

#Test
#freq_list = create_note_list("440Hz.csv",120)
freq_list = create_note_list("Twinkle Twinkle Little Star.csv",120,7000,-.08)
#print(len(freq_list))
print(number_converter(freq_list))

#TODO
'''
Give a small margin of error for timing (humans & machines don't play that perfect)

If it is on the beat, check the surrounding times
Make a list of max values per freq

                for num, freq in enumerate(time):
                    freq = float(freq)
                    
                    if(freq > prev_amplitude): #the next freq has higher amplitude
                        descent = True
                        
                        
                    elif(freq <= prev_amplitude and descent):
                        descent = False
                        if(prev_amplitude > threshold):
                            time_list.append((frequency_list[num-1],prev_amplitude))

                    prev_amplitude = freq
'''
