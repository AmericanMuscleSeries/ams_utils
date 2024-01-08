# Jessica Rabbot
Jessica Rabbot is a Discord bot containing custom functionality for the American Muscle Series. There are currently no plans to extend this bot to other leagues.

The bot runs on `discord.py`.

Dependencies from `requirements.txt` need to be installed via `pip`. The bot can run by executing `main.py`, i.e. `python /path/to/main.py`.

## General Use Commands
### Help
The `/help` command displays the help dialog in an ephemeral response.

### Register
The `/register` command allows the user to register for the league via modal dialog. The user's entered information is stored in `./static/data/users.json`.

### My Info
The `/myinfo` command reads the user's data from `./static/data/users.json` if it exists and displays it in an ephemeral embed.

### Name
The `/name` command allows the user to alter their preferred name.

### Number
The `/number` command allows the user to claim or change their number. This command implements logic to ensure that the number is within the correct range based on the user's registered division and prevents duplicates.

### Team
The `/team` command allows the user to set or change their team name.

### Schedule
The `/schedule` command puts the season's schedule (stored in `./static/data/schedule.json`) in an ephemeral response.

### Next Race
The `/next_race` command puts the next race in an ephemeral response. This command steps through the schedule from `./static/data/schedule.json` and compares the current date to each race's date until it finds the first race that is in the future.

## Broadcaster Commands
### Help
The `/help_broadcast` command displays the broadcast-specific help dialog in an ephemeral response.

### Number Roster
The `/number_roster` command generates a CSV file containing drivers' divisions, names, and numbers.

For example:

```
(PRO) Marty McFly,85
(AM) Doc Brown,188
```

### Overlay Roster
The `/overlay_roster` command generates a CSV file containing drivers' iRacing ID and division.

For example:

```
677234,PRO
12343,AM
```

## Admin Commands
### !sync
Syncs all slash commands globally.

### /clear
Clears the given number of messages (most recent) from the channel. If `year month day` is passed instead, it clears all messages from the channel from that date onward.

### /alter_name
Alters a driver's preferred name.

### /alter_team
Alters a driver's team.

### /division
Sets a driver's division.

### /helpp
Displays the contents of `/help` in a public embed.

### /payment
Processes a driver's payment. When a driver registers, they are given the `unpaid` role. This removes that role.

### /reginfo
Displays the registration info for a given driver in an ephemeral response.

### /registrations
Downloads `./static/data/users.json`

### /reload
Reloads an extension (cog) by name.

### /set_number
Sets a driver's number. This command performs similar logic to when a driver uses `/number`.