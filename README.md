Blackjack Bot
A discord bot built for simple blackjack and coinflip games

Setup:
1. Inside the bots directory you must create an empty folder, "data".
2. in the .env file you must paste in your own discord bots token.
3. you must install dotenv and discord using pip install.
4. to turn the bot on you can run the bot.py script

Command List:
- ?bj {BET} ## Blackjack command, bot replies with a discord embed where the user can select Hit or Stick, other users cannot press these buttons. Bet must be > 0 
- ?cf {Color} {BET} ## Coinflip command, the user can either select "black" or "red", Bet must be > 0 
- ?m ## Balance command, shows the users balance within a discord embed
- ?collectpay ## Collect Pay command, users can collect a payment of money, this defaults at 10000/h but can be configured in bot.py
- ?leaderboard ## Leaderboard command, Lists out the users that have interacted with the bot and puts them in order