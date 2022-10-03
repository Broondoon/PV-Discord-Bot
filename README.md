# PV-Discord-Bot
A discord bot meant to automate a custom Tabletop Role Playing Game system, Project Vegas. Written in Python and utilizing SQLite, it tracks characters and enemies while combat progresses.

# Background
"Project Vegas" is the name of a TTRPG campaign ran by two friends of mine. While heavily inspired by the Persona series of video games, the combat system is complicated and too dense for typical TTRPG play. As such sessions get bogged down in the rules as players grow slowly frusterated. That is why the PV-Discord-Bot will take care of the battle system to streamline gameplay in order to improve the experience of Project Vegas.

# Purpose
The PV-Discord-Bot will handle all combat calculations and character stat management. It will not handle narrative components of gameplay. It will draw from a database of set characters to run combat encounters, allowing one controlling user to designate which actions characters take in combat. It will not be designed for multiple users to interact with at the same time.

# Development Plan
Currently, the PV-Discord-Bot is close to being finished. However, there are some features which stand in the way of its completion. 

## Essential Features
- Database Overhaul
   - Tables for moves known, significant bonds, and items
   - Enforced relationships between tables, such as many-to-one and many-to-many
- Move selection
- Enemy targeting
- Result calulation, including combo effects such as Boosts, Crits and Instant KOs
- Dynamic battlefiled updating, such as as manually editing the HP or SP of combattents

## Advanced Mechanics Features
- Unique monster-only abilities (such as Charge, AOE, Reflect, etc) 
- Item use in and out of battle
- Post-combat permanence, such as HP/SP spent carrying over to the next fight

## Quality of Life Features
- Dynamic character creation while the bot is in use
- Updated combat flow options, such as a "go back" button when the wrong option was chosen and the user would like to go back
