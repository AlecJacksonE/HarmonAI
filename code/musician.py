# ------------------------------------------------------------------------------------------------
# Musician class defines functions to assist the Agent(s) of the simulation
# in identifying and hitting noteblocks.
# ------------------------------------------------------------------------------------------------
import math
import time
from timeit import default_timer as timer

class Musician():

	def __init__(self, note_positions):
		self.note_positions	= note_positions
	#Teleports the agent to location (x, 227, z) on a good_frame.
	def teleport(self, agent_host, x, z):
		#Construct and execute the teleport command.
		tp_command = "tp " + str(x + 0.5) + " 227 " + str(z-1)
		agent_host.sendCommand(tp_command)

		#Ensures that we leave on a good frame.
		good_frame = False 
		start = timer()
		while not good_frame:
			world_state = agent_host.getWorldState()
			if not world_state.is_mission_running:
			    print("Mission ended prematurely - error.")
			    exit(1)
			if not good_frame and world_state.number_of_video_frames_since_last_state > 0:
			    frame_x = world_state.video_frames[-1].xPos
			    frame_z = world_state.video_frames[-1].zPos
			    if math.fabs(frame_x - (x + 0.5)) < 0.001 and math.fabs(frame_z - (z-1)) < 0.001:
			        good_frame = True
			        end_frame = timer()

	def get_note_locations(self,agent_host, note_id):
		return self.note_positions[note_id]

	#Plays the noteblock specified by note_id.
	def play_noteblock(self, agent_host, note_id):
		#Obtain x,z coordinates of noteblock location based on note_id.
		note_location_x, note_location_z = self.get_note_locations(agent_host, note_id)

		#Perform teleport in front of stated noteblock.
		self.teleport(agent_host, note_location_x, note_location_z)
		time.sleep(0.1)

		#Perform the hit. time.sleep() used to ensure expected behavior.
		agent_host.sendCommand("attack 1")
		time.sleep(0.001)
		agent_host.sendCommand("attack 0")
		time.sleep(1)