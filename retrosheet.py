import requests
import zipfile
import io
import os
import csv
import sys
from datetime import datetime

leagues = {
    "AA": "American Association",
    "FL": "Federal League",
    "AL": "Major League Baseball",
    "NL": "Major League Baseball",
    "NL;AL": "Major League Baseball",
    "AL;NL": "Major League Baseball",
    "NAL": "Negro American League",
    "NN2": "Negro National League II",
    "EWL": "East-West League",
    "NSL": "Negro Southern League",
    "NNL": "Negro National League I",
    "ANL": "American Negro League",
    "ECL": "Eastern Colored League",
}

def download_and_unzip(url, extract_to='.'):
    """Downloads a zip file from a URL and extracts its contents."""

    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(extract_to)

csv_dir = './csv'
download_and_unzip('https://www.retrosheet.org/teams.zip', csv_dir)    
teams = {}

with open(f'{csv_dir}/teams.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
      try:
        if leagues[row[1]]:
          teams[row[0]] = f'{row[2]} {row[3]}'
          print(teams[row[0]])
      except KeyError as ex:
        print(row, file=sys.stderr)
        pass

download_and_unzip('https://www.retrosheet.org/ballparks.zip', csv_dir)    
ballparks = {}

with open(f'{csv_dir}/ballparks.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
      try:
          ballparks[row[0]] = row[1]
      except KeyError as ex:
        print(row, file=sys.stderr)


for year in list(map(str, range(1876, 1992))) + ["wc", "dv", "lc", "ws"]:
  csv_file = f'{csv_dir}/gl{year}.txt'
  if not os.path.exists(csv_file):
    download_and_unzip(f'https://www.retrosheet.org/gamelogs/gl{year}.zip', csv_dir)

  with open(csv_file) as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
      try:
        date = datetime.strptime(row[0], "%Y%m%d").strftime("%Y-%m-%d")
        league = leagues[row[4]]
        away_team = teams[row[3]].replace("'", "''")
        home_team = teams[row[6]].replace("'", "''")
        away_score = row[9]
        home_score = row[10]
        venue = ballparks[row[16]].replace("'", "''")
        attendence = row[17] if row[17] else "NULL"
   

        print(f'INSERT INTO COMPETITIONS (COMPETITION_DATE, LEAGUE, TITLE, AWAY_SCORE, HOME_SCORE, ATTENDANCE, VENUE)' 
          + f' VALUES (\'{date}\', \'{league}\', \'{away_team} at {home_team}\', {away_score}, {home_score}, {attendence},\'{venue}\');')
      
      except KeyError as ex:
        print(ex, file=sys.stderr)  