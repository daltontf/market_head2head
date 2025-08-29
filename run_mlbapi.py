import requests
import sqlite3
import datetime


def gatherAttendance(path, league):
  cur = db.cursor()

  cur.execute("SELECT COMPLETE FROM fetches.FETCHES WHERE PATH = ?", [path])

  query_result = cur.fetchall()
  if not query_result:
    cur.execute(f'INSERT INTO fetches.FETCHES (PATH, COMPLETE) VALUES (?, false)', [path])
    db.commit()      
  else:
    if query_result[0][0]: 
      print(path + " already fetched")
      return 

  response = requests.get("https://statsapi.mlb.com/" + path)

  data = response.json()

  dates = data['dates']
 
  # cycle through all the games in the week 
  for date in dates:
    for game in date["games"]:
      if game["gameType"] == "E":
        continue
      try:
        game_date = game['gameDate']
        name = f'{game["teams"]["away"]["team"]["name"]} at {game["teams"]["home"]["team"]["name"]}'
    
        venue = None
        try:  
          venue = game['venue']['name']
        except KeyError as ex:
          print(path)
          print(ex) 

        home_score = game["teams"]["home"]['score']
        away_score = game["teams"]["away"]['score']

        print(name)
         
        insert = cur.execute(
          f'INSERT INTO COMPETITIONS (COMPETITION_DATE, LEAGUE, TITLE, VENUE, AWAY_SCORE, HOME_SCORE) VALUES (?,?,?,?,?,?)',
          [game_date, league, name, venue, away_score, home_score]
        )

      except KeyError as ex:
        print(path)
        print(ex)
        continue  

  cur.execute("UPDATE fetches.FETCHES SET COMPLETE=true WHERE PATH = ?", [path])  

  db.commit()

# Open a SQLite database, stored in the file db.sqlite
db = sqlite3.connect('competitions.db')

# Read and execute the SQL query in ./sql/articles.sql
f = open("./sql/schema.sql")
db.cursor().executescript(f.read())
year=2024

gatherAttendance(f'api/v1/schedule/games/?sportId=11&startDate={year}-01-01&endDate={year}-12-31', "MiLB AAA") 
