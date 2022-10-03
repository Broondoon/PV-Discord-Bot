# bot.py
# Created with the help of a tutorial (https://realpython.com/how-to-make-a-discord-bot-python/)
# Embed tutorial used: https://python.plainenglish.io/send-an-embed-with-a-discord-bot-in-python-61d34c711046?gi=d7b093bc5ca7
# Other tutorials were followed for understanding a topic, but no code was taken from them.

# Libraries:
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
#from discord_ui import UI, LinkButton, Button
#from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select

# External python file which holds the command functions:
import command_list
import combat_calc

#################################################### Basic Bot Functionality (Startup) ####################################################
# These are environment variables, they are grabbed from the .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Token associated with the discord bot. If something breaks, I'll try to refresh the token.
GUILD = os.getenv('DISCORD_GUILD') # 'Guild' is synonymous with 'discord server'.
IN_CHANNEL = os.getenv('DISCORD_INPUT_CHANNEL') # the input channel is where you type your commands, and recieve debug messages.
OUT_CHANNEL = os.getenv('DISCORD_OUTPUT_CHANNEL') # the output channel is where the bot will send out public messages for the players to see.

# If for whatever reason a battle needs to stop, this global variable will signal this to any running battle function.
CEASE_COMBAT = False

# Establish the Intents class for the bot (specifies certain functionalities and permissions)
bot_intents = discord.Intents.all()

# Set the three intents which require permission granting the the dev portal
bot_intents.members = False
bot_intents.presences = False
bot_intents.message_content = True

# Sets whatever prefix you want to use for the bot, and also removes the default help command so I can make my own one.
bot = commands.Bot(command_prefix='+', intents = bot_intents) #, help_command=None)

# Set up the UI class with the created bot
#ui = UI(bot) # <--- bad

# Function which runs once the bot has connected to a client guild.
@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')
	
	# Finds a reference to this guild by checking which of the guilds this bot is connected to shares the GUILD env name.
	guild = discord.utils.get(bot.guilds, name=GUILD)
	
	# A bit funky syntax, but this prints out to command line the guild the bot is connected to.
	print(
		f'\n'
		f'{bot.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})\n'
	)

	# Finds a specified channel and sends a message.
	channel = discord.utils.get(guild.channels, name=IN_CHANNEL)
	await channel.send("Ready to go.")

################################################### BUTTONS ####################################################

# Subclassing! For better Button defining.
class ChooseCharButton(Button):
	# Define some attributes for the button.
	other_potentials = [] # Contains the other possible characters which are not associated with this button. 
	turn_num = -1 # due to scoping, this number has to be ferried around.
	
	# Override the init method.
	def __init__(self, button_char, potentials, turn_num):
		# Directly initialize the parent class.
		super().__init__(label = button_char, style = discord.ButtonStyle.primary, emoji = "❓")
		self.other_potentials = [pots for pots in potentials if pots[0] != self.label]
		self.turn_num = turn_num

		print(self.other_potentials)

	# Define the callback method.
	async def callback(self, interaction):

		# Get rid of the button, now that it's been pressed.
		await interaction.response.edit_message(view = None)

		#.followup returns a webhook, which has a different method for sending messages.
		await interaction.followup.send(content = "You chose " + self.label) 

		# Set turn to equal the character the user chose.
		# Somehow prevent the character the user chose from being an option in the next turn
		#


'''
# Alternatively, view subclassing?
class ControlPanelView(View):
	
	# Use a decorator to make our button!
	@discord.ui.button(label = "hi", style = discord.ButtonStyle.primary, emoji = "❓")
	async def choose_char_callback(self, button, interaction):

		# Get rid of the button, now that it's been pressed.
		await interaction.response.edit_message(view = None)
		await interaction.followup.send_message("Hiiiiiii")
'''

#################################################### BATTLE ####################################################

# User Flow:
# user types in +battle start <battle_num>
# embed sent to OUT_CHANNEL signifying to players that battle will Start
# control panel embed sent to IN_CHANNEL
	# control panel ALWAYS contains current status of battlefield (hps, sps, conditions)
# control panel only has "start" Button
# when buttn pressed:
	# we enter the LOOP
	# ctrl panel show's who's turn it is (loop iter % num characters --> index over list of characters), and has buttons for each of their skills, as well as a redo last turn and end battle button
	# embed sent to OUT_CHANNEL which says who's turn it is
# ctrl panel

