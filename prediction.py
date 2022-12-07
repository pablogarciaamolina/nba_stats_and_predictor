'''
Based on the sportytrader.es website
Obtains predictions for NBA matches
'''

import requests
import bs4
from support.funcs import _set_config_
from support.cons import PREDICTIONS_WEB_PATH, PREDICTION_KEYWORDS

web = requests.get(PREDICTIONS_WEB_PATH)
soup = bs4.BeautifulSoup(web.text, 'lxml')

def _match_tag_(tag: bs4.PageElement, keywords: list[str], feedback=False) -> bool or bs4.PageElement:
    '''
    Searches for matches between the tag_info and the keywords.
    Return True if there's any, else False.

    -> feedback: If True, returns the tag argument if there's a match. Default to False
    '''

    word = tag.__str__().lower()
    for k in keywords:
        if k.lower() in word: return True if not feedback else tag
    
    return False

def extract(team_name: str) -> list[str]:
    '''
    Extracts NBA predictions from the html of the web page.
    Return in a list the prediction of the next match for the team regarded in team_name
    If the string is empty then the team_name is not valid or thre's no such information avaliable
    '''

    # Obtain the tag with the predictions (<div> tag)
    for div_element in soup.find_all('div'):
        if div_element.h2 and _match_tag_(div_element.h2, PREDICTION_KEYWORDS):
            predictions_tag = div_element

    # From that <div> tag, find the <div> tag that contains the predictions needed
    for sub_div in predictions_tag.find_all('div')[::5]: #There's 5 <div> tags inside every div tag, we oly need the superior <div> tags
        
        united_span_string = ''
        for span_tag in sub_div.find_all('span'):
            united_span_string += span_tag.string.strip() + '|'
        
        prediction_string = _match_tag_(united_span_string, [team_name], feedback=True)

    prediction_list = prediction_string.split('|')[:-1] if prediction_string else []
    
    return prediction_list


if __name__ == '__main__':

    config = _set_config_()
    raw_prediction = extract(config['team'])

    print(raw_prediction)