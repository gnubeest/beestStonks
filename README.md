# beestStonks

## a plugin for Limnoria that fetches market info

### requires Python 3, Limnoria, a Finnhub API key, and probably json


Still a work in progress, but mostly not broken.

Usage: `stock <symbol.exchange>`

Exchange is optional, omitting it tends to lean toward US markets. Will do the
best it can to fetch things like ETFs, ADRs, and B/C stocks gracefully.

List of exchange codes (subject to change):
```
"code":"mutualFund","currency":"USD","name":"US Mutual funds"
"code":"indices","currency":"","name":"World Indices"
"code":"US","currency":"USD","name":"US exchanges"
"code":"HM","currency":"EUR","name":"HANSEATISCHE WERTPAPIERBOERSE HAMBURG"
"code":"BD","currency":"HUF","name":"BUDAPEST STOCK EXCHANGE"
"code":"JO","currency":"ZAc","name":"JOHANNESBURG STOCK EXCHANGE"
"code":"SR","currency":"SAR","name":"SAUDI STOCK EXCHANGE"
"code":"JK","currency":"IDR","name":"INDONESIA STOCK EXCHANGE"
"code":"MX","currency":"MXN","name":"BOLSA MEXICANA DE VALORES (MEXICAN STOCK EXCHANGE)"
"code":"TA","currency":"ILa","name":"TEL AVIV STOCK EXCHANGE"
"code":"DB","currency":"AED","name":"DUBAI FINANCIAL MARKET"
"code":"F","currency":"EUR","name":"DEUTSCHE BOERSE AG"
"code":"RG","currency":"EUR","name":"NASDAQ OMX RIGA"
"code":"NZ","currency":"NZD","name":"NEW ZEALAND EXCHANGE LTD"
"code":"AX","currency":"AUD","name":"ASX - ALL MARKETS"
"code":"OL","currency":"NOK","name":"OSLO BORS ASA"
"code":"ME","currency":"RUB","name":"MOSCOW EXCHANGE"
"code":"LS","currency":"EUR","name":"NYSE EURONEXT - EURONEXT LISBON"
"code":"AT","currency":"EUR","name":"ATHENS EXCHANGE S.A. CASH MARKET"
"code":"BO","currency":"INR","name":"BSE LTD"
"code":"SG","currency":"EUR","name":"BOERSE STUTTGART"
"code":"L","currency":"GBP","name":"LONDON STOCK EXCHANGE"
"code":"T","currency":"JPY","name":"TOKYO STOCK EXCHANGE-TOKYO PRO MARKET"
"code":"SA","currency":"BRL","name":"Sao Paolo"
"code":"DE","currency":"EUR","name":"XETRA"
"code":"CR","currency":"","name":"CARACAS STOCK EXCHANGE"
"code":"TL","currency":"EUR","name":"NASDAQ OMX TALLINN"
"code":"BK","currency":"THB","name":"STOCK EXCHANGE OF THAILAND"
"code":"QA","currency":"QAR","name":"QATAR EXCHANGE"
"code":"SS","currency":"CNY","name":"SHANGHAI STOCK EXCHANGE"
"code":"SW","currency":"USD","name":"SWISS EXCHANGE"
"code":"AS","currency":"EUR","name":"NYSE EURONEXT - EURONEXT AMSTERDAM"
"code":"CN","currency":"CAD","name":"CANADIAN NATIONAL STOCK EXCHANGE"
"code":"VS","currency":"EUR","name":"NASDAQ OMX VILNIUS"
"code":"MI","currency":"EUR","name":"MARKET FOR INVESTMENT VEHICULES"
"code":"CO","currency":"DKK","name":"OMX NORDIC EXCHANGE COPENHAGEN A/S"
"code":"NE","currency":"CAD","name":"AEQUITAS NEO EXCHANGE"
"code":"PA","currency":"EUR","name":"NYSE EURONEXT - MARCHE LIBRE PARIS"
"code":"IS","currency":"TRY","name":"BORSA ISTANBUL"
"code":"KQ","currency":"KRW","name":"KOREA EXCHANGE (KOSDAQ)"
"code":"TW","currency":"TWD","name":"TAIWAN STOCK EXCHANGE"
"code":"DU","currency":"EUR","name":"BOERSE DUESSELDORF"
"code":"BA","currency":"ARS","name":"BOLSA DE COMERCIO DE BUENOS AIRES"
"code":"V","currency":"CAD","name":"TSX VENTURE EXCHANGE - NEX"
"code":"BE","currency":"EUR","name":"BOERSE BERLIN"
"code":"SI","currency":"USD","name":"SINGAPORE EXCHANGE"
"code":"MU","currency":"EUR","name":"BOERSE MUENCHEN"
"code":"TO","currency":"CAD","name":"TORONTO STOCK EXCHANGE"
"code":"VI","currency":"EUR","name":"WIENER BOERSE AG DRITTER MARKT (THIRD MARKET)"
"code":"IR","currency":"EUR","name":"IRISH STOCK EXCHANGE - ALL MARKET"
"code":"HE","currency":"EUR","name":"NASDAQ OMX HELSINKI LTD."
"code":"SZ","currency":"CNY","name":"SHENZHEN STOCK EXCHANGE"
"code":"BR","currency":"EUR","name":"NYSE EURONEXT - EURONEXT BRUSSELS"
"code":"MC","currency":"EUR","name":"BOLSA DE MADRID"
"code":"BC","currency":"COP","name":"BOLSA DE VALORES DE COLOMBIA"
"code":"KS","currency":"KRW","name":"KOREA EXCHANGE (STOCK MARKET)"
"code":"NS","currency":"INR","name":"NATIONAL STOCK EXCHANGE OF INDIA"
"code":"PA","currency":"EUR","name":"NYSE EURONEXT - EURONEXT PARIS"
"code":"SN","currency":"CLP","name":"SANTIAGO STOCK EXCHANGE"
"code":"WA","currency":"PLN","name":"WARSAW STOCK EXCHANGE/EQUITIES/MAIN MARKET"
"code":"IC","currency":"ISK","name":"NASDAQ OMX ICELAND"
"code":"HK","currency":"HKD","name":"HONG KONG EXCHANGES AND CLEARING LTD"
"code":"ST","currency":"SEK","name":"NASDAQ OMX NORDIC"
"code":"PR","currency":"CZK","name":"PRAGUE STOCK EXCHANGE"
"code":"KL","currency":"MYR","name":"BURSA MALAYSIA"
"code":"VN","currency":"VND","name":"Vietnam exchanges including HOSE, HNX and UPCOM"
```
