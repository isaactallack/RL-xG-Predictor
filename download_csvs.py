import csv
import os
import urllib.request
import time
import requests
from bs4 import BeautifulSoup

def delete_old_files():
  os.chdir(f'{os.getcwd()}')

  folder_path = 'csvs/'
  # delete all the files in the folder
  for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)
    try:
      if os.path.isfile(file_path):
        os.unlink(file_path)
    except Exception as e:
      print(e)

def dl(new_replay_ids):
  urls = [f'https://ballchasing.com/dl/stats/players/{id}/{id}-players.csv' for id in new_replay_ids]

  # Download and save the remaining URLs to files in the 'csvs' folder
  for i, url in enumerate(urls):
    print(f"Downloading csv file {i+1}...")
    response = urllib.request.urlopen(url)
    data = response.read()

    # Save the file as 'csvs/csv_<i>.csv'
    with open(f'csvs/csv_{i+1}.csv', 'wb') as output_file:
      output_file.write(data)

    time.sleep(5)