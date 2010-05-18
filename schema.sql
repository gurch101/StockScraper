CREATE DATABASE stocks;

USE stocks;

CREATE TABLE stock (
 symbol varchar(10) NOT NULL,
 name varchar(32) NOT NULL,
 category varchar(16) NOT NULL,
 PRIMARY KEY (symbol)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE stock_daily (
 symbol varchar(15) NOT NULL,
 theDate date NOT NULL,
 averageDailyVolume int(11),
 daysLow decimal(8,2),
 daysHigh decimal(8,2),
 volume int(11),
 open decimal(8,2),
 previousClose decimal(8,2),
 earningsShare decimal(10,5),
 dividendShare decimal(10,5),
 percentChangeFromYearLow decimal(10,5),
 percentChangeFromYearHigh decimal(10,5),
 fiftydayMovingAverage decimal(10,5),
 twoHundreddayMovingAverage decimal(10,5),
 percentChangeFromTwoHundreddayMovingAverage decimal(10,5),
 percentChangeFromFiftydayMovingAverage decimal(10,5),
 PRIMARY KEY (symbol,theDate)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
