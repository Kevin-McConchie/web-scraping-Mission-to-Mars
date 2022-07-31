# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_dict ={}

    # News section

    news_url = 'https://redplanetscience.com/'
    browser.visit(news_url)


    html = browser.html
    soup = bs(html, "html.parser") 

    # news_title = soup.find("div", class_="content_title")
    news_title = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[2]').text
    news_p = browser.find_by_xpath('//*[@id="news"]/div[1]/div/div[2]/div/div[3]').text
    
    # news_p = soup.find("div", class_="article_teaser_body")
    
    # # Quit the browser
    # browser.quit()

    # Featured image
    featured_url = 'https://spaceimages-mars.com/'
    browser.visit(featured_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url = featured_url + soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url

    # Mars facts to be scraped
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)

    table_df= pd.DataFrame(tables[0])
    table_df.columns = ["Description", "Mars", "Earth"]
    table_df.set_index("Description", inplace= True)


    mars_html_table = table_df.to_html(classes="table table-striped")

    #hemisphere images
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)

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

    browser.quit()
 # Mars 
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_html_table": str(mars_html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict

if __name__ == "__main__":

    print(scrape())