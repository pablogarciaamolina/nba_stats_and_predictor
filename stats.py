import requests
import pandas as pd
import json
from support.nba_team_report_pdf import PDF
from support.cons import RESULTS_PATH, YEAR, PLAYER_COLS, TEAMS_ID
from support.funcs import _set_config_, _pop_error_

PATH = RESULTS_PATH

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

    # *All teams DataFrame
    json = response[0].json()
    df1 = pd.DataFrame(json)
    df1.drop('OpponentStat', inplace=True, axis=1)

    # *Team DataFrame
    df2 = pd.DataFrame(response[2].json())
    
    return [df1, df2]

def load(df_list: list[pd.DataFrame], team: str, id: str, do_json: bool=False) -> None:

    all_df, team_df = df_list[0], df_list[1]
    team_df = team_df.loc[team_df.Team == id]
    team_df = team_df[PLAYER_COLS]


    # *All teams CSV
    with open(f'{PATH}/teams_stats_{YEAR}.csv', 'w') as file:
        file.write(all_df.to_string())

    # *Team CSV
    with open(f'{PATH}/{id}.csv', 'w', encoding='utf_8') as file:
        file.write(team_df.to_string())


    # *Team JSON
    if do_json:
        team_dict = all_df.loc[all_df.Name == team].to_dict()
        for key in team_dict:
            team_dict[key] = team_dict[key][0]
        with open(f"{PATH}/team.json", "w") as outfile:
            json.dump({team: team_dict}, fp=outfile, indent=4)

    # *Team PDF
    # A4 format
        # width: 210
        # height: 297
    pdf = PDF(unit='mm', format='A4', orientation='L')
    pdf.add_page()
    pdf.titles(team + ' ' + str(YEAR) + ' ' + 'report')
    pdf.df_in_pdf(team_df, id, PATH)
    pdf.output(f'{PATH}/{id}_report.pdf')

def main(header, name) -> None:
    '''
    Main function for obtaining the stats.
    '''
    try:
        id = TEAMS_ID[name]
    except Exception:
        id = None
        _pop_error_(f'no team named "{name}"')
    
    if id:
        resp_list = extract(header, id)
        df_list = transform(resp_list)
        load(df_list, name.strip(), id.strip())


if __name__ == '__main__':

    config = _set_config_()
    main(config['header'], config['team'])
    