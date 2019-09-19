import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import re
import html5lib
import time

def scrape():
    scrape_mars_news()
    scrape_mars_featured_image()
    scrape_mars_weather()
    scrape_mars_facts()
    scrape_mars_hemispheres()  

def scrape_mars_news():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    resp = requests.get(url)
    soup = bs(resp.text,'html.parser')

    results = soup.find_all('div', class_='slide')

    titles = []
    paragraphs = []

    for result in results:
        title = result.find_all('a')[1].text.strip()
        body = result.find('a').text.strip()
        titles.append(title)
        paragraphs.append(body)

    news = dict(zip(titles,paragraphs))
    return news
    

def scrape_mars_featured_image():
    executable_path={'executable_path':'/usr/local/bin/chromedriver'}
    browser=Browser('chrome',**executable_path, headless=True)
    url2='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html=browser.html
    soup2=bs(html,'html.parser')
    soup2.find('section', class_='centered_text').find('article')["style"]
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA01320-1920x1200.jpg'
    return {'featured_img':featured_image_url}


def scrape_mars_weather():
    executable_path={'executable_path':'/usr/local/bin/chromedriver'}
    browser=Browser('chrome',**executable_path, headless=True)
    browser.visit('https://twitter.com/marswxreport?lang=en')
    html3 = browser.html
    soup3=bs(html3, 'html.parser')
    #print(soup3.prettify())
    mars_weather = soup3.find_all('div', class_='js-tweet-text-container')[6].text.strip()
    return {'weather':mars_weather}


def scrape_mars_facts():
    executable_path={'executable_path':'/usr/local/bin/chromedriver'}
    browser=Browser('chrome',**executable_path, headless=True)
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    html_facts = browser.html
    tables=pd.read_html(html_facts)
    df=tables[0]
    return {'df':df}


def scrape_mars_hemispheres():
    executable_path={'executable_path':'/usr/local/bin/chromedriver'}
    browser=Browser('chrome',**executable_path, headless=True)   
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url) 
    hemis_html=browser.html
    hemis_soup=bs(hemis_html,'html.parser')

    hemis_names =[]
    for n in range(0,4):
        hemis= hemis_soup.find_all('h3')[n].text.strip()
        hemis_names.append(hemis)

    hemis_images = []

    for i in range(0,4):
        #click on hemisphere title
        browser.find_by_tag('h3')[i].click()
        time.sleep(1)
        
        #Enlarges image
        browser.find_by_text('Open')
        time.sleep(1)
        
        #Gets new html 
        html_hemispheres = browser.html
        soup_hemispheres = bs(html_hemispheres, 'html.parser')
        img = soup_hemispheres.find_all('img', class_='wide-image')[0]['src']
        hemis_images.append(img)
        
        #go back to original page
        browser.visit(hemis_url)
        time.sleep(2)

    hemisphere_image_urls = dict(zip(hemis_names,hemis_images))
        
    root_url = 'https://astrogeology.usgs.gov'
    hemisphere_image_urls = {}

    for h in range(0,4):
        hemisphere_image_urls.update({hemis_names[h]:root_url+hemis_images[h]})

    return hemisphere_image_urls