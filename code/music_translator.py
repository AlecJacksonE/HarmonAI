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
    #For now, tempo is actual BPM/8 since we'll deal with eighth notes (for now)
    #the offset is for just in case the song doesn't start at 0 sec
    #songs aren't always perfectly timed, so we use leniency to check the frequencies
    #around the beat (in time)
    note_list = []
    interval_list = []
    frequency_list = [] #the list of frequencies checked
    csv_file = open(file_name,'r')
    time_list = []

    reader = csv.reader(csv_file)
    max_list = []
    min_list = []
    within_bounds = False
    descent = False #we don't want to accidentally grab all frequencies on descending
    add_frequency = True # to help with finding 8th notes
    
    for line, time in enumerate(reader):
        prev_amplitude = 0
        if(line == 0): #the list of all frequencies checked (also includes non-notes)
            for freq in time:
                frequency_list.append(float(freq))
        
        elif(line == 1): #the list of all timestamps (using AnthemScore, it's .01s intervals)
            for interval in time:
                interval_list.append(float(interval))
            beats = round(1/(tempo/30.0),2) #changed 60 to 30 to take account of eight notes

            #put over here rather than the next elif to not erase
            max_list = [0]*len(frequency_list)
            min_list = [1000000]*len(frequency_list)
            
        elif(line > 2):
            #print(line)
            #print(interval_list[line-3])
            #print((interval_list[line-2]+offset) % beats,
            #(interval_list[line-2]+offset), (beats-leniency))

            if((interval_list[line-3]+offset) == 0.0 or
               (interval_list[line-3]+offset) % beats <= leniency or
               (interval_list[line-3]+offset) % beats >= (beats-leniency)): #-2 because the csv has 2 offset
                #print("made it")
                
                #print((interval_list[line-3]+offset))
                #print()
                within_bounds = True

                #grab the max and min frequencies
                for index, amp in enumerate(time):
                    #print(max_list)
                    if(float(amp) > max_list[index]):
                        max_list[index] = float(amp)
                    if(float(amp) < min_list[index]):
                        min_list[index] = float(amp)
                    
                #print(max_list)
                        
            elif(within_bounds):
                within_bounds = False
                for num, freq in enumerate(max_list):
                    #print(frequency_list[num],freq)
                    freq = float(freq)
                    #print(prev_amplitude)
                    if(freq > prev_amplitude): #the next freq has higher amplitude
                        descent = True
                         
                    elif(freq <= prev_amplitude and descent):
                        #print("HI")
                        descent = False
                        if(prev_amplitude > threshold):
                            #print(frequency_list[num-1],min_list[num],max_list[num])
                            #print(float(min_list[num])/float(max_list[num]))
                            #if(float(min_list[num])/float(max_list[num]) > .70 ):
                                #if the frequency exists in the previous time and it's louder than the threshold
                            if(len(note_list) > 0 and len(note_list[-1]) > 0):
                                    for f in note_list[-1]:
                                        if(f[0] == frequency_list[num-1] and prev_amplitude/f[1] < .75
                                           and prev_amplitude/f[1] > 1.25):
                                            add_frequency = False
                            if(add_frequency):
                                time_list.append((frequency_list[num-1],prev_amplitude))

                    prev_amplitude = freq
                    add_frequency = True

                sorted(time_list, key=lambda x: x[1])# sort by biggest amplitude in interval
                #print(time_list)
                note_list.append(time_list)
                time_list = []

                #refresh for the next run
                max_list = [0]*len(frequency_list)
                min_list = [1000000]*len(frequency_list)

        #if(line == 12):   #checking first line only
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
#freq_list = create_note_list("Twinkle Twinkle Little Star.csv",120,8000,-0.08)
#freq_list = create_note_list("Chopsticks.csv",120,4000,-.15,.03)
#freq_list = create_note_list("Baa_Baa_Black_Sheep_(120BPM).csv",120,4000,-.08,.03)
freq_list = create_note_list("Bad_Apple.csv",120,3000,-.08,.03)
#print(len(freq_list))
#print(number_converter(freq_list))
#a = number_converter(freq_list)
#for thing in a:
#    print(thing)

#TODO
'''
Find a way to distinguish a long note with a short note

Maybe compare up to 8th notes (for now at least) and compare the min and max
Could be a % or a threshold again
Whole notes probably won't do anything because you can't hold noteboxes

Maybe make threshold a percentage so distinguish min and max
-.08
'''
