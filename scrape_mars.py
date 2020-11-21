from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    # apply code from mission_to_mars.ipynb
    browser = init_browser()

   # Scraping preparation and store data in dictionary
    get_mars_data = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    response= requests.get(url)
    soup = bs(response.text, 'html.parser')

    #Retrieve the latest subject and content from the Mars website
    news_title = soup.find('div', class_="content_title").find('a').text
    news_paragraph = soup.find('div', class_="rollover_description_inner").text
    print('Most Recent Nasa News Article...')
    print(f'Title: {news_title}')
    print(f'Substance: {news_paragraph}')

    # Push values to Mars dictionary
    get_mars_data['recent_news'] = news_title
    get_mars_data['recent_news_substance'] = news_paragraph

    # ## JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image here.

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Url we will be scraping images from
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    splint_url = base_url + soup.find('a', class_="button fancybox")["data-fancybox-href"]

    print(f"URL to Featured Nasa Image: {splint_url}")


    # ## Mars Facts
    # *Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # *Use Pandas to convert the data to a HTML table string.

    url = 'https://space-facts.com/mars/'
    # Read table data from url
    facts_table = pd.read_html(url)

    # Convert to dataframe
    mars_facts_df = facts_table[0]
    mars_facts_df.columns = ['Type', 'Measurement']
    mars_facts_df

    # create HTML table
    html_table = mars_facts_df.to_html(border=3)
    #Remove enter characters 
    get_mars_data['mars_facts_html'] = html_table.replace('\n', '')
    print(get_mars_data['mars_facts_html'])

    # ## Mars Hemispheres
    # *Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # *Use Pandas to convert the data to a HTML table string.

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = "https://astrogeology.usgs.gov"
    # Obtain the webpage
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    # Grab all image urls and append to list
    results = soup.find_all('a', class_="itemLink product-item")
    full_res_img_url = []
    for result in results:
        # Combine link and base url
        full_res_img_url.append(base_url + result['href'])
    
    print(full_res_img_url)

    #create a empty list for diction
    hem_img_urls = []
    base_url = 'https://astrogeology.usgs.gov'

    for url in full_res_img_url:
    
        # Obtain webpage from diff website
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
    
        #Retrieve url to full resolution image
        image_url = soup.find('div', class_="downloads").find('ul').find('li').find('a')['href']
    
        #Retrieve the subject
        title = soup.find('h2', class_="title").text
    
        #initial diction and put into list
        res_dict = { "title":title,"img_url": image_url }
        hem_img_urls.append(res_dict)
        print(title)
        print(image_url)
    
    print(hem_img_urls)
    get_mars_data['hemisphere_image_urls'] = hem_img_urls
    #print all data from diction 
    print(get_mars_data)

