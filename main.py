import discord
from idtoname import *
import random
import math

token = open("token.txt", "r").read()

client = discord.Client()

# info about each player, id is the user's discord ID. This also means the bot remembers you between servers
class players:
    id = []
    state = [] # from tutorial to fight
    credits = []
    ship = [] # from 0 to 5, higher number means better ship
    hp = []
    weapon = [] # from 0 to 5, higher number means better weapon
    inventory = [] # string of items; each item is represented by one character

class fights:
    id = []
    enemyship = []
    enemyweapon = []
    enemyhp = []


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
    if msg.content and msg.author.id != client.user.id:
        if msg.content[0] == '*': # constant prefix
            if msg.content == "*start": # it's a specific command, so it has separate check
                if checkplayer(msg.author.id) == -1:
                    if msg.channel.name == "getting-started":
                        await msg.channel.send(f"{msg.author.display_name} has begun their adventure! You’ve been given 2,750 credits, let’s get your first ship. (*buy starflier)")
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
                                await msg.channel.send(f"{msg.author.display_name} has purchased their first ship! Let’s outfit your hunk of junk with a weapon. (*buy blaster)")
                        elif vals[0] == "blaster":
                            if players.weapon[player] == 1:
                                await msg.channel.send("You already purchased the blaster.")
                            elif players.ship[player] < 1:
                                await msg.channel.send("You do not have a ship to mount your weapon on.")
                            elif msg.channel.name != "getting-started":
                                await msg.channel.send("Please use this command in #getting-started.")
                            else:
                                players.weapon[player] = 0
                                players.credits[player] -= 500
                                await msg.channel.send(f"{msg.author.display_name} has mounted their first weapon on their ship! Before takeoff, we’ll buy some hull repair kits. (*buy repairbox)")
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
                                await msg.channel.send(f"{msg.author.display_name} is now ready for their first flight! Let’s double check our systems before we launch. (*inventory)")
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
**{players.inventory[player][0]}**/5 Quick Hull Weld
**{players.inventory[player][1]}**/3 Medium Repair Bot
**{players.inventory[player][2]}**/1 Nanobot Repair Unit""")
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
                            players.state[player] = 1
                            updatefile()
                            await msg.channel.send(f"{msg.author.display_name} has their first flight! Welcome to (system one). Use (*help) from your ship’s dashboard to see what you can do!")
                    elif command == "help":
                        if players.state[player] == 1:
                            if msg.channel.name != "in-space":
                                await msg.channel.send("You are in space, please go to #in-space to use ship commands.")
                            else:
                                await msg.channel.send("""Your ship's dashboard shows:
*explore - explore the system, might encounter an enemy
*check - displays current status
*dock - returns you to base, where you can *shop and *repair""")
                        elif players.state[player] == 3:
                            if msg.channel.name != "in-base":
                                await msg.channel.send("You are docked, please go to #in-base to use docked commands.")
                            else:
                                await msg.channel.send("""When docked, you can:
*repair - repair your ship at a rate of 5 credits for 10 hp
*shop - enters Tobias' shop
*launch - go to space, where you can *explore the system""")
                    elif command == "check":
                        if players.state[player] != 1 and players.state[player] != 2:
                            await msg.channel.send("This command can only be used in space.")
                        elif msg.channel.name != "in-space":
                            await msg.channel.send("Please use this command in the #in-space channel")
                        else:
                            await msg.channel.send(f"""Credits: **{players.credits[player]}**
