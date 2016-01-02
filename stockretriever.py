#! /usr/bin/env python
#
# Download from https://github.com/gurch101/StockScraper
#
# See http://www.gurchet-rai.net/dev/yahoo-finance-yql for details
#
"""A wrapper for the Yahoo! Finance YQL api."""

import sys
import httplib
import urllib
import json


PUBLIC_API_URL = 'http://query.yahooapis.com/v1/public/yql'
DATATABLES_URL = 'store://datatables.org/alltableswithkeys'
HISTORICAL_URL = 'http://ichart.finance.yahoo.com/table.csv?s='
RSS_URL = 'http://finance.yahoo.com/rss/headline?s='
FINANCE_TABLES = {'quotes': 'yahoo.finance.quotes',
                  'options': 'yahoo.finance.options',
                  'quoteslist': 'yahoo.finance.quoteslist',
                  'sectors': 'yahoo.finance.sectors',
                  'industry': 'yahoo.finance.industry'}


def execute_yql_query(yql):
    """Returns the JSON response of the given YQL query. """

    conn = httplib.HTTPConnection('query.yahooapis.com')
    query_string = urllib.urlencode({
        'q': yql,
        'format': 'json',
        'env': DATATABLES_URL
    })
    conn.request('GET', PUBLIC_API_URL + '?' + query_string)
    return json.loads(conn.getresponse().read())


class QueryError(Exception):
    """Exception that's raised when YQL query execution fails. """
    pass


class NoResultsError(Exception):
    """Exception that's raised when the YQL response contains an empty
    resultset."""
    pass


def __format_symbol_list(symbols):
    return ",".join(["\"" + symbol + "\"" for symbol in symbols])


def __is_valid_response(response):
    return ('query' in response
            and 'results' in response['query']
            and 'error' not in response)


def __validate_response(response, tag):
    if not __is_valid_response(response):
        if 'error' in response:
            raise QueryError('YQL query failed with error: "%s".'
                             % response['error']['description'])
        raise QueryError('YQL response malformed.')
    elif (response['query']['results'] is None
          or tag not in response['query']['results']):
        raise NoResultsError('No results found.')
    return response['query']['results'][tag]


def get_current_info(symbol_list, columns='*'):
    """Retrieves the latest data (15 minute delay) for the
    provided symbols."""

    columns = ','.join(columns)
    symbols = __format_symbol_list(symbol_list)

    yql = ('select %s from %s where symbol in (%s)'
           % (columns, FINANCE_TABLES['quotes'], symbols))
    response = execute_yql_query(yql)
    return __validate_response(response, 'quote')


def get_historical_info(symbol, from_dt=None, to_dt=None):
    """Retrieves historical stock data for the provided symbol.

    Historical data includes date, open, close, high, low, volume,
    and adjusted close."""

    if from_dt is None or to_dt is None:
        date_string = ''
    else:
        date_string = ('&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv' %
                       (from_dt.month-1, from_dt.day, from_dt.year,
                        to_dt.month-1, to_dt.day, to_dt.year))

    yql = ('select * from csv where url="%s"'
           ' and columns="Date,Open,High,Low,Close,Volume,AdjClose"' %
           (HISTORICAL_URL + symbol + date_string))
    response = execute_yql_query(yql)
    results = __validate_response(response, 'row')
    # delete first row which contains column names
    del results[0]
    return results


def get_news_feed(symbol):
    """Retrieves the rss feed for the provided symbol."""

    feed_url = RSS_URL + symbol
    yql = ('select title, link, description, pubDate '
           'from rss where url="%s"' % feed_url)
    response = execute_yql_query(yql)
    return __validate_response(response, 'item')


def get_industry_index(industry_id):
    """retrieves all symbols that belong to an industry."""

    yql = ('select * from %s where id =\'%s\'' %
           (FINANCE_TABLES['industry'], industry_id))
    response = execute_yql_query(yql)
    return __validate_response(response, 'industry')


if __name__ == "__main__":
    try:
        print get_current_info(sys.argv[1:])
        # print get_news_feed('yhoo')
    except QueryError, err:
        print err
        sys.exit(2)
