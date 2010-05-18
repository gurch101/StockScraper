import MySQLdb

def getDBConnection():
	return MySQLdb.connect(host="host", user="user", \
           passwd="pass", db="stocks")

def getStockSymbols():
	conn = getDBConnection()
	cursor = conn.cursor()
	cursor.execute("select symbol from stock")
	rows = cursor.fetchall()
	cursor.close()
	conn.close()
	return rows