# System Flow:
# battleControlPanel() starts, setting everything up
# whosGoing() gets called, which creates buttons to call the next function, or 

# Function to build the section of the control panel which appears in every embed (basically, the current status of the battlefield). Returns an embed.
async def buildCtrlPanelPrefab(team1, team2, turn_num, battle_size):

	embed_colour = discord.Color.red()

	# Build the control panel embed which we'll be editing around a bunch.
	ctrlPanel = discord.Embed(title = "CONTROL PANEL", description = "TURN " + str(turn_num) + ", ROUND " + str(turn_num / battle_size), color = embed_colour)

	# Tell python that the fields variable is a list (so that it doesn't complain when I .append to it).
	fields = []

	#fields.append(["HP:", details[3], True])
	#[name, nums, basics, el_reacts]
	print("Team1:", team1.members)
	print("Team2:", team2.members)

	# Create a field for every character in team 1.
	for character in team1.members:
		fields.append([character[0] + ":", str(character[1][0]) + "/60 HP, " + str(character[1][1]) + "/30 SP", True])

	# Spacer field
	fields.append(['\u200b', '\u200b', False])

	# Do the same but for team 2.
	for character in team2.members:
		fields.append([character[0] + ":", str(character[1][0]) + "/60 HP, " + str(character[1][1]) + "/30 SP", True])

	# Spacer field
	fields.append(['\u200b', '\u200b', False])

	# Fields are just a nice way to format things.
	if fields is not None: #TODO: double check if fields can ever actually be None (since I define it as = []?)
		for field in fields:
			# field = [title, contents, inline_bool]
			ctrlPanel.add_field(name = field[0], value = field[1], inline = field[2])

	return ctrlPanel


# STEP TWO for a turn:
async def chooseYourMove()

# STEP ONE for a turn:
async def chooseYourCharacter(controlChannel, ctrlPanelEmbed, turn, turn_num):
	# If there are multiple options for who's going next...
	if len(turn) > 1:
		# Then we need to provide the user a few buttons to choose which to press.

		# Add a new field that explains to the user why there are multiple options here.
		ctrlPanelEmbed.add_field(name = "Two or more characters have tied MOB!", value = "Please choose which one goes first.", inline = False)

		# Create a view that our buttons will be held in.
		controlPanelView = View(timeout=None)

		# Iterate through the optional characters and create buttons for each:
		for option in turn:
				
			# Add the option to the embed.
			ctrlPanelEmbed.add_field(name = option[0], value = "MOB of " + str(option[2][3]), inline = True)

			# Create a button!
			char_button = ChooseCharButton(option[0], turn, turn_num)

			# Add the button to the view.
			controlPanelView.add_item(char_button)

		# Sent our embed with the new view inside it, which will show the button!
		await controlChannel.send(embed = ctrlPanelEmbed, view = controlPanelView)

	# Otherwise, just move on with the one option that's left to choose.
	else:
		# TODO
		pass

# This handles both user input for dictacting the flow of battle, as well as calculating combat results and outputting to the player channel.
# Parameters are the original context the initial command was sent from, and the number of the battle.
async def battleControlPanel(controlCtx, battle_num): #ctrlPanelView, battle_num): #interacted, battle_num):
	
	print("Control panel up!")

	# Setup the channels:
	guild = controlCtx.guild
	controlChannel = discord.utils.get(guild.channels, name=IN_CHANNEL)
	playerChanel = discord.utils.get(guild.channels, name=OUT_CHANNEL)

	# Set up the Battle object
	curr_battle = command_list.getBattle(int(battle_num))

	# If we couldn't find the battle, something terribly wrong happened.
	if curr_battle is None:
		print("exit ctrl panel early")
		return None

	# Might not be a necessary declaration. Could refactor so that the battle is the only thing ever passed around between functions...
	team1 = curr_battle.team1
	team2 = curr_battle.team2

	# Combat turns are measured by combatProgress # TODO: refactor this to turn_nums or something
	combat_progress = 0

	# Build a default embed prefab to make sending to OUT_CHANNEL easier.
	ctrlPanelEmbed = await buildCtrlPanelPrefab(team1, team2, combat_progress, curr_battle.size)

	# Find who's first!
	turn = combat_calc.whosFirst(curr_battle) #reminder: returns a list of [name, nums, basics, el_reacts, creature] lists.

	# The main UI loop which loops after a character has taken a turn.
	while combat_progress > -1:
		
		# Provide the user options for which character goes next.
		await chooseYourCharacter(controlChannel, ctrlPanelEmbed, turn, combat_progress)

		


		# Create an embed & view for the various moves the character can perform.
		# chooseYourMove()

		# Create an embed & view for the various targets the character can select.

		CEASE_COMBAT = True
		while CEASE_COMBAT is True:
			# May need to put a lock right here until the buttons are pressed...
			pass

		# Call combat_calc and update the current battle's status. 
		# letLooseYourAttack()

		# Get the name of the character who's next.
		#turn = combat_calc.whosNext(turn[2][3])

		# Iterate!
		combat_progress = -1

