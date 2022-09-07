# database.py
# Handles the creation and management of the character table and database
# Created with the help of (https://towardsdatascience.com/do-you-know-python-has-a-built-in-database-d553989c87bd)

# + Strengthen, - Weaken, @ Resist, # Immune, * Absorb, ^ Reflect, / Break, 'n' None

#import re #regex string parsing for input whitelisting/sanitization
import sqlite3 as sl
con = sl.connect('character-stats.db')

DB_PRESENT = 0

# By executing the SQL query, return a list of tuples, and each tuple is the information for one character.
def getAllCharacters():
	chars = []
	with con:
		data = con.execute("SELECT id, name, type FROM Character")
		for row in data:
			chars.append(row)
	return chars

def verifyExists(char):
	# Alt approach? More pythonic? Yeah no this is just better.
	with con:
		# Query the names of every character in the table
		data = con.execute("SELECT name FROM Character")
		names_in_db = []

		# For every tuple (row), grab the name held within that tuple.
		for row in data:
			names_in_db.append(row[0])

		# Check if the provided char name is in our list of names.
		if char not in names_in_db:
			return False
		else:
			return True

	'''
	# Error handling:
	# Attempt to grab data from the database
	# If an exception is thrown, raise an exception command_list.py will recognize
	# Otherwise, the length of the result determines if character exists or not:
	#  - len = 0, result set was empty, so that character doesn't exist
	#  - len > 0, result set got something, so that character exists
	try:
		with con:
			data = con.execute("SELECT * FROM Character WHERE name = \'" + char + "\'") #obvious injection weakness
			#print(data.fetchall()[0][1]) #<-- grabs the name from db
			

	except sl.OperationalError:
		raise RuntimeError("Something broke with the SQL dealing with character " + char)
	else:
		if len(data.fetchall()) == 0:
			return False #"Character " + char + " does NOT exist.\n"
		else:
			return True
	'''

# Given a set of information, create a new character and add them to the table.
# stats[6] = {hp, sp, str, intel, end, mob}
# elem_reacts[9] = {react_phys, react_fire, react_water, react_nature, react_machine, react_earth, react_wind, react_ice, react_fossil}
def saveNewCharacter(name, type, stats, elem_reacts):
	pass

# Given a name, query the table for the associated character and return the results.
def getCharFull(name):
	if verifyExists(name):
		with con:
			result = None # Not pythonic?
			data = con.execute("SELECT * FROM Character WHERE name = \'" + name + "\'")
			for row in data:
				result = row
			return result #row
	else:
		return None

# Given a name, query the table for the associated character's SPECIFIC stats.
def getCharStats(name, desired):
	if verifyExists(name):
		with con:

			if desired == "nums":
				selection = "hp, sp"
			elif desired == "basics":
				selection = "str, intel, end, mob"
			elif desired == "elements":
				selection = "react_phys, react_fire, react_water, react_nature, react_machine, react_earth, react_wind, react_ice, react_fossil"
			elif desired == "creaturetype":
				selection = "type"

			data = con.execute("SELECT " + selection + " FROM Character WHERE name = '" + name + "'")
			
			# Some weird shenanigans happenening where data.fetchall()[0] would result in a list index out of range error...
			results = data.fetchall()
			
			# SQL queries return a list of tuples, even if there's only one tuple. So we access the 1-element long list here to get the only tuple.
			return results[0]
	else:
		return None

if (DB_PRESENT == 0):
	with con:
		
		#con.execute("DROP TABLE Character")
		
		# Create the table if it does not exist already!
		con.execute("""
			CREATE TABLE IF NOT EXISTS Character (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				type TEXT,
				elem TEXT,
				hp INTEGER,
				sp INTEGER,
				str INTEGER,
				intel INTEGER,
				end INTEGER,
				mob INTEGER,
				react_phys TEXT,
				react_fire TEXT,
				react_water TEXT,
				react_nature TEXT,
				react_machine TEXT,
				react_earth TEXT,
				react_wind TEXT,
				react_ice TEXT,
				react_fossil TEXT
			);
		""")

		con.execute("""
			CREATE TABLE IF NOT EXISTS SignificantBonds (
				id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
				char1 TEXT,
				char2 TEXT
			);
		""")

		'''
		print("BEFORE:")
		data = con.execute("SELECT * FROM Character")
		for row in data:
			print(row)
		print("\nAFTER:")
		'''

		# Create tuples and place them into the table, checking first if they already exist within the table.
		# + Strengthen, - Weaken, @ Resist, # Immune, * Absorb, ^ Reflect, / Break, 'n' None
		sql = 'INSERT INTO Character (id, name, type, elem, hp, sp, str, intel, end, mob, react_phys, react_fire, react_water, react_nature, react_machine, react_earth, react_wind, react_ice, react_fossil) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
		data_to_add = []
		data_might_add = [
			(1, 'CIPHER', 'player protag', 'nature', 60, 30, 0, 1, 0, 0, 'n', 'n', '+', '+@', '-', '-', 'n', 'n', 'n'),
			(2, 'SPYDER', 'protag', 'machine', 60, 30, 0, 1, 0, 0, 'n', '+', 'n', '-', '+@', 'n', '-', 'n', 'n'),
			(3, 'SCEPTOR', 'player protag', 'ice', 60, 30, 0, 0, 0, 1, 'n', '-', 'n', 'n', 'n', '+', 'n', '+@', '-'),
			(4, 'COMPASS', 'protag', 'fossil', 60, 30, 0, 0, 0, 1, 'n', 'n', '-', 'n', 'n', 'n', '+', '-', '+@'),
			(999, 'IMMOVABLE GONZALES', 'monster', 'physical', 99, 0, 10, 0, 10, 0, '#', '@', '@', '@', '@', '@', '@', '@', '@',)
		]
		for row in data_might_add:
			if verifyExists(row[1]) is False:
				data_to_add.append(row)
				print(row)
		con.executemany(sql, data_to_add)

		
		# Print out
		#data = con.execute("SELECT hp, sp FROM Character")
		#for row in data:
		#	print(row)
		

		'''
		# Print out Edward's elemental reaction to physical damage
		data = con.execute("SELECT react_phys FROM Character WHERE id = 1")
		print(data.fetchall()[0][0])
		'''