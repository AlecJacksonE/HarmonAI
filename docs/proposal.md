---
layout: default
title: Proposal
---

## Summary of our project
For our project, we will create an AI that creates music by giving the AI something to listen to recreate the notes on time to the beat. Our inputs would be a file that has music (most likely music with only one note at a time with no chords). The outputs will be the sounds from the noteblocks the AI touches and also a log that tells what the AI hit with the timestamp. We will use the Minecraft note blocks for the AI to interact with. I believe we will also have to find a program to allow the AI to “hear” the music.

## AI/ML Algorithms
We will use reinforcement learning with neural networks and maybe some Q learning.

## Evaluation Plans
We allow the AI to move around and hit the note blocks that surround the AI. We want to make sure the AI can move and reach the note block in time, so we let the AI do Q-learning to allow it to find the best path to the next note. The AI will receive rewards based on if the AI chooses the right pitch and if the AI presses the note block on time. The rewards shrink if they play a wrong note on time or played the right note slightly off rhythm. We will give the AI negative rewards either after every time it uses the interact button or by how many times it interacted beyond the total count of notes in the given music piece. 

We will score it using the export log of actions to see if the AI is pressing the correct note blocks on time. The better the AI scores, the better the AI closely follows the music given to it. Our sanity cases will be testing the AI with many simple pieces with different tempos, notes, and rhythms and listening to the results over time. At the end, our goal is to give the AI different pieces of music and it will playback the music on time with the correct notes. Our push goal is to have multiple AIs to play harmony and melody together and on time.

## Appointment Time
Our group time is Apr. 26 at 10:45pm
