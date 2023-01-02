import os
import re
import requests
import bs4

BOLD = '\033[1m'
ALPHA = '\033[7m'
END="\033[m"

def _set_config_() -> dict:
    '''
    Reads config.txt content and returns a dictionary with the configuration
    '''
    
    if not os.path.exists('results'):
        os.mkdir('results')

    with open('config.txt', 'r') as conffile:
        config = conffile.readlines()

    header = [config[0].split(':')[1][:-1], config[1].split(':')[1][:-1]]
    team = config[2].split(':')[1][:-1]

    return {
        'header': header,
        'team': team,
    }

def _get_soup_(path: str) -> bs4.BeautifulSoup:
    '''
    Obtains the BeatifulSoup object of a web page

    -> path: URL of the web page
    '''

    web = requests.get(path)
    soup = bs4.BeautifulSoup(web.text, 'lxml')

    return soup

def _str_coincidence_(base: str, lookfor: str, sep=' ') -> bool:
    '''
    Looks for coincidences in a pair of strings
    '''
    
    if lookfor in base: return True

    p = re.compile(re.sub('\s','|',lookfor), re.I)
    for s in base.split(sep):
        if re.match(p, s): return True
    
    return False

def _pop_error_(error: str, error_code: str=None ) -> None:
    '''
    Displays an error on screen
    '''

    print(f'{ALPHA}ERROR{f"(Code {error_code})" if error_code else ""}{END}{BOLD}: {error}{END}')