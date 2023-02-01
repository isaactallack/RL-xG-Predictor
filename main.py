import discord
import asyncio
import time
import check_new_replays, download_csvs, create_frames, predict, poisson
import csv
from itertools import chain
import math

# Replace YOUR_TOKEN_HERE with your Discord bot token
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Flag to track whether the bot should be running
running = False
channel = None
total_games, total_wins, xW, tot_alt_xW, goals_for, goals_against, xG_for, xG_against, xMMR, real_mmr = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

def alt_xW_model(xG_for, xG_aga):
    gd = float(xG_for) - float(xG_aga)
    #return 1 / (1 + math.exp(-2.75 * (gd))) # BIN SIZE = 0.05
    #return 1 / (1 + math.exp(-3.21 * (gd+0.2))) # BIN SIZE = 0.2
    return 1.00 / (1 + math.exp(-3.06 * (gd + 0.28))) # BIN SIZE = 1

def att_def(goals_for, goals_against, xG_for, xG_against, total_games):
    return (goals_for-xG_for)/total_games, (xG_against-goals_against)/total_games

@client.event
async def test_loop():
    global running, total_games, total_wins, channel, channel_id, tot_alt_xW, goals_for, goals_against, xG_for, xG_against, xMMR, real_mmr
    start_date, existing_replays = check_new_replays.init()
    while running:
        # MOVE THIS LINE OUT OF THE LOOP
        #start_date, existing_replays = check_new_replays.init()
        time.sleep(3)
        # Check for new replays
        new_replay_ids, existing_replays = check_new_replays.get_new_replay_ids(start_date, existing_replays)

        model = 'xG_model.h5'

        if len(new_replay_ids) != 0:
            # Delete existing files in 'csvs' folder
            download_csvs.delete_old_files()
            # Download all new csvs
            download_csvs.dl(new_replay_ids)
            # Create dataframes from new replays
            create_frames.create_dfs()

            predict.predict(model, ['goals-a', 'goals conceded-a'], ['result', 'goals-a', 'goals conceded-a'])

            # open the CSV file
            with open('predictions.csv', 'r') as f:
                # use the csv.reader function to read the file
                reader = csv.reader(f)
                # create an empty list to store the data
                xG = []
                # iterate over the rows in the file
                for row in reader:
                    # append the row to the data list
                    row = list(map(float, row))
                    # append the row to the data list
                    xG.append(row)

            for result in xG:
                win = 0
                #alt_xW = alt_xW_model(result[4], result[5])
                alt_xW = poisson.calculate_win_probability(float(result[2]), float(result[3]))
                total_games += 1
                if float(result[0]) > float(result[1]):
                    win = 1
                    total_wins += 1
                tot_alt_xW += alt_xW

                goals_for += float(result[0])
                goals_against += float(result[1])
                xG_for += float(result[2])
                xG_against += float(result[3])
                xMMR += 18 * alt_xW - 9
                if win == 0:
                    real_mmr += -9
                else:
                    real_mmr += 9

                if win == 0:     
                    await channel.send(f"Game LOSS ({result[0]:.0f}-{result[1]:.0f}): expected win = {alt_xW:.2f}\r\nxG: {result[2]:.2f}-{result[3]:.2f}")
                else:
                    await channel.send(f"Game WIN ({result[0]:.0f}-{result[1]:.0f}): expected win = {alt_xW:.2f}\r\nxG: {result[2]:.2f}-{result[3]:.2f}")
                time.sleep(0.5)
        await asyncio.sleep(45)

@client.event
async def on_message(message):
    global running, total_games, total_wins, channel, channel_id, tot_alt_xW, goals_for, goals_against, xG_for, xG_against, xMMR, real_mmr
    if message.content.lower() == 'start':
        channel, channel_id = message.channel, message.channel.id
        await channel.send(f"Starting new session...")
        running = True
        await test_loop()
    elif message.content.lower() == 'stop':
        await channel.send(f"Session stopped.")
        att_perf, def_perf = att_def(goals_for, goals_against, xG_for, xG_against, total_games)
        await channel.send(f"Session record:\r\n{total_wins}/{total_games}. Expected no. of wins (xW) = {float(tot_alt_xW):.2f}.\r\n xG: {xG_for:.2f}-{xG_against:.2f}. Attacking luck = {att_perf:.2f}, defensive luck = {def_perf:.2f}\r\nxMMR = {xMMR:.2f}, real MMR = {real_mmr:.2f}")
        running = False

client.run('xxxxxxxxxx')
