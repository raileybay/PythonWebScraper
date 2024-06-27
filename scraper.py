import requests
from bs4 import BeautifulSoup

#scraping logic
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get('https://quotes.toscrape.com', headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

#get all <h1> elements on the page
h1_elements = soup.find_all('h1')

quotes = []
quote_elements = soup.find_all('div', class_='quote')

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

#retrieve the page and initialize soup

#get the "Next ->" HTML element
next_li_element = soup.find('li', class_='next')

#if there is a next page to scrape
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True) ['href']

    #get the new page
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    #parse the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    #scraping logic...

    #look for the "Next ->" HTML element in the new page
    next_li_element = soup.find('li', class_='next')


