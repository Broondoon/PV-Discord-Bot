# combat_calc.py
# Handles combat calculations by providing functions which typically return the result of an action.


#class Battlefield:
#	def __init__(self):
		
############### Internal Commands #################

# Function to return a list of characters with the same MOB stat.
# Also take into consideration any protag's versus regular enemies.
def sameMOB(battle, first_char):
	
	target_MOB = first_char[2][3]
	same_list = []

	# Now find any other protagonists with the same speed stat.
	# Quick loop over both teams to avoid code duplication.
	for team in (battle.team1, battle.team2):
		# For every character...
		for member in team.members:	
			# If they have the same MOB stat:
			if member[2][3] == target_MOB:
				# Append to the list.
				same_list.append(member)

	# Return what should be the list of every character with the same MOB stat, INCLUDING the original character.
	return same_list

# Function to establish a baseline fastest character. Should only be called once per Battle.
def whosFirst(battle):
	
	# Default fastest is team1's first member
	fastest_member = battle.team1.members[0]

	# Iterate over every team member to find the highest MOB stat.
	# (Quick loop over both teams to avoid code duplication.)
	for team in (battle.team1, battle.team2):
		# For every character...
		for member in team.members:
			# REMINDER - The contents of members: [name, nums, basics [str, int, end, mob], el_reacts, creature]
			# Check if they're faster than the fastest character.
			if member[2][3] > fastest_member[2][3]:
				# If the current member's MOB stat is higher, they become the fastest.
				fastest_member = member
			elif member[2][3] == fastest_member[2][3] and "protag" in member[4][0]:
				# If the current member has equal MOB, protags take precedence.
				fastest_member = member

	# Return what should now be the fastest member of a battle, and the characters with the same MOB.
	return sameMOB(battle, fastest_member)

	
	

# Determines who should act next, given the mobility of the current character
def whosNext(curr_MOB):
	pass

# Determine what skills a player / monster can choose from this  turn
# Returns a list of tuples, (Ability name, effect)
def discernAbilities():
	pass

# Setter for whenever a Swing would apply an effect like Broken, Boosted, Charged, etc
def applyEffects():
	pass



############### Combat Moves #################


# Return damage dealt and any reactions, depending on params given
# Returns [dmg dealt, defender_effects]
def swing(dice, char_stat_mod):
	pass

def showtime():
	pass

def allout():
	pass

# Returns True if dice roll based off of the mobility stat provided succeeds
def dodge(mob):	
	pass