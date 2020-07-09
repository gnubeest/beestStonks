# beestStonks

## a plugin for Limnoria that fetches market info

a work in progress, but should be somewhat useful and Not Broken™

### requires

Python 3, Limnoria, Requests, and a [Finnhub](https://finnhub.io) API key

### usage

```stock <symbol>```
```stock <symbol.exchange>```
```stock <^index>```
`stock` with no symbol will give you a summary of popular index prices.

Exchange is optional, omitting it tends to lean toward US markets. Will do the
best it can to fetch things like futures, ETFs, ADRs, OTCs, and B/C stocks
gracefully.

See `codes.txt` for useful symbols and exchanges.

```forex <amount> <from currency> <to currency```
Basic currency conversion based on current exchange rates. Accepts ISO 4217
currency codes.
