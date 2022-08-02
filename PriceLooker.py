from bs4 import BeautifulSoup
import requests
import csv
import time
import tkinter
import tkinter.messagebox

# Create the fake head to make amazon think that we are a legit browser
head = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 9.10; rv:69.0) Gecko/20100101 Firefox/68.0'}

# Read the CSV file
file = open("Links.csv")
csvreader = csv.reader(file)

# Skip the csv header
next(csvreader)

# Acquire all the csv data
rows = []
for row in csvreader:
    rows.append(row)

# Create the notify window
window = tkinter.Tk()
window.wm_withdraw()

while True:
    # For every row extract the URL and the price target
    for row in rows:

        # Extract the data
        URL = row[0]
        threshold = row[1]

        website = requests.get(URL, headers=head)
        beautifier = BeautifulSoup(website.content, "html.parser")
        # print(beautifier.prettify())

        # Find the actual title of the object
        title = beautifier.find(id="productTitle").get_text()

        # Find the div containing the price
        prices = beautifier.find(id="corePriceDisplay_desktop_feature_div")

        # Find the classes with the actual price inside
        price = prices.find_all("span", {"class": "a-offscreen"})[0]

        # Extract the text from the class
        price = str(price.get_text())

        # At this point we have the text with the object price and now it needs to be extracted in float form
        price = float(price[0: len(price) - 1].replace(",", "."))

        # Confront the prices
        if(price < float(threshold)):
            window.bell()
            tkinter.messagebox.showinfo(title=title, message=(
                "Is below the threshold! \nThe current price is: " + str(price) + "\nThe threshold price is: " + threshold))
    # Sleep for some time
    time.sleep(3600)
