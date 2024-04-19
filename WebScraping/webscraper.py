from io import StringIO
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
data = requests.get(standings_url) ## getting the html file of webpage
soup = BeautifulSoup(data.text, 'lxml')
table = soup.find('table', id='results2023-202491_overall')
standings = []
print(table)
for row in table.find('tbody').find_all('tr'):
    # Extract text from all the cells in the row
    row_data = [cell.text for cell in row.find_all(['th', 'td'])]
    standings.append(row_data)

print(standings)

# links = standings_table.find_all('a') ## only finds a tags from html text using find a tag
# links = [l.get("href") for l in links] ## grabbing all the href properties of all the a tags (previous line) ## this gets all the links to the stats of the teams in the standings table
# links = [l for l in links if '/squads' in l] ## filtering only for the href links that have '/squads' in it
# team_urls = [f"https://fbref.com{l}" for l in links] ## adding "https://fbref.com" before each link


# team_url = team_urls[0] ## getting url of one specific team
# data = requests.get(team_url) ## getting the html value of team url link
# html_content = StringIO(data.text) ## wrapping the html content in StringIO format
# matches = pd.read_html(html_content, match="Scores & Fixtures") ## reading the html content and finding content that has "Scores and Fixtures"

# soup = BeautifulSoup(data.text) ## gettings a new BeautifulSoup with new data
# links = soup.find_all('a') ## finding all the <a> tags in the html
# links = [l.get("href") for l in links] ## getting all the "href" values in the <a> tags
# links = [l for l in links if l and 'all_comps/shooting/' in l] ## getting all the href values with 'all_comps/shooting/'

# data = requests.get(f"https://fbref.com{links[0]}") ## getting the html file from shooting link
# shooting = pd.read_html(data.text, match="Shooting")[0] ## reading the html file to find shooting table
# shooting.columns = shooting.columns.droplevel() ## dropping the double index of shooting table

# team_data = matches[0].merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date") ## merging the shooting table with the matches table

# years = list(range(2022,2020, -1))
# all_matches = []
# standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
# for year in years:
#     data = requests.get(standings_url)
#     soup = BeautifulSoup(data.text, features="html.parser")
#     standings_table = soup.select('table.stats_table')[0] ## finds the first stats table from html file using css selector 'table.stats_table'
#     links = standings_table.find_all('a') ## only finds a tags from html text using find a tag
#     links = [l.get("href") for l in links] ## grabbing all the href properties of all the a tags (previous line) ## this gets all the links to the stats of the teams in the standings table
#     links = [l for l in links if '/squads' in l] ## filtering only for the href links that have '/squads' in it
#     team_urls = [f"https://fbref.com{l}" for l in links] ## adding "https://fbref.com" before each link
    
#     previous_season = soup.select("a.prev")[0].get("href")
#     standings_url = f"https://fbref.com/{previous_season}"

#     for team_url in team_urls:
#         team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")

#         data = requests.get(team_url) ## getting the html value of team url link
#         html_content = StringIO(data.text) ## wrapping the html content in StringIO format
#         matches = pd.read_html(html_content, match="Scores & Fixtures")[0] ## reading the html content and finding content that has "Scores and Fixtures"

#         soup = BeautifulSoup(data.text) ## gettings a new BeautifulSoup with new data
#         links = soup.find_all('a') ## finding all the <a> tags in the html
#         links = [l.get("href") for l in links] ## getting all the "href" values in the <a> tags
#         links = [l for l in links if l and 'all_comps/shooting/' in l] ## getting all the href values with 'all_comps/shooting/'
#         data = requests.get(f"https://fbref.com{links[0]}")
#         shooting = pd.read_html(data.text, match="Shooting")[0] ## reading the html file to find shooting table
#         shooting.columns = shooting.columns.droplevel() ## dropping the double index of shooting table
#         try:
#             team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date") ## merging the shooting table with the matches table
#         except ValueError:
#             continue

#         team_data = team_data[team_data["Comp"] == "Premier League"]
#         team_data["Season"] = year
#         team_data["Team"] = team_name
#         all_matches.append(team_data)
#         time.sleep(1) ## slowing down scraping so it doesn't crash the website
    

#     match_df = pd.concat(all_matches)
#     match_df.columns = [c.lower() for c in match_df.columns]




