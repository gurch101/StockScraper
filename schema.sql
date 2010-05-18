CREATE DATABASE stocks;

USE stocks;

CREATE TABLE stock (
 symbol varchar(10) NOT NULL,
 name varchar(32) NOT NULL,
 category varchar(16) NOT NULL,
 PRIMARY KEY (symbol)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
