#importing important libraries
import scrapy
import unicodedata

# Class used for scraping data from wepages
class TestSpider(scrapy.Spider):
    #name of my custom spider
    name = 'test'
    # allowed domain on which scraping needs to be done.
    allowed_domains = ['blue-tomato.com']
    # initial webpage url from which scraping starts 
    start_urls = ['https://www.blue-tomato.com/de-AT/products/categories/Snowboard+Shop-00000000/gender/boys--girls--men--women/']
	
    # custom settings written to save our scraped data into a blue_tomato csv file inside tmp folder
    custom_settings = {
            
    'FEED_URI' : 'tmp/blue_tomato.csv'
 
    }
    
    def parse(self, response):
        name = response.css('.name::attr(data-productname)').extract() # scraps name of each product
        brand = response.css('.name::attr(data-brand)').extract() # scraps brand name of each product
        sc_price = response.css('.price::text').extract() # scraps price of each product
        price = removechars(sc_price)
        
        img = response.css(".productimage img::attr(src)").extract() # scraps image url of each product
        img_url=[]
        for i in img:
            if i != 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=':
                img_url.append(i) 
                
        product_url = response.css('.name::attr(href)').extract() # scraps product url of each product
        
        # Merging all collected data in a zip file and yielding the scraped infprmation 
        for item in zip(name,brand,price,img_url,product_url):
           scraped_info = {
               'Product Name' : item[0],
               'Brand' : item[1],
               'Price' : item[2],
               'image_urls' : ["https:"+item[3]], #Set's the url for scrapy to download images
               'Product URL':"https://www.blue-tomato.com/"+item[4]
           }
           yield scraped_info
        
        # To navigate over multiple webpages, yielding url of next page and again scraping whole data of next page
        nextpage = response.css('.next.browse a::attr(href)').extract_first()
        np="https://www.blue-tomato.com"+nextpage
        yield scrapy.Request(np, callback=self.parse)
        
        return
    
    
# removechars() function is written to remove unwanted elements from the sc_price list and return a more precise price list     
def removechars(sc_price):
    tmp =[]
    for i in sc_price:
        i = i.strip()
        if i != "":
            tmp.append(i)
    temp=[]
    for i in tmp:
        clean_text = unicodedata.normalize("NFKD",i)
        temp.append(clean_text)
    return temp