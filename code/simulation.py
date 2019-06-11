# ------------------------------------------------------------------------------------------------
# simulation.py runs the simulation for the project.
# Generates a flat Minecraft world with all of the 25 noteblocks.
# As of right now it runs a minor simulation of the Agent hitting all 25 noteblocks.
# ------------------------------------------------------------------------------------------------

import MalmoPython
import malmoutils
import sys
import json
import constraint_solver as cs
import music_translator as mt
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
		starting_x -= 3

	#Save these positions.
	saveNotePositions(positions)
	return positions

#Saves the positions of each noteblock in data structure note_positions.
def saveNotePositions(positions):
    for i in range(len(pitches)):
        note_positions[i] = positions[i]


def generateAgentTeleportPositions(positions,agent_id):
    shift = [(0,0),(1,1),(0,2),(-1,1)]
    tele_pos = {}

    for i in range(len(positions)):
        pos = (positions[i][0]+shift[agent_id][0], positions[i][1]+shift[agent_id][1])
        tele_pos[i]=pos

    return tele_pos

#Constructs the xml string for generating each noteblock.
def getNoteBlockDrawing(positions):
    drawing = ""
    index = 0
    for p in positions:
        drawing += '<DrawBlock x="' + str(p[0]) + '" y="227" z="' + str(p[1]) + '" type="noteblock" variant="' + pitches[index] +  '"/>'
        index += 1

    return drawing

def generateAgentSection(num_agents):
    cardinal_direction = [0, 90, 180, -90]
    drawing = ""
    for i in range(num_agents):
        drawing += '''<AgentSection mode="Survival">
        <Name>Agent''' + str(i+1) + '''</Name>
        <AgentStart> 
            <Placement x="'''+str(0.5+i) + '''" y="227.0" z="0.5" yaw="''' + str(cardinal_direction[i]) + '''" pitch="50"/>
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
        </AgentHandlers>
        </AgentSection>\n\n'''

    return drawing

#Returns xml string for generating the minecraft world.
def getMissionXML(num_agents):

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
                    <StartTime>0</StartTime>
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
                <ServerQuitWhenAnyAgentFinishes/>
            </ServerHandlers>
        </ServerSection>
    ''' + generateAgentSection(num_agents) + '''

    </Mission>'''

def startMission(agent_host, mission, client_pool, recording, role, experimentId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            agent_host.startMission(mission, client_pool, recording, role, experimentId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)

    print("startMission called okay.")

def waitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow two minutes for mission to start.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')
    print()
    if time.time() - start_time >= time_out:
        print("Timed out waiting for mission to begin. Bailing.")
        exit(1)
    print("Mission has started.")

def main():

    #Hardcode number of agents to play song
    num_agents = 2

    #Obtain song csv and get solutions
    #freq_list = mt.create_note_list("Bad_Apple.csv",120,3000,-.08,.03)
    #freq_list = mt.create_note_list("Twinkle_Twinkle_Little_Star.csv",120,8000,-.08)
    freq_list = mt.create_note_list("Chopsticks.csv",120,4000,-.15,.03)
    freq_list = mt.number_converter(freq_list)
    solutions = cs.get_solutions(freq_list, num_agents)

    #Create musician for each agent and pass teleport positions.
    musicians=[]
    for i in range(num_agents):
        musicians.append(Musician(generateAgentTeleportPositions(note_positions, i)))

    #Hardcode Agent Names
    for i in range(num_agents):
        agent_names.append("Agent" + str(i+1))

    '''
    MALMO
    '''
    print('Starting...', flush=True)

    #Create agents.
    agent_hosts = []
    for i in range(num_agents):
        agent_hosts.append(MalmoPython.AgentHost())

    malmoutils.parse_command_line(agent_hosts[0])

    #Get mission and allow commands for teleport.
    my_mission = MalmoPython.MissionSpec(getMissionXML(num_agents), True)
    my_mission.allowAllChatCommands()

    #Add client for each agent needed.
    my_client_pool = MalmoPython.ClientPool()
    for i in range(num_agents):
        my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000+i))

    MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)

    #Start mission for each agent
    for i in range(num_agents):
        startMission(agent_hosts[i], my_mission, my_client_pool, malmoutils.get_default_recording_object(agent_hosts[0], "agent_" + str(i+1) + "_viewpoint_discrete"), i, '')

    #Wait for all missions to begin.
    waitForStart(agent_hosts)

    #Pause for simulation to begin.
    time.sleep(1)
    

    '''
    SIMULATION BEGINS HERE
    '''
    for i in range(len(solutions[0])):

        #teleport each agent to the corresponding note.
        for j in range(len(musicians)):
            musicians[j].teleport_to_noteblock(agent_hosts[0], solutions[j][i], agent_names[j])
        time.sleep(0.1)
        
        #play each note.
        for k in range(len(musicians)):
            if musicians[k].can_play:
                agent_hosts[k].sendCommand("attack 1")
                
                time.sleep(0.001)
                agent_hosts[k].sendCommand("attack 0")
                musicians[k].can_play = False

        #modifies the timing between each note hit.
        time.sleep(0.1)
        
if __name__ == '__main__':
	main()	