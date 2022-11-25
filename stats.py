import requests
import pandas as pd
import json
from builtins.quick_pdf import PDF
from builtins.cons import PATH, YEAR, PLAYER_COLS


def _set_config_() -> dict:
    '''
    Reads config.txt content and returns a dictionary with the configuration
    '''
    
    with open('config.txt', 'r') as conffile:
        config = conffile.readlines()

    header = [config[0].split(':')[1][:-1], config[1].split(':')[1][:-1]]
    team = config[2].split(':')[1][:-1]
    team_id = config[3].split(':')[1][:-1]


    return {
        'header': header,
        'team': team,
        'ID': team_id
    }

def extract(header: list, id: str) -> list[requests.Response]:

    responses = []
    responses.append(requests.request(
        'GET', 
        f'https://api.sportsdata.io/v3/nba/scores/json/TeamSeasonStats/{str(YEAR)}', 
        headers={header[0]: header[1]}
        ))

    responses.append(requests.request(
        'GET', 
        f'https://api.sportsdata.io/v3/nba/scores/json/Players/{id}', 
        headers={header[0]: header[1]}
        ))

    responses.append(requests.request(
        'GET', 
        f'https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStats/{str(YEAR)}', 
        headers={header[0]: header[1]}
        ))
    
    
    return responses
    
def transform(response: list[requests.Response]) -> list[pd.DataFrame]:

    # All teams DataFrame
    json = response[0].json()
    df1 = pd.DataFrame(json)
    df1.drop('OpponentStat', inplace=True, axis=1)

    # Team DataFrame
    df2 = pd.DataFrame(response[2].json())
    
    return [df1, df2]

def load(df_list: list[pd.DataFrame], team: str, id: str, do_json: bool=False) -> None:

    all_df, team_df = df_list[0], df_list[1]
    team_df = team_df.loc[team_df.Team == id]
    team_df = team_df[PLAYER_COLS]


    # All teams CSV
    with open(f'{PATH}/teams_stats_{YEAR}.csv', 'w') as file:
        file.write(all_df.to_string())

    # Team CSV
    with open(f'{PATH}/{id}.csv', 'w', encoding='utf_8') as file:
        file.write(team_df.to_string())


    # Team JSON
    if do_json:
        team_dict = all_df.loc[all_df.Name == team].to_dict()
        for key in team_dict:
            team_dict[key] = team_dict[key][0]
        with open(f"{PATH}/team.json", "w") as outfile:
            json.dump({team: team_dict}, fp=outfile, indent=4)

    # Team PDF
    pdf_w = 210
    pdf_h = 297
    pdf = PDF(unit='mm', format='A4', orientation='L')
    pdf.add_page()
    pdf.titles(team + ' ' + str(YEAR) + ' ' + 'report')
    pdf.df_in_pdf(team_df, id)
    pdf.output(f'{PATH}/{id}_report.pdf')


if __name__ == '__main__':

    config = _set_config_()
    resp_list = extract(config['header'], config['ID'].strip())
    df_list = transform(resp_list)
    load(df_list, config['team'].strip(), config['ID'].strip())