Ship: **{getship(players.ship[player])}**
Hitpoints: **{players.hp[player]}**/{getmaxhp(players.ship[player])}
Weapon: **{getweapon(players.weapon[player])}**
Damage: **{getdamage(players.weapon[player])}**
Accuracy: **{getacc(players.weapon[player])}**
Inventory:
**{players.inventory[player][0]}**/5 Quick Hull Weld
**{players.inventory[player][1]}**/3 Medium Repair Bot
**{players.inventory[player][2]}**/1 Nanobot Repair Unit""")
                    elif command == "explore":
                        if players.state[player] != 1:
                            await msg.channel.send("This command can only be used in space.")
                        elif msg.channel.name != "in-space":
                            await msg.channel.send("Please use this command in the #in-space channel.")
                        else:
                            random.seed()
                            a = random.randint(0, 3)
                            if a == 0:
                                await msg.channel.send(random.choice(["You fly around and see nothing.", "You’re comms start hissing static and after a moment your ship goes offline. Power is restored after a minute and you get the hell out of there.", "On your scanner you see the callsign Freelancer Alpha 1/1. But it disappears after a few seconds.", "In the distance you see pirates attacking a transport convoy.\nAn explosion happens, destroying the entire convoy.", "You hear static and hissing coming from your comms.\nAll of a sudden, your ship goes offline and you hear a weird noise coming from outside.\nAfter a few seconds, the engines come back online and you get the hell out of there.", "You fly around, nothing really happens. The sun looks really pretty though.", "It is pitch black.\nYou are likely to be eaten by a grue."]))
                            else:
                                players.state[player] = 2
                                fights.id.append(player)
                                ship, weapon = makeenemy()
                                fights.enemyship.append(ship)
                                fights.enemyhp.append(int(getenemymaxhp(ship)))
                                fights.enemyweapon.append(weapon)
                                responses = [f"You catch a Light Pirate Ship in an asteroid field!\nPirate: \"Seems to be my lucky day. You're going down!\"", "A Medium Pirate Ship ambushes you!\nPirate: \"Bad move to be travelling alone. Say goodbye!\"", "You think it's a shipwreck, but it's a Heavy Pirate Ship!\nPirate: \"This'll be fun! You've got nowhere to run.\"", "A Pirate Dreadnaught moves out from a nearby nebula!\nPirate: \"You're outclassed and outgunned. Time to die!\""]
                                if ship < 4:
                                    await msg.channel.send(responses[ship])
                                    await msg.channel.send(f"Looks like their ship has a {getenemyweapon(weapon)}.")
                                else:
                                    await msg.channel.send("An unrecognizable object de-cloaks infront of you!\nLooks to be armed and incredibly dangerous.\n*A mix of static and hissing emit from your comms*")
                                await msg.channel.send("""What do you do?
*attack
*use
*check
*scan
*flee""")
                    elif command == "use":
                        if players.state[player] != 2:
                            await msg.channel.send("You can only use repair systems when in a fight.")
                        elif msg.channel.name != "in-space":
                            await msg.channel.send("Please use this command in the #in-space channel.")
                        else:
                            if len(vals) == 0:
                                await msg.channel.send(f"""You pull up the dashboard for repairs. Which kind of repair do you want to use?
