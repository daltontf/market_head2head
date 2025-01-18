import sys
import itertools

team_clauses = {
  "ATL": (["Atlanta"],[]),
  "AUS": (["Austin"],[]),
  "ANA": (["Anaheim", "Los Angeles Angels", "California Angels"],[]),
  "BAL": (["Baltimore"],[]),
  "BIR": (["Birmingham"],[]),
  "BOS": (["Boston", "New England"],[]),
  "BUF": (["Buffalo"],[]),
  "CAL": (["Calgary"],[]),
  "CHI": (["Chicago"],[]),
  "CIN": (["Cincinnati"],[]),
  "COL": (["Columbus", "Ohio"],[]),
#  "CAR": (["Carolina"],[]),  #More of designation than market since it is Raleigh and Charlotte
  "CLE": (["Cleveland", "Lake Erie"],[]),
  "CLT": (["Charlotte", "Carolina Panthers"],[]),
  "DAL": (["Dallas","Arlington", "Texas Rangers"],[]),
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
  "NY" : (["New York", "Gotham"],["Rochester"]),
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
# "REG": (["Regina", "Saskat"],[]),
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

mode = "html"

extra_clause = " and league not like '%NCAA%'"

for line in """<html><head>
<style>
select {
    font-size: 32;
}
body {
    background: #000
    color: #DDD
}
caption {
   font-weight: bold; 
   text-align: left;
   padding: 5px;
}
table, th, tr, td {
    border: 1px solid;
    border-collapse: collapse;
    padding: 5px;
}
</style>
<script lang="javascript">
var markets = {
    "ATL": ["Atlanta"],
    "AUS": ["Austin"],
    "ANA": ["Anaheim"],
    "BAL": ["Baltimore"],
    "BIR": ["Birmingham"],
    "BOS": ["Boston"],
    "BUF": ["Buffalo"],
    "CAL": ["Calgary"],
    "CHI": ["Chicago"],
    "CIN": ["Cincinnati"],
    "COL": ["Columbus"],
    "CLE": ["Cleveland"],
    "CLT": ["Charlotte"],
    "DAL": ["Dallas"],
    "DEN": ["Denver"],
    "DET": ["Detroit"],
    "EDM": ["Edmonton"],
    "HOU": ["Houston"],
    "IND": ["Indianapolis"],
    "JAX": ["Jacksonville"],
    "KC" : ["Kansas City"],
    "LA" : ["Los Angeles"],
    "LOU": ["Louisville"],
    "LV" : ["Las Vegas"],
    "MEM": ["Memphis"],
    "MIN": ["Minneapolis-St.Paul"],
    "MIA": ["Miami"],
    "MIL": ["Milwaukee"],
    "MON": ["Montreal"],
    "NO" : ["New Orleans"],
    "NSH": ["Nashville"],
    "NY" : ["New York"],
    "NJ" : ["New Jersey"],
    "OAK": ["Oakland"],
    "OKC": ["Oklahoma City"],
    "OMA": ["Omaha"],
    "ORL": ["Orlando"],
    "OTT": ["Ottawa"],
    "PHI": ["Philadelphia"],
    "PHX": ["Phoenix"],
    "PIT": ["Pittsburgh"],
    "POR": ["Portland"],
    "RAL": ["Raleigh"],
    "SAC": ["Sacramento"],
    "SLC": ["Salt Lake City"],
    "SA" : ["San Antonio"],
    "SD" : ["San Diego"],
    "SF" : ["San Francisco"],
    "SJ" : ["San Jose"],
    "SEA": ["Seattle"],
    "STL": ["St. Louis"],
    "TB" : ["Tampa"],
    "TOR": ["Toronto"],
    "VAN": ["Vancouver"],
    "WAS": ["Washington DC"],    
    "WIN": ["Winnipeg"]
}

function createMarketOption(abr) {
    option = document.createElement('option');
    option.setAttribute('value', abr);
    option.appendChild(document.createTextNode(markets[abr]));
    return option
}

function init() {
   let market1 = document.getElementById("market1")
   let market2 = document.getElementById("market2")
   for (let abr in markets) {
     market1.appendChild(createMarketOption(abr))
     market2.appendChild(createMarketOption(abr))
   }
   market1.selectedIndex = -1
   market2.selectedIndex = -1
   if (window.location.hash) {
    target = window.location.hash.substring(1)    
    document.getElementById(target).style.display = "block" 
    markets = target.split("v")   
    market1.value = markets[0];
    market2.value = markets[1];
}
}

function marketSelected(selectedSelect) {
   let market1 = document.getElementById("market1")
   let market2 = document.getElementById("market2")
   let otherSelect = selectedSelect == market1 ? market2 : market1
   if (selectedSelect.selectedIndex > -1) {
    if (otherSelect.selectedIndex > -1) {
        if (selectedSelect.value < otherSelect.value) {
            target = selectedSelect.value + \\"v\\" + otherSelect.value
        } else {
            target = otherSelect.value + \\"v\\" + selectedSelect.value   
        }   
        window.location.hash = target
        let divs = document.getElementsByTagName("DIV")
        for (i = 0; i < divs.length; i++) {
          divs[i].style.display = \\"none\\" 
        }
        hideAll()  
        document.getElementById(target).style.display = \\"block\\"
    }    
   }
}

function hideAll() {
  let divs = document.getElementsByTagName("DIV")
  for (i = 0; i < divs.length; i++) {
    divs[i].style.display = \\"none\\" 
  }
}

function reset() {
    let market1 = document.getElementById("market1")
    let market2 = document.getElementById("market2")
    market1.selectedIndex = -1
    market2.selectedIndex = -1

    hideAll()
}
</script>
</head>
<body onload="javascript:init()">
<table id="marketsSelects"></table>
    <tr>
        <td><select id="market1" onchange="marketSelected(this)"></select></td>
        <td><select id="market2" onchange="marketSelected(this)"></select></td>
        <td><button onclick="reset()">Reset</button>
    </tr>
</table>    
""".splitlines():
  print(f'.print {line}')

for team1, team1_clause in team_clauses.items():
  if len(sys.argv) > 1 and team1 != sys.argv[1]: continue
  for team2, team2_clause in team_clauses.items():
    if len(sys.argv) > 2 and team2 != sys.argv[2]: continue
    if team1 == team2: continue
    if len(sys.argv) == 1 and team1 > team2: continue
    clauses = list(itertools.product(team1_clause[0], team2_clause[0]))

    team1_home_clauses = " or ".join(list(map(lambda x: f"title like '%{x[1]}%at%{x[0]}%'" , clauses)))
    team2_home_clauses = " or ".join(list(map(lambda x: f"title like '%{x[0]}%at%{x[1]}%'" , clauses)))

    
    if team1_clause[1]:
        team1_home_clauses = "(" + team1_home_clauses + ") and (" + " or ".join(list(map(lambda x: f"title not like '%at%{x}%'" , team1_clause[1]))) + ")"
        team2_home_clauses = "(" + team2_home_clauses + ") and (" + " or ".join(list(map(lambda x: f"title not like '%{x}%at%'" , team1_clause[1]))) + ")"

    if team2_clause[1]:
        team2_home_clauses = "(" + team2_home_clauses + ") and (" + " or ".join(list(map(lambda x: f"title not like '%at%{x}%'" , team2_clause[1]))) + ")"
        team1_home_clauses = "(" + team1_home_clauses + ") and (" + " or ".join(list(map(lambda x: f"title not like '%{x}%at%'" , team2_clause[1]))) + ")"

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
.print <div id="{team1}v{team2}" style="display:none">   
.print <a name="{team1}v{team2}"><p>{team1} vs {team2}</p></a>
.print "<table><caption>{team1} - {team2} by Matchup:</caption>"
select * from temp_table;""")
    print(".print </table>")

    print(f"""
.print "<table><caption>{team1} - {team2} by League:</caption>"
select League, 
    sum("{team1} Wins") as '{team1} Wins',
    sum("{team2} Wins") as '{team2} Wins',
    sum("Ties") as 'Ties'
from temp_table group by League;""")
    print(".print </table>")

    print(f"""
.print "<table><caption>{team1} - {team2} Total:</caption>"
select 
    sum("{team1} Wins") as '{team1} Wins',
    sum("{team2} Wins") as '{team2} Wins',
    sum("Ties") as 'Ties'
from temp_table;""")

    print(f"drop table temp_table;")
    print(".print </table><hr/></div>")


print(".print </body></html>")