#################################################### Bot Commands ####################################################

# Help command
'''@bot.command(name='help')
async def helpCommand(ctx):
	await ctx.send(command_list.help())
'''

# Command to stop the bot
@bot.command(name='cease')
async def interruptCombat(ctx):
	# unimplemented
	pass

# For quick startup testing, without having to type 3 commands
@bot.command(name='debugstart')
async def battleCommand(ctx, *args):
	guild = ctx.guild
	channel = discord.utils.get(guild.channels, name=IN_CHANNEL)
	
	command_list.battleBuildTeam(["Build", "Team", "CIPHER", "SPYDER"])
	command_list.battleBuildTeam(["Build", "Team", "SCEPTOR", "COMPASS"])
	command_list.battleBuild(["Build", "Debug", 0, 1])
	#await channel.send("Teams and Battle built.")
	await battleCommand(ctx, "start", "0")

'''
# For a quick scattershot System test, to find anything broken since upgrading to discord.py 2.0
@bot.command(name='systemtest')
async def battleCommand(ctx, *args):
	guild = ctx.guild
	channel = discord.utils.get(guild.channels, name=IN_CHANNEL)

	listCharsCommand(ctx, *args):debug
'''

# Command for dealing with characters specifically (and their database interactions).
@bot.command(name='character')
async def listCharsCommand(ctx, *args):
	guild = ctx.guild
	channel = discord.utils.get(guild.channels, name=IN_CHANNEL) #potential flaw, if a player guesses a command, they'll still be accepted just outputed into IN_CHANNEL

	embed_title = "Character "
	embed_colour = discord.Color.light_grey()
	fields = None

	if len(args) == 0 or len(args) > 2:
		embed_title = "CHARACTER COMMANDS"
		response = command_list.charNoInput()
	elif args[0] == "details":
		embed_title += "Details"
		response = "Displaying character details for \"" + args[1] + "\"..."
		fields = command_list.charDetails(args[1])
	elif args[0] == "list":
		embed_title += "List"
		response = "Displaying characters present in the database..."
		fields = command_list.charList()
	elif args[0] == "new":
		embed_title += "(New!)"
		response = "Unimplemented"
		fields = None
	else:
		embed_title += "Err"
		response = "unimplemented"

	# Create an embedded message using the title, description, and colour defined earlier.
	new_embed = discord.Embed(title = embed_title, description = response, color = embed_colour)

	# Fields are just a nice way to format things.
	if fields is not None:
		for field in fields:
			# field = [title, contents, inline_bool]
			new_embed.add_field(name = field[0], value = field[1], inline = field[2])

	# Send the message into the discord channel
	await channel.send(embed = new_embed)

	# Fun TODO: grab a list of quotes from the stuffed teddie bear being snarky and put random one into the footer:
	# new_embed.set_footer(text = randomQuote())

