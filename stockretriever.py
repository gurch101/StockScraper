import sys
import yahoo.yql

class QueryError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class StockRetriever(yahoo.yql.YQLQuery):
    """A wrapper for the Yahoo! Finance YQL api."""
    
    def __init__(self, symbolList, columnsToRetrieve='*'):
        super(StockRetriever, self).__init__()
        self.__formatSymbolList(symbolList)
        self.columns = ",".join(columnsToRetrieve)

    def __formatSymbolList(self, symbolList):
		self.stocks = ",".join(["\""+stock+"\"" for stock in symbolList])
	
    def __isValidResponse(self, response):
        return 'query' in response and 'results' in response['query'] \
            and 'quote' in response['query']['results']

    def execute(self):
        """Queries Yahoo Finance data table and returns a list containing one 
        dictionary per symbol"""
        yql = 'select '+self.columns+' from yahoo.finance.quotes where symbol \
		        in ('+self.stocks+')'
        response = super(StockRetriever, self).execute(yql)
        if self.__isValidResponse(response):
            quoteInfo = response['query']['results']['quote']
        else:
            if 'error' in response:
                raise QueryError('YQL query failed with error: "%s".' 
                    % response['error']['description'])
            else:
                raise QueryError('YQL response malformed.')
        return quoteInfo

if __name__ == "__main__":
    retriever = StockRetriever(sys.argv[1:])
    try:
        resultSet = retriever.execute()
    except QueryError, e:
        print e
        sys.exit(2)
    print resultSet
