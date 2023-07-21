import requests
from bs4 import BeautifulSoup
import csv

#Set up CSV Stuff
csv_file = open('event_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Event Name', 'Date', 'Time', 'Link', 'Price'])

for pages in range(4, 5):
    # Define the URL of the Eventbrite page
    url = 'https://www.eventbrite.com/d/ny--new-york/ai/?page={}'.format(pages)
    print(url)

    # Send a GET request to the URL and retrieve the HTML content
    response = requests.get(url)
    html_content = response.content

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the event cards on the page

    #event_cards = soup.find_all('div', class_='eds-media-card-content__content')
    #event_cards = soup.find_all('div', class_='browse-cards-container')
    converted  = str(soup)
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

        r = requests.get(eventLink)
        pageHTML = r.text
        eventPrice = pageHTML[pageHTML.find('panelDisplayPrice":"')+20:pageHTML.find('panelDisplayPrice":"')+60]
        eventDateAndTimeString = pageHTML[pageHTML.find('Date and time</h3></div><p><span class="">')+42:pageHTML.find('Date and time</h3></div><p><span class="">')+90].split("<")[0]
        print(eventDateAndTimeString)
        if eventDateAndTimeString.find(",") != -1:
            eventTime = eventDateAndTimeString.split(",")[1].split("·")[1][:-4].split(" - ")
                

            
            if len(eventTime) == 1:
                eventTime.append("NA")


            if eventTime[0].find(':') != -1:
                if eventTime[0].find("am") != -1 and eventTime[0].find("pm") != -1:
                    eventTime[0] = str(int(eventTime[0].split(':')[0][:-2])/60 + int(eventTime[0].split(':')[0])) + eventTime[0].split(':')[1][-2:]
                else:
                    eventTime[0] = str(int(eventTime[0].split(':')[0])/60 + int(eventTime[0].split(':')[0]))
            if eventTime[1].find(':') != -1:
                eventTime[1] = str(int(eventTime[1].split(':')[1][:-2])/60 + int(eventTime[1].split(':')[0])) + eventTime[1].split(':')[1][-2:]
            if eventTime[0].find('am') == -1 and eventTime[0].find('pm') == -1:
                if eventTime[1][-2:] == "pm":
                    eventTime[0] = 12 + float(eventTime[0])
            elif eventTime[0].find("am"):
                eventTime[0] = float(eventTime[0][:-2])
            if eventTime[1].find("am") and eventTime[1] != "NA":
                eventTime[1] = 12 + float(eventTime[1][:-2])
            elif eventTime[1].find("pm") and eventTime[1] != "NA":
                eventTime[1] = 12 + float(eventTime[1][:-2])   
        else:
            eventTime = "Multi Day"     

        if eventPrice.find(' ') != -1 and eventPrice.find("From") == -1:
            eventPrice = eventPrice.split(" ")[0][1:]
        elif eventPrice.find("Free") == -1 and eventPrice.find("From") == -1:
            if eventPrice.count("$") != 2:
                eventPrice = eventPrice.split('"')[0][1:]
        elif eventPrice.find("Free") != -1:
            eventPrice = 0
        elif eventPrice.find("From") != -1:
            eventPrice = eventPrice.split('"')[0][6:]
       

        #Add the present event array to the entire array
        csv_writer.writerow([eventName, eventdate, eventTime, eventLink, eventPrice])

csv_file.close()