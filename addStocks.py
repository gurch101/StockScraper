import sys
import getopt

import MySQLdb

import fin_formatter
import fin_db
from stockretriever import StockRetriever
from stockretriever import QueryError


def parseCategory(input):
	category = ''
	for option, arg in input:
		if option == '--cat':
			category = arg
	while not category:
		category = raw_input('Please enter category: ')
	return category

def getArgs():
	try:
		opt,stocks = getopt.getopt(sys.argv[1:], '', ['cat='])
		category = parseCategory(opt)		
	except getopt.error, msg:
		print('Usage: python addStock.py --cat=<category> <stock1 stock2 ..>')
		sys.exit(2)

	return (category, stocks)

def getStockInfo(category, stocks):
    retriever = StockRetriever(stocks, ['symbol', 'Name'])
    try:
        resultSet = retriever.execute()
    except QueryError, e:
        print e
        sys.exit(2)
    return fin_formatter.getFormattedStockResultSet(category, resultSet)

def addStocksToDb(formattedStocks):
	try:	
		conn = fin_db.getDBConnection()
		cursor = conn.cursor()
		cursor.executemany(
			"""INSERT INTO stock (symbol, name, category)
			values(%s,%s,%s)""",
			formattedStocks)
		cursor.close()
		conn.close()	
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(2)

if __name__ == "__main__":
    category, stocks = getArgs()
	
    stockInfo = getStockInfo(category, stocks)
    print "Retrieved stock data for %d symbols" % len(stockInfo)
        
    addStocksToDb(stockInfo)
    print "Added %d symbols to database" % len(stocks)
    print "done!"
