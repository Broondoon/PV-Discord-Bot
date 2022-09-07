To run the bot:

DO ONCE:
 - ensure Python 3.8 or later is installed
 - "pip install -U discord.py"
 - "pip install --upgrade discord.py" <<<--- not sure if you have to, but discord.py 2.0 is necessary
 - "pip install -U python-dotenv"

DO EVERY TIME:
 - check the .env file has the correct discord guild & channels
 - "python bot.py" in the same directory as bot.py

NOTES:
 - when adding characters with spaces in their name, like IMMOVABLE GONZALES, to use the "+character details <name>" command, you'll have to put
	quotation marks around the full name. For example: +character details "IMMOVABLE GONZALES"
 - every playable character is marked as a "protag" in the database. The combat calculator relies on this, so don't forget to put that into any new characters