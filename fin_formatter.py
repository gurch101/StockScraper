import datetime

def getFormattedSymbolList(symbols):
	return [symbol[0] for symbol in symbols]

def getFormattedYrStockResultSet(stockInfo):
	now = datetime.datetime.now()
	year = now.year
	if type(stockInfo) is not list:
		return [__getFormattedYrStockTuple(year, stockInfo)]
	formattedResults = [__getFormattedYrStockTuple(year, s) for s in stockInfo]
	return formattedResults

def __formatKey(key):
    return key[0].lower + key[1:]

def getFormattedDailyStockResultSet(stockInfo):
	today = datetime.date.today()
	date = today.isoformat()
	formattedResults = []
	for s in stockInfo:
	        row = {}
        for item in s.items():
	        row[__formatKey(item[0])] = item[1]
        row["theDate"] = date
        formattedResults.append(row)
	return formattedResults

def getFormattedFreqStockResultSet(stockInfo):
	now = datetime.datetime.now()
	timestamp = "%d-%d-%d %d:%d:00" %(now.year, now.month, now.day, now.hour, \
                __formatMinute(now.minute))
	if type(stockInfo) is not list:	
		return [__getFormattedFreqStockTuple(timestamp, stockInfo)]
	formattedResults = [__getFormattedFreqStockTuple(timestamp, s) \
                        for s in stockInfo]
	return formattedResults

def getFormattedStockResultSet(category, stocks):
	if type(stocks) is not list:
		return [__getFormattedStockTuple(category, stocks)]
	formattedResults = [__getFormattedStockTuple(category,s) for s in stocks]	
	return formattedResults

def __getFormattedYrStockTuple(year, s):	
	return (s['symbol'], year, \
			s['YearLow'], s['YearHigh'], \
			s['PriceEPSEstimateCurrentYear'], \
			s['PriceEPSEstimateNextYear'], \
			__expandValue(s['EBITDA']), 
			__expandValue(s['MarketCapitalization']),\
			s['EPSEstimateCurrentYear'], \
			s['EPSEstimateNextYear'], \
			s['EPSEstimateNextQuarter']) 

def __getFormattedDayStockTuple(date, s):
	return (s["symbol"], date, s["AverageDailyVolume"], \
			s["DaysLow"], s["DaysHigh"], s["Volume"], \
			s["ShortRatio"], s["OneyrTargetPrice"], s["Open"], \
			s["PreviousClose"], s["EarningsShare"], s["DividendShare"], \
			s["ChangeFromYearLow"], __remPcnt(s["PercentChangeFromYearLow"]), \
			s["ChangeFromYearHigh"], __remPcnt(s["PercebtChangeFromYearHigh"]), \
			s["FiftydayMovingAverage"], s["TwoHundreddayMovingAverage"], \
			s["ChangeFromTwoHundreddayMovingAverage"], \
			__remPcnt(s["PercentChangeFromTwoHundreddayMovingAverage"]), \
			s["ChangeFromFiftydayMovingAverage"], \
			__remPcnt(s["PercentChangeFromFiftydayMovingAverage"]), \
			s["PriceSales"], s["PERatio"], s["PEGRatio"])

def __getFormattedFreqStockTuple(timestamp, s):
	changePercentLow, changePercentHi = __parsePctRange(s["Change_PercentChange"])
	lastTradeTime = __parseTrade(s["LastTradeWithTime"]);
	return (s["symbol"], timestamp, s["Ask"], s["Bid"], s["AskRealtime"], \
		    s["BidRealtime"], changePercentLow, changePercentHi, s["Change"], \
 			s["ChangeRealtime"], s["BookValue"], lastTradeTime, s["Volume"])

def __getFormattedStockTuple(category, s):
	return (s['symbol'], s['Name'], category)

def __remPcnt(val):
	if val is None:
		return
	else:
		return val[:-1]

def __parseTrade(val):
	return val[val.find(">")+1:val.find("</b>")]	

def __parsePctRange(val):
	pctRange = (val[:val.find(" - ")], val[val.find("- ")+1:])
	if pctRange[0] == "N/A":
		pctRange = (None, None)
	return pctRange

def __expandValue(val):
	if val is None:
		return
	elif val[-1] == 'B':
		return float(val[:-1]) * 1000000000
	elif val[-1] == 'M':
		return float(val[:-1]) * 1000000
	elif val[-1] == 'K':
		return float(val[:-1]) * 100000
	else:
		return float(val)

def __formatMinute(val):
	if val >=15 and val <= 25:
		return 20
	elif val >= 35 and val <= 45:
		return 40
	else:
		return 00 
