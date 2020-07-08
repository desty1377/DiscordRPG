import discord
from DiscordRPG.idtoname import *

token = open("token.txt", "r").read()

client = discord.Client()
counter = 0

# info about each player, id is the user's discord ID. This also means the bot remembers you between servers
class players:
    id = []
    state = [] # from tutorial to fight
    credits = []
    ship = [] # from 0 to 5, higher number means better ship
    hp = []
    weapon = [] # from 0 to 5, higher number means better weapon
    inventory = [] # string of items; each item is represented by one character


@client.event
async def on_ready(): # executes every time bot starts up
    activity = discord.Activity(name='RPG (*start)', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity, status=discord.Status.online)
    print(f"Beep, boop. Logged in as {client.user}")
    print("Reading player info")
    readfile()
    return


@client.event
async def on_message(msg): # executes every message the bot can see
    if msg.content:
        if msg.content[0] == '*': # constant prefix
            if msg.content == "*start": # it's a specific command, so it has separate check
                if checkplayer(msg.author.id) == -1:
                    if msg.channel.name == "getting-started":
                        await msg.channel.send((f"{msg.author.nick}" if msg.author.nick is not None else f"{msg.author.name}") + " has begun their adventure! You’ve been given 2,750 credits, let’s get your first ship. (*buy starflier)")
                        addplayer(msg.author.id)
                    else:
                        await msg.channel.send("Please start in #getting-started.")
                else:
                    await msg.channel.send("You have already started playing.")
            else:
                if checkplayer(msg.author.id) == -1:
                    await msg.channel.send("You haven't started yet. Please start in #getting-started using *start.")
                else:
                    player = checkplayer(msg.author.id)
                    command, vals = getvals(msg.content[1:])
                    if command == "buy":
                        if vals[0] == "starflier":
                            if players.ship[player] >= 1:
                                await msg.channel.send("You already purchased this ship.")
                            elif msg.channel.name != "getting-started":
                                await msg.channel.send("Please use this command in #getting-started.")
                            else:
                                players.ship[player] = 1
                                players.credits[player] -= 1000
                                players.hp[player] = 1000
                                await msg.channel.send((f"{msg.author.nick}" if msg.author.nick is not None else f"{msg.author.name}") + " has purchased their first ship! Let’s outfit your hunk of junk with a weapon. (*buy blaster)")
                        elif vals[0] == "blaster":
                            if players.weapon[player] >= 0:
                                await msg.channel.send("You already purchased the blaster.")
                            elif players.ship[player] < 1:
                                await msg.channel.send("You do not have a ship to mount your weapon on.")
                            elif msg.channel.name != "getting-started":
                                await msg.channel.send("Please use this command in #getting-started.")
                            else:
                                players.weapon[player] = 0
                                players.credits[player] -= 500
                                await msg.channel.send((f"{msg.author.nick}" if msg.author.nick is not None else f"{msg.author.name}") + " has mounted their first weapon on their ship! Before takeoff, we’ll buy some hull repair kits. (*buy repairbox)")
                        elif vals[0] == "repairbox":
                            if players.state[player] >= 1:
                                await msg.channel.send("You cannot purchase this kit after tutorial.")
                            elif players.inventory[player] != "000":
                                await msg.channel.send("You already purchased this kit.")
                            elif msg.channel.name != "getting-started":
                                await msg.channel.send("Please use this command in #getting-started.")
                            else:
                                players.inventory[player] = '3' + players.inventory[player][1:]
                                players.credits[player] -= 750
                                await msg.channel.send((f"{msg.author.nick}" if msg.author.nick is not None else f"{msg.author.name}") + " is now ready for their first flight! Let’s double check our systems before we launch. (*inventory)")
                    elif command == "inventory":
                        if players.state[player] >= 1:
                            await msg.channel.send("You can only use this command during the tutorial.")
                        elif msg.channel.name != "getting-started":
                            await msg.channel.send("Please use this command in #getting-started.")
                        else:
                            await msg.channel.send(f"""Credits: **{players.credits[player]}**
Ship: **{getship(players.ship[player])}**
Hitpoints: **{players.hp[player]}**/{getmaxhp(players.ship[player])}
Weapon: **{getweapon(players.weapon[player])}**
Damage: **{getdamage(players.weapon[player])}**
Accuracy: **{getacc(players.weapon[player])}**
Inventory:
**{players.inventory[player][0]}** Quick Hull Weld
**{players.inventory[player][1]}** Medium Repair Bot
**{players.inventory[player][2]}** Nanobot Repair Unit""")
                            if players.weapon[player] > -1 and players.ship[player] > 0 and players.inventory[player][0] == '3':
                                await msg.channel.send("Pre-flight checks are good! Use the autopilot (*firstflight) to launch!")
                    elif command == "firstflight":
                        if players.state[player] != 0:
                            await msg.channel.send("You already completed the tutorial and flown your first flight.")
                        elif players.ship[player] < 1:
                            await msg.channel.send("It's difficult to fly without a ship. You should definitely buy one. (*buy starflier)")
                        elif players.weapon[player] < 0:
                            await msg.channel.send("Space is full of dangers. You need a weapon. (*buy blaster)")
                        elif players.inventory[player] != "300":
                            await msg.channel.send("Without any repair tools, you won't last much. Get some Quick Hull Welds. (*buy repairbox)")
                        else:
                            players.state[player] = 3
                            updatefile()
                            await msg.channel.send((f"{msg.author.nick}" if msg.author.nick is not None else f"{msg.author.name}") + " has their first flight! Welcome to (system one). Use (*help) from your ship’s dashboard to see what you can do!")
    return


def getvals(txt): # splits the message into command and its arguments
    x = txt.split()
    return x[0], x[1:]


def checkplayer(pid): # there is an index() function but it errors when it does not find the argument (-1 normally means last in list)
    i = 0
    while i < len(players.id):
        if players.id[i] == int(pid):
            return i
        i += 1
    return -1


def addplayer(pid):
    players.id.append(pid)
    players.credits.append(2750)
    players.hp.append(1)
    players.inventory.append("000") # empty inventory
    players.state.append(0) # tutorial state
    players.weapon.append(-1)
    players.ship.append(0) # no weapon or ship
    writeplayer()
    return


def writeplayer(): # adds player to the list. On the list the player already has the starting items, ensuring they can play if the bot crashed mid-start
    f = open("players.txt", "a") # (a stands for append)
    f.write(str(players.id[-1]) + " 0 2750 0 1 -1 000")
    f.close()
    return


def updatefile():
    i = 0
    s = ""
    while i < len(players.id):
        s += str(players.id[i]) + ' ' + str(players.state[i]) + ' ' + str(players.credits[i]) + ' ' + str(players.ship[i]) + ' ' + str(players.hp[i]) + ' ' + str(players.weapon[i]) + ' ' + players.inventory[i] + '\n'
        i += 1
    f = open("players.txt", "w")
    f.write(s)
    f.close()
    return


def readfile():
    f = open("players.txt")
    for x in f:
        if x == "":
            f.close()
            return
        vals = x.split()
        print(vals)
        players.id.append(int(vals[0]))
        if vals[1] == "4":
            players.state.append(3)
        else:
            players.state.append(int(vals[1]))
        players.credits.append(int(vals[2]))
        players.ship.append(int(vals[3]))
        players.hp.append(int(vals[4]))
        players.weapon.append(int(vals[5]))
        players.inventory.append(vals[6])
    f.close()
    return


if __name__ == "__main__":
    client.run(token)
