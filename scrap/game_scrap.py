import pickle
from lxml import etree


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


from utils import parse_game_homepage

TOTAL_PAGE = 4

url = 'https://steamdb.info/stats/globaltopsellers/'

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install())
)

driver.get(url=url)

res = []

for _ in range(TOTAL_PAGE):
    page_source = driver.page_source
    games = etree.HTML(page_source).xpath('//*[@id="table-apps"]/tbody/tr')
    
    for game in games:
        id = game.attrib['data-appid']
        try:
            res.append(parse_game_homepage(id))
        except: pass
    
    driver.execute_script(
        'document.getElementsByClassName("paginate_button next")[0].click()'
    )


with open('game.pickle', 'wb') as handler:
    pickle.dump(res, handler)
