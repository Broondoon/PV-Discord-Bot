# command_list.py
# Holds the response functionalities for the bot commands

# USER FLOW:
#  - characters (players + monsters) are hard-coded
#  - bot is connected
#  - teams are built from groups of characters
#  - battles are built from teams
#  - battle are started
#  - battle ends
#  - next battle is started
#  - repeat until no more battles
#  - bot is disconected

import database as db
import combat_calc

battles = [] # list of current available battles
teams = [] # list of current active teams

# Simple definition for a Team object
class Team:
	num = -1
	members = [] # [name, nums, basics, el_reacts, creature]
	def __init__(self, num, chars):
		self.num = num
		#self.members = chars

		# When creating a team, extract the relevant info from the database.
		for name in chars:

			print("Building team... Name is:", name)

			# Query the database to get the various stats.
			nums = db.getCharStats(name, "nums") #hp, sp
			basics = db.getCharStats(name, "basics") #str, int, end, mob
			el_reacts = db.getCharStats(name, "elements") #react_phys, react_fire, react_water, react_nature, react_machine, react_earth, react_wind, react_ice, react_fossil
			creature = db.getCharStats(name, "creaturetype") #type

			# Add this character to the team!
			self.members.append([name, nums, basics, el_reacts, creature])

# Simple definition for a Battle object
class Battle:
	num = -1
	name = "Default"
	size = 0
	team1 = Team(-1, [])
	team2 = Team(-1, [])
	def __init__(self, num, name, team1, team2):
		self.num = num
		self.name = name
		self.team1 = team1
		self.team2 = team2
		self.size = len(team1.members) + len(team2.members)

in_progress = 0

###### Helper Functions:

'''
def readTeam(team):
	result = "Team " + str(team.num) + ":\n"
	for char in team.members:
		result += " - " + char + "\n"
		result += "\n"
	return result
'''

# Quick function to find a battle in the battle list given an id number
# If this is broken, double check you're passsing an integer for b_num!
def getBattle(b_num):
	for battle in battles:
		if battle.num == b_num:
			return battle
	return None


# Function to format an output that the players will see, not just the user. Goes into the OUTPUT_CHANNEL.
# More of a function for bot.py rather than a command helper, but I didn't want to congest bot.py more
def battle():
	fields = []

	return fields

###### Commands:

def help():
	pass

# character list (shows every hard-coded character)
# return a 'field' = [title, contents, inline_bool]
def charList():
	fields = []
	char_list = db.getAllCharacters()
	for char in char_list:
		# Each char looks like this: (4, 'COMPASS', 'protag')
		title = "Character " + str(char[0]) + ": \"" + char[1] + "\""
		contents = "They are a __" + char[2] + "__"
		inline_bool = False

		fields.append([title, contents, inline_bool])
		
	return fields

# character details (shows every hard-coded character)
# return a 'field' = [title, contents, inline_bool]
def charDetails(char_name):
	fields = []
	details = db.getCharFull(char_name)

	if details is not None:
		#fields.append(['\u200b', '\u200b', False])

		fields.append(["ID:", details[0], True])
		fields.append(["Character Name:", details[1], True])
		fields.append(["Type:", details[2], True])

		fields.append(['\u200b', '\u200b', False])

		fields.append(["HP:", details[3], True])
		fields.append(["SP:", details[4], True])
		fields.append(["Strength:", details[5], True])
		fields.append(["Intelligence:", details[6], True])
		fields.append(["Endurance:", details[7], True])
		fields.append(["Mobility:", details[8], True])

		fields.append(['\u200b', '\u200b', False])

		fields.append(["Physical Reaction:", details[9], True])
		fields.append(["Fire Reaction:", details[10], True])
		fields.append(["Water Reaction:", details[11], True])
		fields.append(["Nature Reaction:", details[12], True])
		fields.append(["Machine Reaction:", details[13], True])
		fields.append(["Earth Reaction:", details[14], True])
		fields.append(["Wind Reaction:", details[15], True])
		fields.append(["Ice Reaction:", details[16], True])
		fields.append(["Fossil Reaction:", details[17], True])

		return fields
	else:
		return None

def charNoInput():
	response = """\> Options:
	__+character list__
			- Provides a list of every character in the database
	__+character details <character name>__
			- Provides the details of a specified character"""

	return response

# battle ready teams (lists teams built in a numbered list)
# TODO improvement: make team number a field title, and field contents be team members (for readability)
def battleReadyTeams():
	response = ""

	if len(teams) == 0:
		response = "There are no active teams built this session."
	else:
		for team in teams:
			response += "Team " + str(team.num) + ":\n"
			#print("Team members in team", team.num, ": ", team.members)
			for char in team.members:
				response += " - " + char[0] + "\n"
			response += "\n"

	return response

