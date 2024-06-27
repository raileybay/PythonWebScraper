import requests
from bs4 import BeautifulSoup
import csv

#scraping logic
def scrape_page(soup, quotes):
    #retrieving all the quote <div> HTML elements on the page
    quote_elements = soup.find_all('div', class_='quote')

    # iterating over the list of quote elements
    # to extract the data of interest and store it
    # in quotes
    for quote_element in quote_elements:
        #extract text of the quote
        text = quote_element.find('span', class_='text').text

        #extract author of the quote
        author = quote_element.find('small', class_='author').text

        #extract the tag <a> HTML elements related to the quote
        tag_elements = quote_element.select('.tags .tag')

        #store the list of tag strings in a list
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags) #merge the tags into a "A, B, ..., Z" string
            }
        )
#crawling logic
#URL of the home page of target website
base_url = 'https://quotes.toscrape.com'

# defining the User-Agent header to use in the GET request below
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
#retrieve the page and initialize soup
page = requests.get('https://quotes.toscrape.com', headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

#initializing the variable that will contain
#the list of all quote data
quotes = []

#scraping the home page
scrape_page(soup, quotes)

#get the "Next ->" HTML element
next_li_element = soup.find('li', class_='next')

#if there is a next page to scrape
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True) ['href']

    #get the new page
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    #parse the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    #scraping the next page
    scrape_page(soup, quotes)

    #look for the "Next ->" HTML element in the new page
    next_li_element = soup.find('li', class_='next')


#reading the "quotes.csv" file and creating it if not present
csv_file = open('quotes.csv', 'w', encoding ='utf-8', newline='')

#initializing the writer object to insert data in the CSV file
writer = csv.writer(csv_file)

#writing the header of the CSV file
writer.writerow(['Text', 'Author', 'Tags'])

#writing each row of the CSV
for quote in quotes:
    writer.writerow(quote.values())

#terminating the operation and releasing the resources
csv_file.close()
