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
		self.curr_x = 0
		self.curr_z = 0
		self.in_position = False
		self.can_play = False

	#Teleports the agent to location (x, 227, z) on a good_frame.
	def teleport(self, agent_host, x, z):
		#Save position.
		self.curr_x=x
		self.curr_z=z

		#Construct and execute the teleport command.
		tp_command = "tp " + str(x+0.5)+ " 227 " + str(z-0.5)
		agent_host.sendCommand(tp_command)

	def get_note_locations(self,agent_host, note_id):
		return self.note_positions[note_id]

	#Plays the noteblock specified by note_id.
	def teleport_to_noteblock(self, agent_host, note_id):

		if note_id == -1:
			return None

		#Obtain x,z coordinates of noteblock location based on note_id.
		note_location_x, note_location_z = self.get_note_locations(agent_host, note_id)

		if self.curr_x != note_location_x or self.curr_z != note_location_z:
			#Perform teleport in front of stated noteblock.
			self.teleport(agent_host, note_location_x, note_location_z)

		#Set so we know to play a note.
		self.can_play = True
		time.sleep(0.1)