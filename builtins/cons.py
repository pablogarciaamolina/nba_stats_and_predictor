import os, sys

if not os.path.exists('../results'):
    os.mkdir('../results')
PATH = 'results'

YEAR = 2022

PLAYER_COLS = [
    'Name',
    'Position',
    'Games',
    'TwoPointersMade',
    'ThreePointersMade',
    'Rebounds',
    'Assists',
    'PersonalFouls',
    'Points',
    ]