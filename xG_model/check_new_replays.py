import datetime, requests
from bs4 import BeautifulSoup
import time

uploader = "76561198021360335"

def get_replay_ids(url, debug = False):

    replays = []

    # Send a GET request to the URL and retrieve the HTML content
    response = requests.get(url)
    html = response.text
            
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')
    if debug == True:
        print(soup)
            
    # Find all `a` tags with the class `replay-link`
    replay_links = soup.find_all('a', class_='replay-link')

    # Print the URLs of the replay links
    for replay_link in replay_links:
        replay_id = replay_link['href'][8:]
        replays += [replay_id]

    return replays

def init():
    existing_replays = []

    # Get the current date
    start_date = datetime.datetime.now()
    # Used in testing to force a fake start date
    #start_date = datetime.datetime(2022, 12, 28)

    # Format the date in the desired format
    start_date = start_date.strftime("%Y-%m-%d")

    url = f"https://ballchasing.com/?uploader={uploader}&replay-after={start_date}&replay-before={start_date}"
    
    existing_replays = get_replay_ids(url)
    
    # Print the formatted date
    return start_date, existing_replays

def update(start_date):
    # Get the current date
    current_date = datetime.datetime.now()

    # Format the date in the desired format
    current_date = current_date.strftime("%Y-%m-%d")

    url = f"https://ballchasing.com/?uploader={uploader}&replay-after={start_date}&replay-before={current_date}"

    return get_replay_ids(url)

def get_new_replay_ids(start_date, existing_replays):
    updated_replays = update(start_date)

    # Convert the lists to sets and get the symmetric difference
    new_replays = list(set(existing_replays).symmetric_difference(set(updated_replays)))

    existing_replays = updated_replays
    
    # Return the replay IDs
    return new_replays, existing_replays