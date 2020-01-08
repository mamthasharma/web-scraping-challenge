# importing dependencies same as  jupyter notebook

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from urllib.request import urlopen
import re

def scrape_all():
    #Set executable path  
    executable_path = {"executable_path": "chromedriver.exe"}

    # initialise browser 
    browser = Browser('chrome', **executable_path, headless=False)
    title,para = marsnews(browser)
    data ={
        "marsnewstitle": title,
        "marsnewspara": para,
        "marsimages": marsimages(browser),
        "marsweather":marsweather(browser),
        "marshemps":marshemisphere(browser),
        "marsfacts":marstable(browser)

    }
    return data

def marsnews(browser):
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)
    # convert html to browser object
    article = {}
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # search to find the first title and paragragh paraghaph using div tag
    news_title=soup.find("div", class_="content_title").text
    news_para=soup.find("div", class_="article_teaser_body").text
    # #print the results
    # print(news_title)
    # print(news_para)
    return news_title,news_para

def marsimages(browser):
    # visit url
    url2="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    # Go to 'FULL IMAGE' and click
    base_url = 'https://www.jpl.nasa.gov'
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    # Go to 'more info' and click
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    # Parse HTML with Beautiful Soup
    html=browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Scrape the URL
    img_url = soup.select_one('figure.lede a img').get("src")
    # concat the base url with the result url to get an absolute url
    featured_image_url = base_url + img_url
    return featured_image_url

def marsweather(browser):
    # visit url
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    # parse html with soup
    html=browser.html
    soup = BeautifulSoup(html, "html.parser")
    # find the tweet with text 'Mars Weather'
    mars_weather= soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    return mars_weather

def marstable(browser):
    # Visit url
    url4 = "https://space-facts.com/mars/"
    browser.visit(url4)
    # Parse html with soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # create table to real url
    fact_table=pd.read_html(url4)
    
    # change column names
    mars_facts_df=fact_table[0]
    mars_facts_df.columns=['Data Type','Mars']
    return mars_facts_df.to_html(classes = "table table-striped")

def marshemisphere(browser):
    url5= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    img_urls=[]
    # Get a list of all hemisphers
    links = browser.find_by_css("a.product-item h3")

    # Loop through the links to get to the href
    for i in range(len(links)):
        hemisphere={}
        
        browser.find_by_css("a.product-item h3")[i].click()
        
    #Get sample image anchor tag to extract the href
        sample_tag= browser.find_link_by_text('Sample').first
        hemisphere['img_url']=sample_tag['href']
    #Get title
        hemisphere['title']=browser.find_by_css("h2.title").text
    # Append hemisphere details to list
        img_urls.append(hemisphere)
    # Navigate back
        browser.back()
    return img_urls

if __name__ == "__main__":
    print(scrape_all())

    