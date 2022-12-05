import os

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
    team_id = config[3].split(':')[1][:-1]


    return {
        'header': header,
        'team': team,
        'ID': team_id
    }