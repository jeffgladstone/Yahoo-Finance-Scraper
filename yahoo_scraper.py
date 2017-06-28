
"""
    Filename: yahoo_scraper.py
    Author: Jeff Gladstone
    Date: 6/28/2017
    Description:
    This program parses HTML from Yahoo Finance
    to create a list of stocks with ticker, name and price.
    It uses tickers from an input file called "symbols.csv".
    It outputs results to an XML document called  "yahoo_output.xml".
"""

from lxml import html
import requests
import csv

# create list of tickers from input file 'symbols.csv'
tickers = list()
with open("symbols.csv", "rt") as f:
	reader = csv.reader(f, delimiter=' ')
	for row in reader:
		tickers.append(row[0])

# initialize two lists. 'prices' and 'names'
prices = list()
names = list()

# iterate through tickers and parse HTML to get price and name of stock
for ticker in tickers:
	url = 'https://finance.yahoo.com/quote/' + ticker
	page = requests.get(url)
	tree = html.fromstring(page.content)
	try:
		price = float(tree.xpath('//div[@id="quote-header-info"]//span[@data-reactid="36"]/text()')[0])
		price = '{0:.2f}'.format(price)
		name = tree.xpath('//div[@id="quote-header-info"]//h1/text()')[0]
		prices.append(price)
		names.append(name)

		print('Current price for ' + name + ' is: $' + str(price) + '.')
		print()
	except:
		print('Price not found for ' + ticker + '. Try again.')
		print()

# combine three existing lists into one single list of tuples
stocks = list(zip(tickers, names, prices))

# Write to output
with open("yahoo_output.xml", "w") as f:
	for stock in stocks:
		f.write("<stock>\n")
		f.write("\t<ticker>" + stock[0] + "</ticker>\n")
		f.write("\t<name>" + stock[1] + "</name>\n")
		f.write("\t<price>" + stock[2] + "</price>\n")
		f.write("</stock>\n")