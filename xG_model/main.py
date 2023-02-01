import discord
import asyncio
import time
import check_new_replays, download_csvs, create_frames, predict
import csv

# Replace YOUR_TOKEN_HERE with your Discord bot token
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Flag to track whether the bot should be running
running = False
total_games = 0
total_wins = 0
xW = 0
channel = None

'''
@client.event
async def on_ready():
    global channel
    channel_id = 390295707568963598
    channel = client.get_channel(channel_id)
'''

@client.event
async def test_loop():
    global running, total_games, total_wins, xW, channel, channel_id
    start_date, existing_replays = check_new_replays.init()
    while running:
        # MOVE THIS LINE OUT OF THE LOOP
        #start_date, existing_replays = check_new_replays.init()
        time.sleep(3)
        # Check for new replays
        new_replay_ids, existing_replays = check_new_replays.get_new_replay_ids(start_date, existing_replays)

        if channel_id == 1057951103431491666:
            model = 'isaac.h5'
        elif channel_id == 390295707568963598:
            model = 'shad.h5'

        if len(new_replay_ids) != 0:
            # Delete existing files in 'csvs' folder
            download_csvs.delete_old_files()
            # Download all new csvs
            download_csvs.dl(new_replay_ids)
            # Create dataframes from new replays
            create_frames.create_dfs()
            # Predict result
            predict.predict(model)

            # open the CSV file
            with open('predictions.csv', 'r') as f:
                # use the csv.reader function to read the file
                reader = csv.reader(f)
                # create an empty list to store the data
                results = []
                # iterate over the rows in the file
                for row in reader:
                    # append the row to the data list
                    results.append(row)

            for result in results:
                total_games += 1
                total_wins += int(result[0])
                xW += float(result[1])
                if int(result[0]) == 0:     
                    await channel.send(f"Game LOSS: expected win = {float(result[1]):.3f}")
                else:
                    await channel.send(f"Game WIN: expected win = {float(result[1]):.3f}")
                time.sleep(0.5)
        await asyncio.sleep(45)

@client.event
async def on_message(message):
    global running, total_games, total_wins, xW, channel, channel_id
    if message.content.lower() == 'start':
        channel, channel_id = message.channel, message.channel.id
        await channel.send(f"Starting new session...")
        running = True
        await test_loop()
    elif message.content.lower() == 'stop':
        await channel.send(f"Session stopped.")
        await channel.send(f"Session record:\r\n{total_wins}/{total_games}. Expected no. of wins (xW) = {float(xW):.2f}. Thanks for playing.")
        running = False

client.run('MTA1Nzc1NjU0MTk4MzQwMDAyNg.GWGCxe.jqt1srytsWXk6DHqhiDIHLRauwRA9aeocpdoDo')
