import discord
import datetime
import gspread

from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

#discord API

TOKEN = 'NjExNDM2MzA4ODI0MzI2MTQ1.XVTyog.Or7HJ636b-isQc5CWw5NqIXEjFI'

client = commands.Bot(command_prefix='!')
client.remove_command("help")

#gspread API

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
credentials = ServiceAccountCredentials.from_json_keyfile_name('VLDR-167b33a1bc35.json', scope)
gc = gspread.authorize(credentials)
player_sheet = gc.open_by_key('1EfYOD1UireD-DDzfkIVOmvjq14UX13dI1SsTgfnhXjA').sheet1
room_sheet = gc.open_by_key('1C2VBdqrHQpgP6Es9op4SV64AdNvtGo_pak2IM_6fXyg')

#--------------------------------- CODE GOES BELOW ---------------------------------#

player_list = {'Player 1': 1, 'Player 2': 2, 'Player 3': 3, 'Player 4': 4, 
'Player 5': 5, 'Player 6': 6, 'Player 7': 7, 'Player 8': 8, 
'Player 9': 9, 'Player 10': 10, 'Player 11': 11, 'Player 12': 12, 'Player Test' : 13}

room_list = {'Lobby': [0, 1], 'Number 12 Door': [0, 2], 'Ambidex Booths': [0, 3], 'Lounge': [0, 4], 'Cabin A': [0, 5],
"Captain's Quarters": [0, 6], 'Infirmary': [0, 8], 'Engine Room': [0, 9], 'Personal Lockers': [0, 10], 'Radio Office': [0, 11],
'Cafeteria': [1, 1], 'Kitchen': [1, 2], 'Chemistry Lab': [1, 3], 'Storage': [1, 4], 'Art Gallery': [1, 5], 'Cabin B': [1, 6],
'Solitary': [1, 7], 'Computer Lab': [1, 8], 'Woodworking': [1, 9], 'Blacksmith': [2, 0], 'Library': [2, 1], 'Casino': [2, 2],
'Vault': [2, 3], 'Cabin C': [2, 4], 'Power Room': [2, 5], 'Gym': [2, 6], 'Pool': [2, 7]}

AP_ROW = 4
ITEMS = 6
PRIVATE_ITEMS = 13
ROLE_ITEMS = 15
HEALTH = 17
MAX_HEALTH = 18
BP = 19

ROOM_PUZZLE = 4
ROOM_ITEMS = 5

#--------------------------------- MODERATOR COMMANDS ---------------------------------#

@client.command()
async def sendlog(ctx, log_channel : discord.TextChannel, dest_channel : discord.TextChannel):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        messages = await log_channel.history(limit = 1000).flatten()
        flag = True

        count = 0
        i = len(messages) - 1
        msg = ''
        while flag:
            if (count > 2000):
                count = 0
                await dest_channel.send(msg)
                msg = ''

            newMsg = ('*Author:* ' + str(messages[i].author) + ', *Room:* ' + str(messages[i].channel) + '\n' + '*Message:* ' + str(messages[i].content) + '\n\n')
            msg = msg + newMsg.replace('@', '')
            count = count + len(msg)
            i = i - 1

            if (i == -1):
                flag = False

        await dest_channel.send(msg)
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def change_ap(ctx, target : discord.Role, change_amount : int):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        col = player_list[target.name] + 1
        ap = player_sheet.cell(AP_ROW, col).value

        ap = int(int(ap) + change_amount)
        player_sheet.update_cell(AP_ROW, col, str(ap))

        await ctx.send("Changed " + str(target) + " AP by " + str(change_amount) + ". " + str(target) + " now has " + str(ap) + " AP.")
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def change_health(ctx, target : discord.Role, change_amount : int):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        col = player_list[target.name] + 1
        health = player_sheet.cell(HEALTH, col).value

        health = int(int(health) + change_amount)
        player_sheet.update_cell(HEALTH, col, str(health))

        await ctx.send("Changed " + str(target) + " health by " + str(change_amount) + ". " + str(target) + " now has " + str(health) + " health.")
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def change_bp(ctx, target : discord.Role, change_amount : int):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        col = player_list[target.name] + 1
        bp = player_sheet.cell(BP, col).value

        bp = int(int(bp) + change_amount)
        player_sheet.update_cell(BP, col, str(bp))

        await ctx.send("Changed " + str(target) + " BP by " + str(change_amount) + ". " + str(target) + " now has " + str(bp) + " BP.")
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def get_ap(ctx, target : discord.Role):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        col = player_list[target.name] + 1
        ap = player_sheet.cell(AP_ROW, col).value
        await ctx.send(target.name + "'s AP is: " + str(ap))
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def reset_ap(ctx):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        for col in range(2, 13):
            player_sheet.update_cell(AP_ROW, col, 50)
        await ctx.send("Set all player's AP to 50 at " + datetime.datetime.now().strftime("%c") + ".")
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def get_health(ctx, target : discord.Role):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        col = player_list[target.name] + 1
        health = player_sheet.cell(HEALTH, col).value
        await ctx.send(target.name + "'s health is: " + str(health))
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def get_inventory(ctx, target : discord.Role):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        col = player_list[target.name] + 1

        msg = "INVENTORY OF " + target.name + ": \n"
        for row in range(ITEMS, ITEMS + 5):
            msg = msg + player_sheet.cell(row, col).value + "\n"
        if col == 11:
            for row in range(ITEMS + 6, ITEMS + 7):
                msg = msg + player_sheet.cell(row, col).value + "\n"
        msg = msg + "\nPRIVATE ITEMS: \n" + player_sheet.cell(PRIVATE_ITEMS, col).value
        if col == 11:
            msg = msg + player_sheet.cell(PRIVATE_ITEMS + 1, col).value + "\n"
        msg = msg + "\nROLE ITEMS: \n" + player_sheet.cell(ROLE_ITEMS, col).value
        await ctx.send(msg)
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def items(ctx, room : str):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        if room in room_list:
            index = room_list[room]
            room_worksheet = room_sheet.get_worksheet(index[0])
            items = room_worksheet.cell(ROOM_ITEMS, index[1] + 2).value
            await ctx.send("Items in " + str(room) + ": \n" + str(items))
        else: 
            await ctx.send("ERROR - This is not a valid room.")
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

