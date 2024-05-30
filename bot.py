
## Imports

import discord
from discord.ext import commands
from typing import Final
import os
from dotenv import load_dotenv
import database
import random
import datetime

## loading and reading the token from the .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

## Bot and intents setup
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='?', intents=intents)

## Functions

## name check to see if the user is in the database
def namecheck(name, connection):
        names = database.get_all_names(connection)
        for i in names:
            if (i[0]) == name:
                return True
        return False

## check if the user is in the database and if not add them
def existscheck(exists, connection, name):
    if exists == False:
        database.add_row(connection, name)

## Blackjack Command
@client.command()
async def bj(ctx, *args):
    connection = database.connect()
    database.create_tables(connection)
    name = str(ctx.author.name)
    cards = ["2","3","4","5","6","7","8","9","10","K","Q","J","A"]
    suits = ["♤","♧","♡","♢"]

    async def printcards(n, final): ## Function to print cards
        embed=discord.Embed(title="Blackjack", description=" ", color=0x000000)
        embed.set_author(name=str(ctx.author))
        
        pt = database.get_player_total(connection, n)
        dt = database.get_dealer_total(connection, n)
        if final == False:
            dt = dt - getd2value(database.get_dealer_cards(connection, n).split(",")[1])
        pc = database.get_player_cards(connection, n)
        dc = database.get_dealer_cards(connection, n)
        ps = database.get_player_suits(connection, n)
        ds = database.get_dealer_suits(connection, n)
        ps = ps.replace(" ", "")
        ds = ds.replace(" ", "")
        pc = pc.split(",")
        dc = dc.split(",")
        playerstring = ""
        dealerstring = ""
        for i in range(len(pc)):
            if i == len(pc)-1:
                playerstring += pc[i] + " "+ ps[i]
            else:
                playerstring += pc[i] + " "+ ps[i] + ", " 
        if final == False:
            dealerstring = dc[0] +" "+ ds[0] + ", X"
        else:
            for i in range(len(dc)):
                if i == len(dc)-1:
                    dealerstring += dc[i] + " "+ ds[i]
                else:
                    dealerstring += dc[i] +" "+ ds[i] + ", "
        embed.add_field(name="Your Cards [" + str(pt) +"]", value=str(playerstring), inline=False)
        embed.add_field(name="Dealers Cards [" + str(dt) +"]", value=str(dealerstring), inline=False)
        await ctx.send(embed=embed)
        if final == False: 
            await sendbuttons(ctx)

    def getd2value(dd2): ## Function to get the value of the second dealer card as it should be hidden
        if dd2 == "K" or dd2 == "Q" or dd2 == "J":
            return 10
        if dd2 == "A":
            return 11
        else:
            return int(dd2)
    
    def activecheck(name): ## Function to check if the game is active
        active = database.get_active(connection, name)
        if active == "True":
            return True
        else:
            return False
        
    def dealcard(): ## Function to deal a card
        total = 0
        card = cards[random.randint(0, len(cards)-1)]
        if (card == "A"):
            total = 11
        elif (card == "K") or (card == "Q") or (card == "J"):
            total = 10
        else: 
            total = int(card)
        return total,card
    
    def dealcards(): ## Function to deal the first two cards
        total = 0
        firstcard = cards[random.randint(0,len(cards)-1)]
        if (firstcard == "K") or (firstcard == "Q") or (firstcard == "J"):
            total += 10
        elif (firstcard == "A"):
            total += 11
        else:
            total += int(firstcard)
        secondcard = cards[random.randint(0,len(cards)-1)]
        if (secondcard == "K") or (secondcard == "Q") or (secondcard == "J"):
            total += 10
        elif (secondcard == "A"):
            total += 11
        else:
            total += int(secondcard)
        return total, firstcard, secondcard

    async def stick(): ## Function to stick
        dt = database.get_dealer_total(connection, name)
        cards = database.get_dealer_cards(connection, name)
        twoace = False
        if cards == "A,A":
            twoace = True
            dt = 12
        while dt < 17:
            xt,xcard = dealcard()
            dt += xt
            cards = database.get_dealer_cards(connection, name)
            cards = cards + "," + xcard
            database.set_dealer_cards(connection, name, cards)
            suits = database.get_dealer_suits(connection, name)
            suits = suits + suits[random.randint(0,len(suits)-1)]
            database.set_dealer_suits(connection, name, suits)
        if dt > 21:
            acecount = 0
            timesaceplayed = database.get_ace_count(connection, name)
            if twoace == True:
                timesaceplayed += 1
            cards = cards.split(",")
            for i in range(len(cards)):
                if "A" in cards[i]:
                    acecount += 1
            while acecount > timesaceplayed:
                dt -= 10 
                timesaceplayed += 1     
            if dt > 21:
                database.set_dealer_total(connection, name, dt)
                await printcards(name, True)
                database.set_game_active(connection, name, "False")
                await ctx.send("**You Win**")
                database.get_bet(connection, name)
                balance = database.get_balance(connection, name)
                database.set_balance(connection, name, balance + (2*bet))
                return
            else:
                database.set_dealer_total(connection, name, dt)
                database.set_ace_count(connection, name, timesaceplayed)
                await stick()
        else:
            database.set_dealer_total(connection, name, dt)
            await printcards(name, True)
            pt = database.get_player_total(connection, name)
            dt = database.get_dealer_total(connection, name)
            if pt > dt:
                await ctx.send("**You Win**")
                database.get_bet(connection, name)
                balance = database.get_balance(connection, name)
                database.set_balance(connection, name, balance + (2*bet))
                database.set_game_active(connection, name, "False")
            elif pt < dt:
                await ctx.send("**You Lose**")
                database.set_game_active(connection, name, "False")
            else:
                await ctx.send("**Push**")
                database.get_bet(connection, name)
                balance = database.get_balance(connection, name)
                database.set_balance(connection, name, balance + bet)
                database.set_game_active(connection, name, "False")

    async def hit(): ## Function to hit
        xt,xcard = dealcard()
        total = database.get_player_total(connection, name)
        total += xt
        database.set_player_total(connection, name, total)
        cards = database.get_player_cards(connection, name)
        cards = cards + "," + xcard
        database.set_player_cards(connection, name, cards)
        suits = database.get_player_suits(connection, name)
        suits = suits + suits[random.randint(0,len(suits)-1)]
        database.set_player_suits(connection, name, suits)
        if total > 21:
            acecount = 0
            timesaceplayed = database.get_ace_count(connection, name)
            cards = cards.split(",")
            for i in range(len(cards)):
                if "A" in cards[i]:
                    acecount += 1
            while acecount > timesaceplayed:
                total -= 10 
                timesaceplayed += 1     
            if total > 21:
                database.set_player_total(connection, name, total)
                await printcards(name, True)
                database.set_game_active(connection, name, "False")
                await ctx.send("You Lose")
                return
            else:
                database.set_player_total(connection, name, total)
                database.set_ace_count(connection, name, timesaceplayed)
                await printcards(name, False)
        else:
            await printcards(name, False)
                

    class MyView(discord.ui.View): ## Button class
        def __init__(self):
            super().__init__()
        @discord.ui.button(label='Hit', style=discord.ButtonStyle.green)
        async def asdf(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user == ctx.author:
                await interaction.response.send_message("**You Hit**")
                await hit()
            else:
                return 
        
        @discord.ui.button(label='Stick', style=discord.ButtonStyle.red) 
        async def stick(self, interaction: discord.Interaction, button: discord.ui.Button):
            if interaction.user == ctx.author:
                await interaction.response.send_message("**You Stick**")
                database.set_ace_count(connection, name, 0)
                await stick()
            else:
                return 

    async def sendbuttons(ctx: discord.Interaction): ## Function to send buttons
        await ctx.send(view=MyView())
    ## Main function
    exists = namecheck(name,connection) 
    existscheck(exists, connection, name)
    if (len(args)) == 0:
        if activecheck(name) == False:
            await ctx.send("**Provide a bet amount**")
            return
        else:
            await printcards(name, False)
            return
    if len(args) > 0:
        if activecheck(name) == True:
            await ctx.send("**Bet is already placed**")
            await printcards(name, False)
            return
    bet = int(args[0])
    if bet < 0:
        await ctx.send("**Invalid bet amount**")
        return
    active = activecheck(name)
    balance = database.get_balance(connection, name)
    if bet > balance:
        await ctx.send("**You don't have enough money**")
        return
    database.set_bet(connection, name, bet)
    database.set_balance(connection, name, balance-bet)

    if active == True:
        await printcards(name, False)
        return
    database.set_game_active(connection, name, "True")
        
    playertotal,P1,P2 = dealcards()
    database.set_player_total(connection, name, playertotal)
    database.set_player_cards(connection, name, P1 +","+ P2)
    dealertotal,D1,D2 = dealcards()
    database.set_dealer_cards(connection, name, D1 +","+ D2)
    database.set_player_suits(connection, name, suits[random.randint(0,len(suits)-1)] + suits[random.randint(0,len(suits)-1)])
    database.set_dealer_suits(connection, name, suits[random.randint(0,len(suits)-1)] + suits[random.randint(0,len(suits)-1)])
    database.set_dealer_total(connection, name, dealertotal)
    database.set_ace_count(connection, name, 0)
    await printcards(name, False)


## Balance Command
@client.command()
async def m(ctx): 
    embed=discord.Embed(title="Balance", description=" ", color=0x000000)
    embed.set_author(name=str(ctx.author))
    connection = database.connect()
    database.create_tables(connection)
    found = False
    name = str(ctx.author.name)
    names = database.get_all_names(connection)
    for i in names:
        if (i[0]) == name:
            found = True
    if found == False:
        database.add_row(connection, name)
    balance = database.get_balance(connection, name)
    embed.add_field(name="$ "+str(balance), value="",inline=False)
    await ctx.send(embed=embed)
    
## Coinflip Command
@client.command()
async def cf(ctx,*args):
    connection = database.connect()
    database.create_tables(connection)
    name = str(ctx.author.name)
    exists = namecheck(name,connection)
    existscheck(exists, connection, name)
    if len(args) == 0:
        await ctx.send("**Provide a colour and bet amount**")
        return
    if len(args) == 1:
        await ctx.send("**Provide a bet amount**")
        return
    if len(args) > 2:
        await ctx.send("**Too many arguments**")
        return
    if args[0] != "red" and args[0] != "black":
        await ctx.send("**Invalid colour**")
        return
    bet = int(args[1])
    balance = database.get_balance(connection, name)
    if bet > balance:
        await ctx.send("**You don't have enough money**")
        return
    if bet < 0:
        await ctx.send("**Invalid bet amount**")
        return
    balance = balance - bet
    result = random.choice(["red","black"])
    if result == args[0]:
        balance = balance + (2*bet)
        await ctx.send("**You win**")
    else:
        await ctx.send("**You lose**")
    database.set_balance(connection, name, balance)

## leaderboard command
@client.command()
async def leaderboard(ctx):
    connection = database.connect()
    database.create_tables(connection)
    names = database.get_all_names(connection)
    leaderboard = []
    for i in names:
        leaderboard.append([i[0],database.get_balance(connection, i[0])])
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    embed=discord.Embed(title="Leaderboard", description=" ", color=0x000000)
    embed.set_author(name=" ")
    for i in range(len(leaderboard)):
        embed.add_field(name=str(i+1) + ". " + leaderboard[i][0], value="$ "+str(leaderboard[i][1]), inline=False)
    await ctx.send(embed=embed)

## Collectpay command
@client.command()
async def collectpay(ctx):
    connection = database.connect()
    database.create_tables(connection)
    name = str(ctx.author.name)
    exists = namecheck(name,connection)
    existscheck(exists, connection, name)
    balance = database.get_balance(connection, name)
    lastpayed = database.get_last_payed(connection, name)
    lastpayed = datetime.datetime.strptime(lastpayed, '%Y-%m-%d %H:%M:%S.%f')
    today = datetime.datetime.now()
    time = today-lastpayed
    hours = time.total_seconds()/3600
    pay = int(hours*10000) ## Change this if you want to change the pay rate.
    balance += pay
    database.set_balance(connection, name, balance)
    database.set_last_payed(connection, name, today)
    await ctx.send("You have collected $ " + str(pay))

## Help command
@client.command()
async def helpme(ctx):
    embed=discord.Embed(title="Help", description=" ", color=0x000000)
    embed.set_author(name=" ")
    embed.add_field(name="?m", value="Check your balance", inline=False)
    embed.add_field(name="?bj [BET]", value="Play a game of blackjack", inline=False)
    embed.add_field(name="?cf [COLOR] [BET]", value="Play a game of coinflip", inline=False)
    embed.add_field(name="?leaderboard", value="Check the leaderboard", inline=False)
    embed.add_field(name="?collectpay", value="Collect your pay", inline=False)
    await ctx.send(embed=embed)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

client.run(TOKEN)