'''
Script based on the sportytrader.es website
Obtains predictions for NBA matches
'''

import bs4
import support.funcs as f
from support.cons import PREDICTIONS_WEB_PATH_1, PREDICTIONS_WEB_PATH_2, BOLD, ALPHA, GREEN, END

def extraction_sportytraider(team_name: str, soup: bs4.BeautifulSoup) -> list[str]:
    '''
    Extracts NBA predictions from the soup the web page.
    Return in a list the prediction of the next match for the team regarded in team_name
    If the string is empty then the team_name is not valid or there's no such information avaliable
    
    Follow's this pattern for the extraction:

        - finds the <div> tag with id="1x2wrap" (contains predictions)
        - each of the <div> tags inside it are the NBA matches
        - find the one with the corresponding team
        - get the prediction list
    
    The result ,if possible, is a list such that:

        [ team(1), team(2), date, prediction element(1), X, prediction element(2) ]
    '''
    
    raw_match = None
    wrap = soup.find('div', attrs={'id': '1x2wrap'})

    # Each NBA match is a <di> tag with class='flex flex-col xl...primary-grayborder rounded-lg p-2 my-4
    class_attr_match = 'flex flex-col xl:flex-row justify-center items-center border-2 border-primary-grayborder rounded-lg p-2 my-4'
    class_attr_team_name = 'w-1/2 text-center break-word p-1 dark:text-white'
    for div in wrap.find_all('div', attrs={'class': class_attr_match}):

        # Take the one that corresponds with the provided team
        # The tags corresponding to the name of the teams involved in the match have the attribute class=class_attr_team_name
        teams_divs = div.find_all('div', attrs={'class': class_attr_team_name})
        for team in teams_divs:
            if not raw_match:
                if f._str_coincidence_(team.text.strip(), team_name):
                    raw_match = div

    if raw_match:
        # Get the raw prediction information from the match's associated <div> tag
        #   Add the teams
        extracted = [d.text.strip() for d in raw_match.find_all('div', attrs={'class': class_attr_team_name})]
        #   Add the date and expected result
        span_tags = raw_match.find_all('span')
        #   The date and the expectations are enclosed in the text and attrs of the span tags
        #   The date is the first span tag, the expected results are next
        #   From the date we want the text of the tag, form the espectations we want the class_ attr of the second
        #   and fourth tag, the third is just an X
        extracted.append(span_tags[0].text)
        extracted.append(span_tags[1].attrs['class'][7]) 
        extracted.append(span_tags[2].text) 
        extracted.append(span_tags[3].attrs['class'][7])
            
        return extracted
    else:
        return []

def transform_raw_prediction(raw: list[str]) -> dict:
    '''
    Transforms a prediction given by extraction_sportytrader().

    -> raw: the predicted results as a list such that:
    
        [ team(1), team(2), date, prediction element(1), X, prediction element(2) ]

        Where the prediction elements are str extracted from a class attr of the span tags.
        Each of them is associated to team. The <span> tag coloured as "green" is the one of the
        expected WINNER 
    '''

    prediction = {'teams': [raw[0], raw[1]], 'date': raw[2]}

    if f._str_coincidence_(raw[3], 'green'): winner = raw[0]
    else: winner = raw[1]
    
    prediction['winner'] = winner

    return prediction # * ??

def show_prediction(team_name: str, prediction: dict) -> None:
    '''
    Prints in terminal the result of a prediction

    -> team_name: name of the team required of prediction

    -> prediction: prediction formatted dictionary such that:
        {
            teams: [(1),(2)] # list of teams invoved in the match
            date: '...' # date of the game
            winner: '...'   # name of the predicted winner
        }
    '''
    
    print(f'\n\t\t\t{ALPHA}PREDICTION FOR NEXT NBA MATCH OF {team_name} ({prediction["date"]}){END}')
    print(f'\n\t\t\t\t{BOLD}{prediction["teams"][0]}  vs  {prediction["teams"][1]}{END}')
    print(f'\n Expected winner: {GREEN}{prediction["winner"]}{END}')

def main(team: str):
    '''
    Main function for obtaining the prediction.
    Searches in both possible URL's the information of the match.
    Shows the result on screen
    '''
    
    soup = f._get_soup_(PREDICTIONS_WEB_PATH_1)
    
    raw_prediction = extraction_sportytraider(team, soup)
    if raw_prediction == []:
        # Information about expectated results is divided in two independent html, with different URLs
        raw_prediction = extraction_sportytraider(team, f._get_soup_(PREDICTIONS_WEB_PATH_2))
    
    if raw_prediction:
        prediction = transform_raw_prediction(raw_prediction)
        show_prediction(team, prediction)
    else:
        f._pop_error_('unable to find a prediction')
        print(f'{BOLD}Either the result is not avaliable or no matches comming soon for this team{END}')

if __name__ == '__main__':

    config = f._set_config_()
    main(config['team'])    