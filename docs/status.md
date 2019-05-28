# Status

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/xW8mXuhalDM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project Summary:
For our project, we created an orchestra of AI agents that are capable of listening to music and recreate a song in Minecraft by scheduling each other to hit the appropriate Minecraft noteblocks on time in an optimal manner. Our inputs is an audio file (such as .wav or .mp3). The outputs will be the sounds from the noteblocks the AI touches and also a log that tells what the AI hit with the timestamp.

## Approach:
To start, we input an audio file with a simple rhythmic pattern to AnthemScore. AnthemScore then transcribes it to a CSV file. The music_translator.py file uses the CSV file along with given information (such as tempo, offset, and amplitude threshold) and runs through each time frame that falls within the tempo. The function uses hill-climbing search and collects frequencies that have peak amplitudes. After finding the peak amplitudes, the function puts them in a tuple of frequency and its peak amplitude at the time. Once the list of frequencies are collected, each index is sorted by biggest amplitude. Afterwards, the function goes through a dictionary that converts frequencies into integers that correlate to the noteblocks and finally the function outputs a list of timestamps with each timestamp having a sorted list of noteblock integers with its corresponding amplitude.

The new frequency list allows us to treat this problem in a discrete time domain and sets up this optimization scheduling problem as a constraint satisfaction problem. The constraint_solver.py file uses this new frequency list, as well as the total number of agents, to pre-process the list and copy it as an appropriate matrix $N$ for variables (where $N[t][i]$ is the note played at time $t$ by agent $i$ given that both $i,t$ are indexes starting at $0$). In this list, notes are only given in the range from 0 to 24 and the number -1 is given to represent an agent not playing any music that second. Next, each variable’s domain is given by the possible note choices for its specific time, so for each variable in $N[0]$, their domain is given by the possible choices from time $t = 0$ in the frequency list. Lastly, we are trying to optimize the scheduling decisions between agents, therefore we try to minimize the distance between notes for each agent as they play the song. From this work we obtain a list of notes for each agent to play at each time interval. The note of course is the number within the range of 0 to 24 and using this number our agents perform a search on the position of the note in the world and use that to teleport our agent in front of the noteblock. Afterwards the agents will then hit the noteblock and in this process perform the song to be played.


## Evaluation: 
Currently, we are only comparing the audio file and the Minecraft AI qualitatively, meaning we are basing it off of our knowledge of popular music and comparing our results to our perception of the song. After being more confident on the AI’s performance, we will record the song and put it into an audio file where we will then run it through AnthemScore and compare the frequency and amplitude values of the Minecraft AI’s audio and the original audio.


## Remaining Goals and Challenges:
Right now, the AI only knows the BPM of the song, so it checks every quarter note (e.g. with 120 BPM, the AI will check every .5 seconds and play a note if it finds a frequency with a large enough amplitude.) However, it has no way of checking different-sized notes (such as longer half notes or shorter eighth notes). We will try to let the AI determine the length of the note and then play the note as what the AI perceives it to be. 




## Resources Used: 
We used AnthemScore, a neural network, to transcribe audio files such as .wav and .mp3.