# 
@bot.command(name='battle')
async def battleCommand(ctx, *args):
	guild = ctx.guild # Skip the hard way of finding the guild and just get it from the message context.
	channel = discord.utils.get(guild.channels, name=IN_CHANNEL)

	# Set basic settings of the embed
	embed_title = "Battle "
	embed_colour = discord.Color.light_grey()
	fields = None

	# For editing embeds, need to save the reference to what was sent.
	battleMsg = None

	# If-else tree to determine which command should be used based off the args given.
	if len(args) == 0 or len(args) > 7:
		response = command_list.battleNoArgs()
	elif args[0] == "build":
		if len(args) > 1 and args[1] == "team":
			response = command_list.battleBuildTeam(args)
			embed_title += "Build Team"
		else:
			if len(args) < 4:
				response = "Missing argument."
			else:
				response = command_list.battleBuild(args)
				embed_title += "Build"
	elif args[0] == "ready":
		if len(args) > 1 and args[1] == "teams":
			response = command_list.battleReadyTeams()
			embed_title += "Ready Teams"
		else:
			response = command_list.battleReady()
			embed_title += "Ready"
	elif args[0] == "start":
		response = "Battle starting..."
		fields = command_list.battleStart(args[1], OUT_CHANNEL)
		embed_title += "Start"

		# When battleStart finds a correct battle, in order to signal different behaviour, the first element in fields is ["START"].
		if fields[0][0] == "START":
			# Remove the signal so fields doesn't get messed up.
			fields.pop(0)

			# This is the only case within +battle where the OUT_CHANNEL is needed, so we define it here.
			player_channel = discord.utils.get(guild.channels, name=OUT_CHANNEL)

			# Create an embedded message using the title, description, and colour...
			new_new_embed = discord.Embed(title = "BATTLE BEGINS", description = "\"Tensions rise as wills collide. Which way will the scales turn?\"", color = discord.Color.red())

			# And send it to the OUT_CHANNEL for the players to see! (While saving the embed for later)
			battleMsg = await player_channel.send(embed = new_new_embed)
	else:
		response = "unimplemented"
		embed_title += "Err"

	# Create an embedded message using the title, description, and colour defined earlier
	new_embed = discord.Embed(title = embed_title, description = response, color = embed_colour)

	# Fields are just a nice way to format things.
	# @TODO: change the commands to actually use the fields
	if fields is not None:
		for field in fields:
			# field = [title, contents, inline_bool]
			new_embed.add_field(name = field[0], value = field[1], inline = field[2])

	# Send the message into the discord channel
	#await channel.send(response)

	# If we started a battle, the battleMsg was sent, so we need to fire up the battleControlPanel().
	if battleMsg is not None:
		
		# TODO: This bit could probably be extracted to another function...

		# Create the base of a button which will start the battle.
		start_button = Button(label = "Start Battle", style = discord.ButtonStyle.primary, emoji = "⚔")
		
		# Implement the callback, which seems to be what occurs on button press.
		async def sbutton_callback(interaction):
			# Get rid of the start button, now that it's been pressed.
			#controlPanelView.remove_item(start_button)

			# This ALSO removes the start button.
			await interaction.response.edit_message(view = None)

			# Call the coroutine to start the control panel shenanigans!
			await battleControlPanel(ctx, args[1])

		# Set the callback as the callback we created.
		start_button.callback = sbutton_callback

		# Create the View the button needs to be in, and add the button to it.
		controlPanelView = View(timeout=None)
		controlPanelView.add_item(start_button)
		#controlPanelView.remove_item(start_button) # gets rid of it

		# Sent our embed with the new view inside it, which will show the button!
		await channel.send(embed = new_embed, view = controlPanelView)

		print("battleMsg")

	else:
		# If there's no special 'start battle' stuff, just send embed as normal.
		await channel.send(embed = new_embed)

# Template for creating new commands:
#@bot.command(name='template')
#async def attack_roll(ctx):
#	guild = discord.utils.get(bot.guilds, name=GUILD)
#	channel = discord.utils.get(guild.channels, name=OUT_CHANNEL)
#	response = example.exampleResponse() # change the function to what you want to call
#	await channel.send(response)

#################################################### End of commands. ####################################################

# This starts the bot.
bot.run(TOKEN)



# Old code that I can't get rid of just yet, just in case...
'''

		# If there are multiple options for who's going next...
		if len(turn) > 1:
			# Then we need to provide the user a few buttons to choose which to press.

			# Add a new field that explains to the user why there are multiple options here.
			ctrlPanelEmbed.add_field(name = "Two or more characters have tied MOB!", value = "Please choose which one goes first.", inline = False)

			# Create a view that our buttons will be held in.
			controlPanelView = View(timeout=None)

			# Iterate through the optional characters and create buttons for each:
			for option in turn:
				
				# Add the option to the embed.
				ctrlPanelEmbed.add_field(name = option[0], value = "MOB of " + str(option[2][3]), inline = True)

				# Create the base of a button which will start the battle.
				#char_button = Button(label = option[0], style = discord.ButtonStyle.primary, emoji = "❓")
		
				# Create a button!
				char_button = ChooseCharButton(option[0])

				

				# Set the callback as the callback we created.
				#char_button.callback = choose_char_callback

				# Add the button to the view.
				controlPanelView.add_item(char_button)

			# Sent our embed with the new view inside it, which will show the button!
			await controlChannel.send(embed = ctrlPanelEmbed, view = controlPanelView)

		'''