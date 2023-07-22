import requests
import csv

url = 'https://www.eventbrite.com/d/ny--new-york/tech/?page=1'
r = requests.get(url)
pageHTML = r.text

csv_file = open('raw_data_swag.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(pageHTML)

with open('raw_data.txt', 'w') as f:
    f.write(pageHTML)