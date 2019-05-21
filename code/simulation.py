# ------------------------------------------------------------------------------------------------
# simulation.py runs the simulation for the project.
# Generates a flat Minecraft world with all of the 25 noteblocks.
# As of right now it runs a minor simulation of the Agent hitting all 25 noteblocks.
# ------------------------------------------------------------------------------------------------

import MalmoPython
import sys
import json
from musician import *

#Data structure to store the positions of each block.
note_positions = {}

#All the different notes.
pitches = [
        "F_sharp_3",
        "G3",
        "G_sharp_3",
        "A3",
        "A_sharp_3",
        "B3",
        "C4",
        "C_sharp_4",
        "D4",
        "D_sharp_4",
        "E4",
        "F4",
        "F_sharp_4",
        "G4",
        "G_sharp_4",
        "A4",
        "A_sharp_4",
        "B4",
        "C5",
        "C_sharp_5",
        "D5",
        "D_sharp_5",
        "E5",
        "F5",
        "F_sharp_5"]

#Builds the positions of each note.
def buildNotePositions(pitches):
	positions = []
	starting_x = 24
	z = 6

	#Position of noteblocks is in a straight line in front of the Agent starting positon.
	for i in range(len(pitches)):
		positions.append((starting_x,z))
		starting_x -= 2

	#Save these positions.
	saveNotePositions(positions)
	return positions

#Saves the positions of each noteblock in data structure note_positions.
def saveNotePositions(positions):
    for i in range(len(pitches)):
        note_positions[i] = positions[i]


#Constructs the xml string for generating each noteblock.
def getNoteBlockDrawing(positions):
	drawing = ""
	index = 0
	for p in positions:
		drawing += '<DrawBlock x="' + str(p[0]) + '" y="227" z="' + str(p[1]) + '" type="noteblock" variant="' + pitches[index] +  '"/>'
		index += 1

	return drawing

#Returns xml string for generating the minecraft world.
def getMissionXML():

	positions = buildNotePositions(pitches)

	return '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary> summary </Summary>
        </About>

        <ModSettings>
            <MsPerTick>100</MsPerTick>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />
                <DrawingDecorator>
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="monster_egg" variant="chiseled_brick" />
                    ''' + getNoteBlockDrawing(positions) + '''
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Agent1</Name>
            <AgentStart>
                <Placement x="0.5" y="227.0" z="0.5" yaw="0" pitch="50"/>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <AbsoluteMovementCommands/>
                <SimpleCraftCommands/>
                <MissionQuitCommands/>
                <InventoryCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullInventory/>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

#runs the simulation.
def run(agent_host, musician):
	for note_id in range(len(pitches)):
		musician.play_noteblock(agent_host, note_id)

def main():
    print('Starting...', flush=True)

    my_client_pool = MalmoPython.ClientPool()
    my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))

    agent_host = MalmoPython.AgentHost()

    try:
    	agent_host.parse( sys.argv )
    except RuntimeError as e:
    	print('ERROR:', e)
    	print(agent_host.getUsage())
    	exit(1)
    if agent_host.receivedArgument("help"):
    	print(agent_host.getUsage())
    	exit(0)

    musician = Musician(note_positions)

    my_mission = MalmoPython.MissionSpec(getMissionXML(), True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    my_mission.requestVideo(800, 500)
    my_mission.setViewpoint(0)

    # Attempt to start a mission:
    max_retries = 3
    for retry in range(max_retries):
    	try:
    		agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "Agent1")
    		break
    	except RuntimeError as e:
    		if retry == max_retries - 1:
    			print("Error starting mission:",e)
    			exit(1)
    		else:
    			time.sleep(2)

    world_state = agent_host.getWorldState()	
    while not world_state.has_mission_begun:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        time.sleep(1)

    #Simulation starts here.
    run(agent_host, musician)

if __name__ == '__main__':
	main()	