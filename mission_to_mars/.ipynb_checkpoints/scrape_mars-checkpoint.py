def scrape():
    pass


def scrape_mars_news():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    resp = requests.get(url)
    soup = bs(resp.text,'html.parser')