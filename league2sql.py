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

csv_dir = './csv'

teams = {}

with open(f'{csv_dir}/teams.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
      try:
        #if leagues[row[1]]:
        teams[row[0]] = f'{row[2]} {row[3]}'
          #print(teams[row[0]])
      except KeyError as ex:
        print(row, file=sys.stderr)
        pass

ballparks = {}

with open(f'{csv_dir}/ballparks.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
      try:
          ballparks[row[0]] = row[1]
      except KeyError as ex:
        print(row, file=sys.stderr)

with open(f'league.txt') as league:
   for line in league.readlines():
    date = datetime.strptime(line[0:8], "%Y%m%d").strftime("%Y-%m-%d")
    try:
      away_team = teams[line[24:27]]
      home_team = teams[line[29:32]]
      away_score = line[61:62]
      home_score = line[64:65]
      venue = ballparks[line[50:55]].replace("'", "''")
      attendance = row[128:133] if row[128:133] else "NULL"
   
      print(f'INSERT INTO COMPETITIONS (COMPETITION_DATE, LEAGUE, TITLE, AWAY_SCORE, HOME_SCORE, ATTENDANCE, VENUE) VALUES (\'{date}\', \'Negro Leagues\', \'{away_team} at {home_team}\', {away_score}, {home_score}, {attendance}, \'{venue}\');')
    except KeyError as ex:
        print(ex, file=sys.stderr)  