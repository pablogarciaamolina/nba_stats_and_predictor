import requests
from bs4 import BeautifulSoup
import lxml
from support.funcs import _set_config_
from support.cons import PREDICTIONS_WEB_PATH

web = requests.get(PREDICTIONS_WEB_PATH)
soup = BeautifulSoup(web.text, 'lxml')








if __name__ == '__main__':

    config = _set_config_()
    print(soup)