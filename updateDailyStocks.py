import sys

import MySQLdb

import fin_db
import fin_formatter
from stockretriever import StockRetriever
from stockretriever import QueryError

def getStockSymbols():
	try:
		symbols = fin_db.getStockSymbols()
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(2)
	return fin_formatter.getFormattedSymbolList(symbols)

def getDailyStockInfo(symbols):
    retriever = StockRetriever(symbols, ["symbol", "AverageDailyVolume", \
    "DaysLow", "DaysHigh", "Volume", "Open", "PreviousClose", "EarningsShare", \
    "DividendShare", "PercentChangeFromYearLow", "PercebtChangeFromYearHigh", \
    "ChangeFromFiftydayMovingAverage", "ChangeFromTwoHundreddayMovingAverage", \
    "FiftydayMovingAverage", "TwoHundreddayMovingAverage", \
    "PercentChangeFromFiftydayMovingAverage", \
    "PercentChangeFromTwoHundreddayMovingAverage"])
    try:	
        resultSet = retriever.execute()
    except QueryError, e:
        print e
        sys.exit(2)
    return fin_formatter.getFormattedDailyStockResultSet(resultSet)

def updateDBDailyStockInfo(formattedStockInfo):		
	try:	
		conn = fin_db.getDBConnection()
		cursor = conn.cursor()
		cursor.executemany(
			"""INSERT INTO stock_daily (symbol, theDate, averageDailyVolume, 
            daysLow, daysHigh, volume, open, previousClose, earningsShare, 
            dividendShare, percentChangeFromYearLow, percentChangeFromYearHigh, 
            fiftydayMovingAverage, twoHundreddayMovingAverage,
            percentChangeFromFiftydayMovingAverage,  
            percentChangeFromTwoHundreddayMovingAverage)
			values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
			formattedStockInfo)
		cursor.close()
		conn.close()	
	except MySQLdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(2)	

if __name__ == "__main__":
	symbols = getStockSymbols()
	print "Retrieved %d symbols" % len(symbols)

	stockInfo = getDailyStockInfo(symbols)
	print "Retrieved info for %d symbols" %len(stockInfo)
	
	updateDBDailyStockInfo(stockInfo)
	print "Updated stock_daily table"
	print "Done!"	