1 - Quick Hull Weld **{players.inventory[player][0]}**/5
2 - Medium Repair Bot **{players.inventory[player][1]}**/3
3 - Nanobot Repair Unit **{players.inventory[player][2]}**/1
(*use (number))""")
                            elif vals[0] in ["1", "2", "3"]:
                                if int(players.inventory[player][int(vals[0]) - 1]) == 0:
                                    await msg.channel.send("You don't have this item.")
                                elif players.hp[player] == int(getmaxhp(players.ship[player])):
                                    await msg.channel.send("You don't need to repair the ship.")
                                else:
                                    itemuse(int(vals[0]) - 1, player)
                                    j = [0.15, 0.25, 0.8]
                                    responses = ["The bots get together and repair part of your ship!", "The bots get together and repair part of your ship!", "Nanobots swarm around your ship, covering up holes in your ships hull, greatly repairing your ship."]
                                    players.hp[player] += round(float(getmaxhp(players.ship[player])) * j[int(vals[0]) - 1])
                                    if players.hp[player] > int(getmaxhp(players.ship[player])):
                                        players.hp[player] = int(getmaxhp(players.ship[player]))
                                    await msg.channel.send(responses[int(vals[0]) - 1])
                                    await msg.channel.send(f"Repaired back to **{players.hp[player]}** hp!")
                                    updatefile()
                                    dmg = pirateshot(player)
                                    players.hp[player] -= dmg
                                    if dmg != 0:
                                        await msg.channel.send(f"{getenemyship(fights.enemyship[fights.id.index(player)])} comes around for an attack and deals **{dmg}** dmg to you!")
                                        updatefile()
                                    else:
                                        await msg.channel.send(f"{getenemyship(fights.enemyship[fights.id.index(player)])}'s weapons bounce off your shield, leaving you unharmed this turn!")
                                    if players.hp[player] <= 0:
                                        players.state[player] = -1
                                        players.inventory[player] = "000"
                                        await msg.channel.send("You are dead.\nAll consumables are lost.\nType *respawn to spawn back at base.")
                                        endoffight(fights.id.index(player))
                                        updatefile()
                    elif command == "attack":
                        if players.state[player] != 2:
                            await msg.channel.send("You can only use repair systems when in a fight.")
                        elif msg.channel.name != "in-space":
                            await msg.channel.send("Please use this command in the #in-space channel.")
                        else:
                            dmg = humanshot(player)
                            index = fights.id.index(player)
                            fights.enemyhp[index] -= dmg
                            if dmg != 0:
                                await msg.channel.send(f"**{msg.author.display_name}** attacks the **{getenemyship(fights.enemyship[index])}** dealing **{dmg}** damage.")
                                if fights.enemyhp[index] <= 0: # enemy death
                                    cred = [[200, 400], [400, 600], [600, 800], [800, 1000], [5000, 10000]]
                                    players.state[player] = 1
                                    reward = random.randint(cred[fights.enemyship[index]][0], cred[fights.enemyship[index]][1])
                                    await msg.channel.send(f"**{msg.author.display_name}** has destroyed the **{getenemyship(fights.enemyship[index])}**!")
                                    await msg.channel.send(f"Gained **{reward}** credits.")
                                    if fights.enemyship[index] == 1:
                                        if players.inventory[player][0] != "5":
                                            players.inventory[player] = str(int(players.inventory[player][0]) + 1) + players.inventory[player][1:]
                                            await msg.channel.send("Gained 1 Quick Hull Weld.")
                                        else:
                                            await msg.channel.send("You found a Quick Hull Weld but could not take it with you because of full inventory.")
                                    elif fights.enemyship[index] == 2:
                                        if players.inventory[player][0] != "5":
                                            players.inventory[player] = str(int(players.inventory[player][0]) + 1) + players.inventory[player][1:]
                                            await msg.channel.send("Gained 1 Quick Hull Weld.")
                                        else:
                                            await msg.channel.send("You found a Quick Hull Weld but could not take it with you because of full inventory.")
                                        if random.randint(1, 4) == 1:
                                            if players.inventory[player][1] != "3":
                                                players.inventory[player] = players.inventory[player][0] + str(int(players.inventory[player][1]) + 1) + players.inventory[player][2]
                                                await msg.channel.send("Gained 1 Medium Repair Bot.")
                                            else:
                                                await msg.channel.send("You found a Medium Repair Bot but could not take it with you because of full inventory.")
                                    elif fights.enemyship[index] == 3:
                                        if players.inventory[player][1] != "3":
                                            players.inventory[player] = str(int(players.inventory[player][0]) + 1) + players.inventory[player][1:]
                                            await msg.channel.send("Gained 1 Medium Repair Bot.")
                                        else:
                                            await msg.channel.send("You found a Medium Repair Bot but could not take it with you because of full inventory.")
                                        if random.randint(1, 4) == 1:
                                            if players.inventory[player][2] != "1":
                                                players.inventory[player] = players.inventory[player][0] + str(int(players.inventory[player][1]) + 1) + players.inventory[player][2]
                                                await msg.channel.send("Gained 1 Nanobot Repair Unit.")
                                            else:
                                                await msg.channel.send("You found a Nanobot Repair Unit but could not take it with you because of full inventory.")
                                    endoffight(index)
                                    updatefile()
                                    return
                            else:
                                await msg.channel.send("Your weapons overshot and missed your target! No damage was dealt.")
                            dmg = pirateshot(player)
                            players.hp[player] -= dmg
                            if dmg != 0:
                                await msg.channel.send(f"**{getenemyship(fights.enemyship[fights.id.index(player)])}** comes around for an attack and deals **{dmg}** dmg to you!")
                                updatefile()
                            else:
                                await msg.channel.send(f"**{getenemyship(fights.enemyship[fights.id.index(player)])}**'s weapons bounce off your shield, leaving you unharmed this turn!")
                            if players.hp[player] <= 0:
                                players.state[player] = -1
                                players.inventory[player] = "000"
                                await msg.channel.send("You are dead.\nAll consumables are lost.\nType *respawn to spawn back at base.")
                                endoffight(index)
                                updatefile()
                    elif command == "scan":
                        if players.state[player] != 2:
                            await msg.channel.send("You can only use repair systems when in a fight.")
                        elif msg.channel.name != "in-space":
                            await msg.channel.send("Please use this command in the #in-space channel.")
                        else:
                            index = fights.id.index(player)
                            if fights.enemyship[index] != 4:
                                await msg.channel.send(f"""Ship: **{getenemyship(fights.enemyship[index])}**
