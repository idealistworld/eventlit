import requests
from bs4 import BeautifulSoup
import csv

#Set up CSV Stuff
csv_file = open('event_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Event Name', 'Date', 'Link'])

for pages in range(30):
    # Define the URL of the Eventbrite page
    url = 'https://www.eventbrite.com/d/ny--new-york/tech/?page={pages}'

    # Send a GET request to the URL and retrieve the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the event cards on the page

    #event_cards = soup.find_all('div', class_='eds-media-card-content__content')
    #event_cards = soup.find_all('div', class_='browse-cards-container')
    converted  = str(soup)
    csv_writer.writerow(soup)
    converted = converted.split('<script type="application/ld+json">')
    converted = converted[1:]

    for eventCode in converted:
        #Define and clean
        eventCode = eventCode.replace('"','')
        eventCodeArray = eventCode.split(',')
        
        #Add event name to array
        eventName = (eventCodeArray[2][5:])

        #Add date to array
        eventdate = (eventCodeArray[0][26:])
        
        #Add event link to array
        eventLink = (eventCodeArray[3][4:])
        
        #Add the present event array to the entire array
        csv_writer.writerow([eventName, eventdate, eventLink])

csv_file.close()

"""
eventCode = converted[0]
eventCode = eventCode.replace('"','')
print(eventCode)

eventCodeArray = eventCode.split(',')
print(eventCodeArray)
"""