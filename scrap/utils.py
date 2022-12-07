from schema import Game
from lxml import etree
import re


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


homepage_route = 'https://steamdb.info/app/'

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install())
)


def parse_game_homepage(id):
    url = f'{homepage_route}{id}/'
    driver.get(url)
    page_source = etree.HTML(driver.page_source)
    

    __name = page_source.xpath('//h1[@itemprop="name"]/text()')[0]
    __developer = page_source.xpath('//td[text()="Developer"]/following-sibling::td/a')
    __publisher = page_source.xpath('//td[text()="Publisher"]/following-sibling::td/a')
    
    if len(__developer) == 1:
        __developer = __developer[0].xpath('text()')[0]
    else:
        __developer = [
            a.xpath('text()')[0] for a in __developer
        ]
        
    if len(__publisher) == 1:
        __publisher = __publisher[0].xpath('text()')[0]
    else:
        __publisher = [
            a.xpath('text()')[0] for a in __publisher
        ]
    
    
    __price = page_source.xpath('//tr[@class="table-prices-current"]/td[@data-cc="us"]/following-sibling::td[1]/text()')[0]
    __price = re.search(r'(\$\d*[.]*\d*).*', __price).group(1)
    
    
    __pic_url = page_source.xpath('//div[@class="js-open-screenshot-viewer"]/img')[0].attrib['src']
    
    __release_date = page_source.xpath('//td[text()="Release Date"]/following-sibling::td/text()')[0]
    # dash here is unicode U+2013
    __release_date = re.search(r'^(.*) –.*', __release_date).group(1)
    
    
    __user_tag = page_source.xpath('//*[@id="prices"]/a')
    __user_tag = [
        a.xpath('text()')[0] for a in __user_tag
    ]
    
    
    return Game(
        id = id, name = __name,  
        developer = __developer,  publisher = __publisher,
        release_date = __release_date,
        price = __price,  pic_url = __pic_url,
        user_tag = __user_tag
    )


if __name__ == '__main__':
    id = 239140
    res = parse_game_homepage(id)
    print(res)