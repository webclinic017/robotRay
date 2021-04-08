# -*- coding: utf-8 -*-

"""
Created on 07 05 2019

@author: camilorojas

Data Fetcher proxy for market data
Data Fetcher supports public datasources from Finviz and Yahoo. And in
v1 verson will support Interactive Brokers connectivity for data.

DataFetcher calls two different py files with the specific fetching logic
- rrDFPublic.py - will capture the public data sources
- rrDFIB.py - will connect and gather info from Interactive Brokers

"""

import sys
import os
import pandas as pd


class StockDataFetcher():
    # StockDataFetcher class

    def __init__(self, symbol):
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from rrlib.rrLogger import logger
        self.symbol = symbol
        self.log = logger()
        self.log.logger.debug("    Init Stock Data Fetcher "+str(symbol))
        # timeout import
        import configparser
        config = configparser.ConfigParser()
        config.read("rrlib/robotRay.ini")
        self.source = config.get('datasource', 'source')
        self.timeout = int(config['urlfetcher']['Timeout'])

    def getData(self):
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        self.log.logger.debug("    About to retreive "+self.symbol)
        if (self.source == "public"):
            from rrlib.rrDFPublic import StockDFPublic as sdfp
            df = sdfp(self.symbol).getData()
        elif(self.source == "ib"):
            # implement class for ib retreival
            df = pd.DataFrame()
        else:
            self.log.logger.error("    DataFetcher source error:"+self.source)
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        self.log.logger.debug("   Values loaded: \n"+str(df))
        self.log.logger.debug(
            "    DONE - Stock Data Fetcher "+str(self.symbol))
        return df

    def getIntradayData(self):
        self.log.logger.debug("    About to retreive "+self.symbol)
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        if(self.source == "public"):
            from rrlib.rrDFPublic import StockDFPublic as sdfp
            df = sdfp(self.symbol).getIntradayData()
            self.log.logger.debug("   Values loaded: \n"+str(df))
        elif(self.souce == "ib"):
            self.log.logger.debug("   Loading intraday from IB")
            # implement class for ib retreival
            df = pd.DataFrame()
        else:
            self.log.logger.error("   DataFetcher source error:"+self.source)
            df = pd.DataFrame()
        self.log.logger.debug(
            "    DONE - Stock Intraday Data Fetcher "+str(self.symbol))
        return df


class OptionDataFetcher():

    def __init__(self, symbol):
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from rrlib.rrLogger import logger
        self.symbol = symbol
        self.log = logger()
        self.log.logger.debug("    Init Option Data Fetcher for "+symbol)
        # timeout import
        import configparser
        config = configparser.ConfigParser()
        config.read("rrlib/robotRay.ini")
        self.timeout = int(config['urlfetcher']['Timeout'])
        self.source = config.get('datasource', 'source')

    # Strike int, month is int and the number of months after today
    def getData(self, month, strike):
        # https://finance.yahoo.com/quote/WDAY200117P00160000
        # Get the put value for specified month 3-8
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        if(self.source == "public"):
            from rrlib.rrDFPublic import OptionDFPublic as odfp
            df = odfp(self.symbol).getData(month, strike)
            self.log.logger.debug("   Values loaded: \n"+str(df))
        elif(self.souce == "ib"):
            self.log.logger.debug("   Loading intraday from IB")
            # implement class for ib retreival
            df = pd.DataFrame()
        else:
            self.log.logger.error("   DataFetcher source error:"+self.source)
            df = pd.DataFrame()
        return df
