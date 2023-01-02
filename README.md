2/01/2023

# nba stats and predictor

All the information is extracted from https://www.api-basketball.com/ and https://www.sportytrader.es/

## stats.py

Code for obtaining useful data regarding any team of the NBA. The sats are from the 2022 season but it can be changed in /support/cons.py (not recommended, other years data has not been verified as updated).
Running this code will create a directory named 'results' where all the obtaines stats will be saved, as well as a report on a PDF format.

#### Read config.txt for proper use

## prediction.py

Code for obtaining a prediction of the next match result involving the selected team (if such information is avaliable).
Running this code will display a result on screen.

### Read config.txt for propper use

## config.txt

A .txt file containing the required credentials and the desired team.
- key:Ocp-Apim-Subscription-Key
- value: *
- team: (complete name of the team, see obtions avaliable on TEAMS)

** The value is the most important field. It is an individual private token required for having access to the data from https://www.api-basketball.com/. Thus, it is obtained creating an account. For more information visit: https://www.api-basketball.com/documentation

The values in the file must be sepparated by ':' with no space in between. A templae is provided.

## TEAMS

- Atlanta Hawks
- Brooklyn Nets
- Boston Celtics
- Charlotte Hornets
- Chicago Bulls
- Cleveland Cavaliers
- Dallas Mavericks
- Denver Nuggets
- Detroit Pistons
- Golden State Warriors
- Houston Rockets
- Indiana Pacers
- Los Angeles Clippers
- Los Angeles Lakers
- Memphis Grizzlies
- Miami Heat
- Milwaukee Bucks
- Minnesota Timberwolves
- New Orleans Pelicans
- New York Knicks
- Oklahoma City Thunder
- Orlando Magic
- Philadelphia 76ers
- Phoenix Suns
- Portland Trail Blazers
- San Antonio Spurs
- Sacramento Kings
- Toronto Raptors
- Utah Jazz
- Washington Wizards 
