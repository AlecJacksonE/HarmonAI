'''
read csv file
go through list
if a note peaks, it's probably the note
Maybe we make it a hivemind AI, the highest peak gets AI 1, then
next peak is AI 2, and etc.
Need to find a way to make 2 notes that are half-steps (next to each other)
recognizable to the AI or else it thinks it's just a weird note.

As a guide (according to AnthemScore): (An octave higher is basically x2 the frequency)
F#3 = 184.997Hz     F#4 = 369.994Hz       F#5 = 739.988Hz
G3 = 195.998Hz      G4 = 391.995Hz
G#3 = 207.652Hz     G#4 = 415.304Hz
A3 = 220Hz          A4 = 439.999Hz
A#3 = 233.082Hz     A#3 = 466.163Hz
B3 = 246.941Hz      B4 = 493.883Hz
C4 = 261.625Hz      C5 = 523.25Hz
C#4 = 277.182Hz     C#5 = 554.365Hz
D4 = 293.664Hz      D5 = 587.329Hz
D#4 = 311.127Hz     D#5 = 622.253Hz
E4 = 329.627Hz      E5 = 659.254Hz
F4 = 349.228Hz      F5 = 698.455Hz
'''
import csv

def create_note_list(file_name,tempo,threshold=10000,offset = 0.00):
    #Later, this will be tuples of frequencies with their amplitudes (loudness).
    #For now, tempo is actual BPM/4 since we'll deal with quarter notes (for now)
    #the offset is for just in case the song doesn't start at 0 sec
    note_list = []
    interval_list = []
    frequency_list = [] #the list of frequencies checked
    csv_file = open(file_name,'r')
    time_list = []

    reader = csv.reader(csv_file)

    descent = False #we don't want to accidentally grab all frequencies on decending

    for line, time in enumerate(reader):
        prev_amplitude = 0
        if(line == 0): #the list of all frequencies checked (also includes non-notes)
            for freq in time:
                frequency_list.append(float(freq))

        elif(line == 1): #the list of all timestamps (using AnthemScore, it's .01s intervals)
            for interval in time:
                interval_list.append(float(interval))
            beats = round(1/(tempo/60.0),2)
            
            #we may need above to calculate tempo
            #print(interval_list)
            
        elif(line > 2):
            #print(interval_list[line-2]+offset)
            #will change below later so tempos that don't divide evenly can also work
            if((interval_list[line-3]+offset) % beats == 0): #-2 because the csv has 2 offset
                #print(interval_list[line-3]+offset)
                for num, freq in enumerate(time):
                    freq = float(freq)
                    
                    if(freq > prev_amplitude): #the next freq has higher amplitude
                        descent = True
                        
                        
                    elif(freq <= prev_amplitude and descent):
                        descent = False
                        if(prev_amplitude > threshold):
                            time_list.append((frequency_list[num-1],prev_amplitude))

                    prev_amplitude = freq

                #print(time_list)
                time_list.sort(key=lambda tup: tup[1]) # sort by biggest amplitude in interval
                note_list.append(time_list)
                time_list = []

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
freq_list = create_note_list("Twinkle Twinkle Little Star.csv",120,5000,-.07)
print(number_converter(freq_list))