HP: **{fights.enemyhp[index]}**/{getenemymaxhp(fights.enemyship[index])}
Weapon: **{getenemyweapon(fights.enemyweapon[index])}**
Accuracy: **{getenemyacc(fights.enemyweapon[index])}**
Damage: **{getenemydamage(fights.enemyweapon[index])}**""")
                            else:
                                await msg.channel.send("Your scanners are trying to make sense of what's in front of you.")
                                await msg.channel.send(f"""**Ship: ?ES?O??SI?E?**
HP: **{str(fights.enemyhp[index])[0]}???**/3???
Weapon: **?ES?O??????O?**
Accuracy: **?0%**
Damage: **?5?-?5?**""")
                    elif command == "flee":
                        if players.state[player] != 2:
                            await msg.channel.send("You can only use repair systems when in a fight.")
                        elif msg.channel.name != "in-space":
                            await msg.channel.send("Please use this command in the #in-space channel.")
                        elif random.randint(1, 4) != 1:
                            endoffight(fights.id.index(player))
                            players.state[player] = 1
                            await msg.channel.send(f"Using evasive maneuvers, **{msg.author.display_name}** outsmarts their foe and manages to get away.")
                        else:
                            await msg.channel.send(f"The **{getenemyship(fights.enemyship[fights.id.index(player)]) if fights.enemyship[fights.id.index(player)] != 4 else '?ES?O??SI?E?'}** manages to hit your engines and stops you from fleeing.")
                            dmg = pirateshot(player)
                            players.hp[player] -= dmg
                            if dmg != 0:
                                await msg.channel.send(f"**{getenemyship(fights.enemyship[fights.id.index(player)]) if fights.enemyship[fights.id.index(player)] != 4 else '?ES?O??SI?E?'}** comes around for an attack and deals **{dmg}** dmg to you!")
                                if players.hp[player] <= 0:
                                    players.state[player] = -1
                                    players.inventory[player] = "000"
                                    await msg.channel.send("You are dead.\nAll consumables are lost.\nType *respawn to spawn back at base.")
                                    endoffight(fights.id.index(player))
                                    updatefile()
                                    return
                                updatefile()
                            else:
                                await msg.channel.send(
                                    f"{getenemyship(fights.enemyship[fights.id.index(player)])}'s weapons bounce off your shield, leaving you unharmed this turn!")
                    elif command == "dock":
                        if players.state[player] != 1:
                            await msg.channel.send("This command can only be used in space.")
                        elif msg.channel.name != "in-space":
                            await msg.channel.send("Please use this command in the #in-space channel.")
                        else:
                            players.state[player] = 3
                            await msg.channel.send(f"{msg.author.display_name} has returned to their base. They eat some food, maybe sleep a little.")
                            updatefile()
                    elif command == "launch":
                        if players.state[player] != 3 and players.state[player] != 4:
                            await msg.channel.send("This command can only be used when docked.")
                        elif msg.channel.name != "docked":
                            await msg.channel.send("Please use this command in the #docked channel.")
                        else:
                            players.state[player] = 1
                            await msg.channel.send(f"{msg.author.display_name} has launched into space!")
                            updatefile()
                    elif command == "repair":
                        if players.state[player] != 3 and players.state[player] != 4:
                            await msg.channel.send("This command can only be used when docked.")
                        elif msg.channel.name != "docked":
                            await msg.channel.send("Please use this command in the #docked channel.")
                        elif players.hp[player] == int(getmaxhp(players.ship[player])):
                            await msg.channel.send("There is no need to repair anything, you already have full hp.")
                        else:
                            if math.ceil((float(getmaxhp(players.ship[player])) - players.hp[player]) / 10.0) * 5 > players.credits[player]:
                                players.hp[player] += math.floor(players.credits[player] / 5) * 10
                                players.credits[player] %= 5
                                await msg.channel.send(f"You could not afford to repair your ship completely, but you brought it back to **{players.hp[player]}**/{getmaxhp(players.ship[player])} hp.")
                            else:
                                players.credits[player] -= math.ceil((float(getmaxhp(players.ship[player])) - players.hp[player]) / 10.0) * 5
                                await msg.channel.send(f"Your ship's hull integrity has now been restored to maximum! You now have **{players.credits[player]}** credits.")
                                players.hp[player] = int(getmaxhp(players.ship[player]))
                            updatefile()
                    elif command == "shop":
                        if players.state[player] != 3 and players.state[player] != 4:
                            await msg.channel.send("This command can only be used when docked.")
                        elif msg.channel.name != "docked":
                            await msg.channel.send("Please use this command in the #docked channel.")
                        elif players.state[player] == 3:
                            await msg.channel.send("You already are in the shop. Try *upgrades, *weapons and *special to see items for purchase.")
                        else:
                            await msg.channel.send("You've now entered Tobias' shop. You can ask him about ship *upgrades, new *weapons and *special items.")
                    elif command == "respawn":
                        if players.state[player] != -1:
                            await msg.channel.send("You are not dead.")
                        else:
                            players.state[player] = 3
                            players.hp[player] = int(getmaxhp(players.ship[player]))
                            await msg.channel.send("You returned to your base.")
                            updatefile()
    return


def endoffight(index):
    fights.enemyship.pop(index)
    fights.enemyhp.pop(index)
    fights.enemyweapon.pop(index)
    fights.id.pop(index)
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
        if vals[1] == "2":
            players.state.append(1)
        else:
            players.state.append(int(vals[1]))
        players.credits.append(int(vals[2]))
        players.ship.append(int(vals[3]))
        players.hp.append(int(vals[4]))
        players.weapon.append(int(vals[5]))
        players.inventory.append(vals[6])
    f.close()
    return


def itemuse(item, player):
    if item == 0:
        players.inventory[player] = str(int(players.inventory[player][0]) - 1) + players.inventory[player][1:]
    elif item == 1:
        players.inventory[player] = players.inventory[player][0] + str(int(players.inventory[player][1]) - 1) + players.inventory[player][2]
    else:
        players.inventory[player] = players.inventory[player][:2]


def makeenemy():
    g = random.randint(1, 20)
    if g == 20:
        return 4, 7
    elif g >= 18:
        h = random.randint(1, 20)
        if h <= 10:
            return 3, 4
        elif h <= 17:
            return 3, 5
        else:
            return 3, 6
    elif g >= 15:
        h = random.randint(1, 10)
        if h == 10:
            return 2, 1
        elif h <= 7:
            return 2, 3
        else:
            return 2, 2
    elif g >= 9:
        h = random.randint(1, 5)
        if h == 5:
            return 1, 0
        elif h == 4:
            return 1, 2
        else:
            return 1, 1
    else:
        h = random.randint(1, 10)
        if h == 10:
            return 0, 3
        elif h <= 8:
            return 0, 1
        else:
            return 0, 0


def humanshot(pid):
    accuracy = getacc(players.weapon[pid])
    if random.randint(1, 100) <= int(accuracy[:-1]):
        dmg = getdamage(players.weapon[pid])
        a = dmg.split('-')
        return random.randint(int(a[0]), int(a[-1]))
    else:
        return 0

def pirateshot(pid):
    index = fights.id.index(pid)
    accuracy = getenemyacc(fights.enemyweapon[index])
    if random.randint(1, 100) <= int(accuracy[:-1]):
        dmg = getenemydamage(fights.enemyweapon[index])
        a = dmg.split('-')
        return random.randint(int(a[0]), int(a[-1]))
    else:
        return 0


if __name__ == "__main__":
    client.run(token)