@client.command()
async def puzzle(ctx, room : str):
    if ("Moderator" in [role.name for role in ctx.author.roles]):
        if room in room_list:
            index = room_list[room]
            room_worksheet = room_sheet.get_worksheet(index[0])
            items = room_worksheet.cell(ROOM_PUZZLE, index[1] + 2).value
            await ctx.send("Puzzle in " + str(room) + ": \n" + str(items))
        else: 
            await ctx.send("ERROR - This is not a valid room.")
    else:
        await ctx.send("ERROR - You are not a moderator.")
    return

#--------------------------------- PLAYER COMMANDS ---------------------------------#

@client.command()
async def ap(ctx):
    if ctx.channel.category_id == 619515301914083348:
        col = get_role_int(ctx.author.roles)
        if col == -1:
            await ctx.send("ERROR - You are not a player.")
            return
        
        ap = player_sheet.cell(AP_ROW, col).value
        await ctx.send("You have: " + str(ap) + " AP.")
    else:
        await ctx.send("ERROR - Command must be used in your private channel.")
    return

@client.command()
async def inventory(ctx):
    if ctx.channel.category_id == 619515301914083348:
        col = get_role_int(ctx.author.roles)
        if col == -1:
            await ctx.send("ERROR - You are not a player.")
        else:
            msg = "CURRENT INVENTORY: \n"
            for row in range(ITEMS, ITEMS + 5):
                msg = msg + player_sheet.cell(row, col).value + "\n"
            if col == 11:
                for row in range(ITEMS + 6, ITEMS + 7):
                    msg = msg + player_sheet.cell(row, col).value + "\n"
            msg = msg + "\nPRIVATE ITEMS: \n" + player_sheet.cell(PRIVATE_ITEMS, col).value
            if col == 11:
                msg = msg + player_sheet.cell(PRIVATE_ITEMS + 1, col).value + "\n"
            msg = msg + "\nROLE ITEMS: \n" + player_sheet.cell(ROLE_ITEMS, col).value
            await ctx.send(msg)
    else:
        await ctx.send("ERROR - Command must be used in your private channel.")
    return

@client.command()
async def health(ctx):
    if ctx.channel.category_id == 619515301914083348:
        col = get_role_int(ctx.author.roles)
        if col == -1:
            await ctx.send("ERROR - You are not a player.")
        else:
            health = player_sheet.cell(HEALTH, col).value
            max_health = player_sheet.cell(MAX_HEALTH, col).value
            await ctx.send("You have: " + str(health) + " health. Your maximum health is " + str(max_health) + ".")
    else:
        await ctx.send("ERROR - Command must be used in your private channel.")
    return

@client.command()
async def bp(ctx):
    if ctx.channel.category_id == 619515301914083348:
        col = get_role_int(ctx.author.roles)
        if col == -1:
            await ctx.send("ERROR - You are not a player.")
        else:
            bp = player_sheet.cell(BP, col).value
            await ctx.send("You have: " + str(bp) + " BP.")
    else:
        await ctx.send("ERROR - Command must be used in your private channel.")
    return

@client.command()
async def help(ctx):
    await ctx.send("""```All available commands:\n
    "!help" - Display this message.
    "!inventory" - Display your current inventory.
    "!health" - Display your current and maximum health.
    "!ap" - Display your number of action points.
    "!bp" - Display your number of bracelet points.
    
    For more help, tag a moderator!```""")

def get_role_int(roles):
    col = -1
    for role in roles:
        if role.name in player_list:
            col = player_list[role.name] + 1
    return col
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(process.env.BOT_TOKEN)
