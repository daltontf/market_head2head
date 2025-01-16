import sys
import itertools

team_clauses = {
    "ATL": (["Atlanta"],[]),
    "AUS": (["Austin"],[]),
    "ANA": (["Anaheim"],[]),
    "BAL": (["Baltimore"],[]),
    "BIR": (["Birmingham"],[]),
    "BOS": (["Boston", "New England"],[]),
    "BUF": (["Buffalo"],[]),
    "CAL": (["Calgary"],[]),
    "CHI": (["Chicago"],[]),
    "CIN": (["Cincinnati"],[]),
    "COL": (["Columbus", "Ohio"],[]),
#    "CAR": (["Carolina"],[]),  #More of designation than market since it is Raleigh and Charlotte
    "CLE": (["Cleveland", "Lake Erie"],[]),
    "CLT": (["Charlotte", "Carolina Panthers"],[]),
    "DAL": (["Dallas","Arlington"],[]),
    "DEN": (["Denver", "Colorado"],[]),
    "DET": (["Detroit", "Michigan"],[]),
    "EDM": (["Edmonton"],[]),
    "HOU": (["Houston"],[]),
    "IND": (["Indiana", "Indy"],[]),
    "JAX": (["Jacksonville"],[]),
    "KC" : (["Kansas City"],[]),
    "LA" : (["Los Angeles"],["Angels"]),
    "LOU": (["Louisville"],[]),
    "LV" : (["Vegas"],[]),
    "MEM": (["Memphis"],[]),
    "MIN": (["Minne","S&t%Paul"],[]),
    "MIA": (["Miami", "Florida"],[]),
    "MIL": (["Milwaukee", "Green Bay"],[]),
    "MON": (["Montreal"],[]),
    "NO" : (["New Orleans"],[]),
    "NSH": (["Nashville", "Tennessee"],[]),
    "NY" : (["New York", "Gotham"],[]),
    "NJ" : (["New Jersey"],[]),
    "OAK": (["Oakland", "California Golden"],[]),
    "OKC": (["Oklahoma City"],[]),
    "OMA": (["Omaha"],[]),
    "ORL": (["Orlando"],[]),
    "OTT": (["Ottawa"],[]),
    "PHI": (["Philadelphia"],[]),
    "PHX": (["Phoenix", "Arizona"],[]),
    "PIT": (["Pittsburgh"],[]),
    "POR": (["Portland"],[]),
    "RAL": (["Raleigh", "Carolina Hurricanes", "Durham"],[]),
#   "REG": (["Regina", "Saskat"],[]),
    "SAC": (["Sacramento"],[]),
    "SLC": (["Salt Lake", "Utah"],[]),
    "SA" : (["San Antonio"],[]),
    "SD" : (["San Diego"],[]),
    "SF" : (["San Fran", "Golden State"],[]),
    "SJ" : (["San Jose"],[]),
    "SEA": (["Seattle"],[]),
    "STL": (["St.%Louis", "Saint Louis"],[]),
    "TB" : (["Tampa"],[]),
    "TOR": (["Toronto"],[]),
    "VAN": (["Vancouver"],[]),
    "WAS": (["Washington", "D.C."],[]),    
    "WIN": (["Winnipeg"],[])
}

mode = "markdown"

extra_clause = " and league not like '%NCAA%'"

for team1, team1_clause in team_clauses.items():
  if len(sys.argv) > 1 and team1 != sys.argv[1]: continue
  for team2, team2_clause in team_clauses.items():
    if len(sys.argv) > 2 and team2 != sys.argv[2]: continue
    if team1 == team2: continue
    if len(sys.argv) == 1 and team1 > team2: continue
    clauses = list(itertools.product(team1_clause[0], team2_clause[0]))

    team1_home_clauses = " or ".join(list(map(lambda x: f"title like '%{x[1]}%at%{x[0]}%'" , clauses)))
    team2_home_clauses = " or ".join(list(map(lambda x: f"title like '%{x[0]}%at%{x[1]}%'" , clauses)))

    print(f"""
.mode {mode}
.headers on  
create temp table temp_table as select League as 'League',
       Title as 'Title',
       substr(min(Earliest), 0, 11) as 'Earliest',
       substr(max(Latest), 0, 11) as 'Latest',
       sum(results.'{team1} Wins') as '{team1} Wins',
       sum(results.'{team2} Wins') as '{team2} Wins',
       sum(results.Ties) as Ties 
from (select league, title,
    MIN(competition_date) as 'Earliest',
    MAX(competition_date) as 'Latest',
     Count(*) as '{team1} Wins',
     0 as '{team2} Wins',
     0 as 'Ties'
from COMPETITIONS 
where HOME_SCORE > AWAY_SCORE 
and ( {team1_home_clauses} )
{extra_clause}
group by league, title
union
select league, title,
    MIN(competition_date) as 'Earliest',
    MAX(competition_date) as 'Latest',
     0 as '{team1} Wins',
     Count(*) as '{team2} Wins',
     0 as 'Ties'
from COMPETITIONS 
where HOME_SCORE < AWAY_SCORE
and ( {team1_home_clauses} )
{extra_clause}
group by league, title
union
select league, title,
    MIN(competition_date) as 'Earliest',
    MAX(competition_date) as 'Latest',
    0 as '{team1} Wins',
    0 as '{team2} Wins',
    Count(*) as 'Ties'
from COMPETITIONS 
where HOME_SCORE = AWAY_SCORE 
and ( {team1_home_clauses} )
{extra_clause}
group by league, title
union
select league, title,
    MIN(competition_date) as 'Earliest',
    MAX(competition_date) as 'Latest',
    0 as '{team1} Wins',
    Count(*) as '{team2} Wins',
    0 as 'Ties'
from COMPETITIONS 
where HOME_SCORE > AWAY_SCORE
and ( {team2_home_clauses} )
{extra_clause}
group by league, title
union
select league, title,
    MIN(competition_date) as 'Earliest',
    MAX(competition_date) as 'Latest',
    Count(*) as '{team1} Wins',
    0 as '{team2} Wins',
    0 as 'Ties'
from COMPETITIONS 
where HOME_SCORE < AWAY_SCORE
and ( {team2_home_clauses} )
{extra_clause}
group by league, title
union
select league, title, 
    MIN(competition_date) as 'Earliest',
    MAX(competition_date) as 'Latest',
    0 as '{team1} Wins',
    0 as '{team2} Wins',
    Count(*) as 'Ties'
from COMPETITIONS 
where HOME_SCORE = AWAY_SCORE 
and ( {team2_home_clauses} )
{extra_clause}
group by league, title
) as results group by league, title;
""")

    print(f"""
.print ""
.print {team1} - {team2} by Matchup:
select * from temp_table;""")

    print(f"""
.print ""
.print {team1} - {team2} by League:
select League, 
    sum("{team1} Wins") as '{team1} Wins',
    sum("{team2} Wins") as '{team2} Wins',
    sum("Ties") as 'Ties'
from temp_table group by League;""")

    print(f"""
.print ""
.print "{team1} - {team2} Total:"
select 
    sum("{team1} Wins") as '{team1} Wins',
    sum("{team2} Wins") as '{team2} Wins',
    sum("Ties") as 'Ties'
from temp_table;""")

    print(f"drop table temp_table;")
