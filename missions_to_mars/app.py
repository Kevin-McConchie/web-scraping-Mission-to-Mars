# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template



app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)



# @app.route("/")
# def index():
#     listings = mongo.db.listings.find_one()
#     return render_template("index.html", listings=listings)


# @app.route("/scrape")
# def scraper():
#     listings = mongo.db.listings
#     listings_data = scrape_phone.scrape()
#     listings.update({}, listings_data, upsert=True)
#     return redirect("/", code=302)




def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_dict ={}

    # News section
    news = {}

    news_url = 'https://redplanetscience.com/'

    html = browser.html
    soup = bs(html, "html.parser") 

    news["title"] = soup.find("div", class_="content_title")
    news['teaser'] = soup.find("div", class_="article_teaser_body")
    
    # # Quit the browser
    # browser.quit()

    # Featured image
    featured_url = 'https://spaceimages-mars.com/'

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url = featured_url + soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url

    # Mars facts to be scraped
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)

    table_df= pd.DataFrame(tables[1])
    table_df.columns = ["Description", "Value"]
    table_df.set_index("Description")

    mars_html_table = table_df.to_html(classes="table table-striped")

    #hemisphere images
    hemisphere_url = 'https://marshemispheres.com/'
    # browser.visit(url)

    hemisphere_image_urls = []

    for i in range(1,5):
        x_path = f'//*[@id="product-section"]/div[2]/div[{i}]/div/a/h3'
        browser.find_by_xpath(x_path).click()
        
        
        title = browser.find_by_xpath('//*[@id="results"]/div[1]/div/div[3]/h2').text
        link =  browser.find_by_xpath('/html/body/div[1]/div/div[2]/div/ul/li[1]/a')['href']     
        
        post = {
        'title': title,
        'img_url': link,
        }
        
        hemisphere_image_urls.append(post)
        browser.back()


 # Mars 
    mars_dict = {
        "title": news["title"],
        "teaser": news['teaser'],
        "featured_image_url": featured_image_url,
        "fact_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict

if __name__ == "__main__":
    app.run(debug=True)