# battle ready (lists battles built in a numbered list)
# TODO improvement: make battle name a field title, and field contents be team members (for readability)
def battleReady():
	response = ""

	if len(battles) == 0:
		response = "There are no ready battles built this session."
	else:
		for battle in battles:
			response += "__Battle \"" + battle.name + "\" (" + str(battle.num) + ")__\n"
			response += " - Team " + str(battle.team1.num) + "\n" 
			response += "   VERSUS\n"
			response += " - Team " + str(battle.team2.num) + "\n"
			response += "\n"

	return response

#  battle build (args = name of battle, two teams) (adds a built battle to the list)
def battleBuild(args):
	
	# Catch if the user hasn't built enough teams yet
	if len(teams) <= 1:
		return "Not enough teams to create a battle (must have at least 2)."
	
	# Grab the two team numbers (which are strings)
	team1 = args[2]
	team2 = args[3]

	# Attempt to convert the arguments into numbers, and handle the event where that fails
	try:
		team1_num = int(team1)
		team2_num = int(team2)
	except ValueError:
		return "Teams must be specified by number. Please try \"+battle ready teams\" if you are unsure. " + team1 + " " + team2

	# Catch if the user inputs the same team twice 
	if team1_num == team2_num:
		return "A team cannot fight itself."

	# Find the Team objects which match the team numbers provided
	team_to_add_1 = None
	team_to_add_2 = None
	for team in teams:
		if team1_num == team.num:
			team_to_add_1 = team
		elif team2_num == team.num:
			team_to_add_2 = team

	# Catch if the user asked for a team that hasn't been built yet
	if team_to_add_1 == None or team_to_add_2 == None:
		return "Could not find both teams."

	# If everything has been done properly, add the completed Battle object to the list
	new_battle = Battle(len(battles), args[1], team_to_add_1, team_to_add_2)
	battles.append(new_battle)

	return "Battle \"" + args[1] + "\" created."
	
# "battle build team" - Given 1-4 combattents, create a Team object containing those characters if they exist within the database
def battleBuildTeam(args):
	response = ""
	chars = args[2:] # slice list to ignore 'build' and 'team' arguments
	cannot_complete = False # flag for if one or more characters don't exist

	print("Chars:", chars)

	# For every provided character, verify if they are present in the database
	try:
		for char in chars:
			if (db.verifyExists(char) == False):
				response += "Character " + char + " does NOT exist.\n"
				cannot_complete = True
	# If for whatever reason the SQL died, need to send that back.
	except RuntimeError as error:
		for arg in error.args:
			response += arg
		return response
	# If something wasn't in the db, do not create a team
	if cannot_complete:
		return response
	# Otherwise, build the team from what we've been given
	else:
		new_team = Team(len(teams), chars)			
		teams.append(new_team)
		return "Team " + str(new_team.num) + " created."

#  battle start (args = num or name in list)
def battleStart(battle_identifier, OUT_CHANNEL):
	fields = []
	# First attempt to verify that the user passed in a numeric value, intercepting the error if they didn't.
	try:
		battle_id = int(battle_identifier)
	except ValueError:
		fields.append(["Invalid battle specified.", "Please use a battle's associated numeric id. Check \"+battle ready\" for your options.", False])
	else:
		# Find the battle the user is looking for, if we can.
		the_battle = getBattle(battle_id)

		# If we couldn't find the battle, we need to inform the user and do nothing after that.
		if the_battle == None:
			fields.append(["Cannot find battle.", "Please double check created battles with \"+battle ready\".", False])
		else:
			fields.append(["START"]) # not a field, but a signal
			fields.append(["Starting battle \"" + the_battle.name + "\" now!", "Team " + str(the_battle.team1.num) + " VS Team " + str(the_battle.team2.num), False])
			fields.append(["Output channel is:", "" + OUT_CHANNEL, False])

	return fields

def battleNoArgs():
	response = """BATTLE COMMANDS
	> Options:
	__+battle ready__
			- Provides in a numbered list every prepared battle this session
	__+battle ready teams__
			- Provides in a numbered list every prepared team this session
	__+battle build <"battle_name">, <team1>, <team2>__
			- Builds a battle for deployment
			- Built battle is added to the list of battles
			- Ensure that the battle_name is enclosed in brackets!
	__+battle build team <fighter1>, <fighter2>, <etc>__
			- Groups together 1-4 characters into a team
			- Identifies if SHOWTIME ATTACKS are possible
	__+battle start <list_num>__
			- Begins combat for the specified battle
			- The number is the one in the "battle ready" list
			- Outputs a control menu"""

	return response