import sys
import urllib2

import yahoo.yql

class QueryError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
        
class StockRetriever(yahoo.yql.YQLQuery):
    """A wrapper for the Yahoo! Finance YQL api."""
    
    HISTORICALURL = 'http://ichart.finance.yahoo.com/table.csv?s='
    RSSURL = 'http://finance.yahoo.com/rss/headline?s='
    FINANCETABLES = {'quotes': 'yahoo.finance.quotes',
                     'options': 'yahoo.finance.options',
                     'quoteslist': 'yahoo.finance.quoteslist',
                     'sectors': 'yahoo.finance.sectors',
                     'industry': 'yahoo.finance.industry'}
                     
    def __init__(self):
        super(StockRetriever, self).__init__()

    def __format_symbol_list(self, symbolList):
		return ",".join(["\""+stock+"\"" for stock in symbolList])
	
    def __is_valid_response(self, response, field):
        return 'query' in response and 'results' in response['query'] \
            and field in response['query']['results']
    
    def __validate_response(self, response, tagToCheck):
        if self.__is_valid_response(response, tagToCheck):
            quoteInfo = response['query']['results'][tagToCheck]
        else:
            if 'error' in response:
                raise QueryError('YQL query failed with error: "%s".' 
                    % response['error']['description'])
            else:
                raise QueryError('YQL response malformed.')
        return quoteInfo
        
    def get_current_info(self, symbolList, columnsToRetrieve='*'):
        """Retrieves the latest data (15 minute delay) for the 
        provided symbols."""
        
        columns = ','.join(columnsToRetrieve)
        symbols = self.__format_symbol_list(symbolList)

        yql = 'select %s from %s where symbol in (%s)' \
              %(columns, self.FINANCETABLES['quotes'], symbols)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'quote')
    
    def get_historical_info(self, symbol):
        """Retrieves historical stock data for the provided symbol.
        Historical data includes day open, close, high, low, volume,
        and adjusted close."""
        yql = 'select * from csv where url=\'%s\'' \
              ' and columns=\"Date,Open,High,Low,Close,Volume,AdjClose\"' \
               % (self.HISTORICALURL+symbol)
        results = super(StockRetriever, self).execute(yql)
        # delete first row which contains column names
        del results['query']['results']['row'][0]
        return results['query']['results']['row']
        
    
    def get_news_feed(self, symbol):
        """Retrieves the rss feed for the provided symbol."""
        
        feedUrl = self.RSSURL+symbol
        yql = 'select title, link, description, pubDate from rss where url=\'%s\'' % feedUrl
        response = super(StockRetriever, self).execute(yql)
        if response['query']['results']['item'][0]['title'].find('not found') > 0:
            raise QueryError('Feed for %s does not exist.' % symbol)
        else:
            return response['query']['results']['item']
        
    def get_options_info(self, symbol, expiration='', columnsToRetrieve ='*'):
        """Retrieves options data for the provided symbol."""
        
        columns = ','.join(columnsToRetrieve)
        yql = 'select %s from %s where symbol = \'%s\'' \
              % (columns, self.FINANCETABLES['options'], symbol)
        
        if expiration != '':
            yql += " and expiration='%s'" %(expiration)
        
        response = super(StockRetriever, self).execute(yql)
        print response
        return self.__validate_response(response, 'optionsChain')
        
    def get_index_summary(self, index, columnsToRetrieve='*'):
        columns = ','.join(columnsToRetrieve)
        yql = 'select %s from %s where symbol = \'@%s\'' \
              % (columns, self.FINANCETABLES['quoteslist'], index)
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'quote')
    
    def get_industry_ids(self):
        """retrieves all industry names and ids."""
        
        yql = 'select * from %s' % self.FINANCETABLES['sectors']
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'sector')
    
    def get_industry_index(self, id):
        """retrieves all symbols that belong to an industry."""
        
        yql = 'select * from %s where id =\'%s\'' \
              % (id, self.FINANCETABLES['industry'])
        response = super(StockRetriever, self).execute(yql)
        return self.__validate_response(response, 'industry')
        
if __name__ == "__main__":
    retriever = StockRetriever()
    try:
        #print retriever.getCurrentData(sys.argv[1:])
        print retriever.get_industry_ids()
        #print retriever.get_news_feed('yhoo')
    except QueryError, e:
        print e
        sys.exit(2)