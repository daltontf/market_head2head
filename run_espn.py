import requests
import sqlite3
import datetime

leagues = [
  ("usa.1", 2001),
  ("usa.usl.1", 2008),
  ("ger.1", 2000),
  ("ger.2", 2006),
  ("aut.1", 2006),
  ("eng.1", 2001),
  ("eng.2", 2001),
  ("esp.1", 2000),
  ("por.1", 2006),
  ("ita.1", 2000),
  ("fra.1", 2001),
  ("ned.1", 2000),
  ("bel.1", 2006),
  ("den.1", 2006),
  ("swe.1", 2008),
  ("nor.1", 2008),
  ("rus.1", 2006),
  ("tur.1", 2006),
  ("ksa.1", 2022),
  ("mex.1", 2001),
  ("bra.1", 2006),
  ("arg.1", 2000),
  ("uefa.champions", 2001),
  ("uefa.europa.conf", 2021),
  ("conmebol.sudamericana", 2005),
  ("usa.nwsl", 2013),
  ("eng.w.1", 2011),
  ("club.friendly", 2008),
  ("ned.w.1", 2020),
  ("usa.nwsl.summer.cup", 2024),
  ("uefa.wchampions", 2019),
  ("uefa.europa", 2009),
  ("eng.3", 2001),
  ("eng.league_cup", 2001),
  ("eng.trophy", 2001),
  ("ger.super_cup", 2011),
  ("ger.dfb_pokal", 2006),
  ("uefa.super_cup", 2009),  
  ("aus.1", 2009),
  ("aus.w.1", 2019),
  ("jpn.1", 2006),
  ("usa.ncaa.m.1", 2014),
  ("usa.ncaa.w.1", 2005),
  ("usa.open", 2014),
  ("concacaf.leagues.cup", 2023),
  ("concacaf.champions_cup", 2007),
  ("concacaf.champions", 2008),
  ("concacaf.w.champions_cup", 2024),
  ("fifa.cwc", 2025),
]

def gatherAttendance(sport, league, date, query, first_year):
  if str(first_year) > date[0:4]:
    #print(f'{path} not yet {first_year}')
    return 
  
  path = f'apis/site/v2/sports/{sport}/{league}/scoreboard?dates={date}'
  
  response = requests.get("http://site.api.espn.com/" + path + "&" + query)

  data = response.json()

  try:  
    league = data['leagues'][0]['name']
  except KeyError as ex:
    print(path)
    print(ex) 
    return 

  events = data['events']
  print(f'{league} {len(events)}')
 
  if len(events) == 0:
    return

  cur = db.cursor()

  cur.execute("SELECT COMPLETE FROM fetches.FETCHES WHERE SPORT = ? AND LEAGUE = ? AND DATE = ?", [sport, league, date])

  query_result = cur.fetchall()
  if not query_result:
    cur.execute(f'INSERT INTO fetches.FETCHES (SPORT, LEAGUE, DATE, COMPLETE) VALUES (?, ?, ?, false)', [sport, league, date])
    db.commit() 
  else:
    if query_result[0][0]: 
      print(path + " already fetched")
      return 


  # cycle through all the games in the week 
  for event in events:
    # create a dict (game) with each game as a shortcut 
    # var date = Utilities.formatDate(new Date(games[i]['date']), Session.getScriptTimeZone(), "YYYY-MM-dd")
    try:
      competition_date = event['date']
      game = event['competitions'][0]
      name = event['name']

      attendance = None
      try:
        attendance = game['attendance']
      except KeyError as ex:
        print(path)
        print(ex)   
    
      venue = None
      try:  
        venue = game['venue']['fullName']
      except KeyError as ex:
        print(path)
        print(ex)        

      if game['competitors'][0]['homeAway'] == "home":
        home_score = game['competitors'][0]['score']
        away_score = game['competitors'][1]['score']
      else: 
        home_score = game['competitors'][1]['score']
        away_score = game['competitors'][0]['score']
         
      insert = cur.execute(
        f'INSERT INTO COMPETITIONS (COMPETITION_DATE, LEAGUE, TITLE, ATTENDANCE, VENUE, AWAY_SCORE, HOME_SCORE) VALUES (?,?,?,?,?,?,?)',
          [competition_date, league, name, attendance, venue, away_score, home_score]
      )   

    except KeyError as ex:
      print(path)
      print(ex)
      continue  

  cur.execute("UPDATE fetches.FETCHES SET COMPLETE=true WHERE SPORT = ? AND LEAGUE = ? AND DATE = ?", [sport, league, date])  

  db.commit()

# Open a SQLite database, stored in the file db.sqlite
db = sqlite3.connect('competitions.db')

# Read and execute the SQL query in ./sql/articles.sql
f = open("./sql/schema.sql")
db.cursor().executescript(f.read())
day = datetime.datetime(2025, 8, 10)
before_date = "20250901"

while 1:
  date = day.strftime("%Y%m%d")
  if date >= before_date:
    break

  print(date)

  for (league, first_year) in leagues:
    gatherAttendance("soccer", league, date,'limit=1000', first_year)
  
  # # TODO fix NCAA D1 have multiple days during bowl season = Also FCS vs FBS (need different script?)
  # gatherAttendance("football", "college-football", date,'limit=1000', first_year)
  # # #gatherAttendance(f'apis/site/v2/sports/football/college-football/scoreboard?dates={date}&groups=80','limit=1000', date, 1873) # 1873! 
  # # #gatherAttendance(f'apis/site/v2/sports/football/college-football/scoreboard?dates={date}&groups=81','limit=1000') # FCS
  # # #gatherAttendance(f'apis/site/v2/sports/football/college-football/scoreboard?dates={date}&groups=35','limit=1000') # Div II/III

  gatherAttendance("football", "nfl", date, 'limit=1000', 1933) #1933
  gatherAttendance("football", "cfl", date, 'limit=1000', 2021) # 2021
  gatherAttendance("football", "ufl", date, 'limit=1000', 2024) # 2024+
  # gatherAttendance("football", "xfl", date, 'limit=1000', 2020) # 2020, 2023
  gatherAttendance("baseball", "mlb", date, 'limit=1000', 1876) #1876
  gatherAttendance("hockey", "nhl", date, 'limit=1000', 1993) #1993
  gatherAttendance("basketball", "nba", date, 'limit=1000', 1947) #1947
  gatherAttendance("basketball", "wnba", date, 'limit=1000', 1997) #1997

  # # gatherAttendance(f'apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?dates={date}&groups=50','limit=1000', date, 2001) #2001
  # # gatherAttendance(f'apis/site/v2/sports/basketball/womens-college-basketball/scoreboard?dates={date}&groups=50','limit=1000', date, 2001) #2001
  gatherAttendance("volleyball", "womens-college-volleyball", date, 'limit=1000', 2011) #2011

  gatherAttendance("rugby", "289262", date, 'limit=1000', 2019)
  gatherAttendance("lacrosse", "pll", date, 'limit=1000', 2022)
  gatherAttendance("lacrosse", "nll", date, 'limit=1000', 2025)

  day = day + datetime.timedelta(days=1)
