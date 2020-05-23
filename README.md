# beestStonks

## a plugin for Limnoria that fetches market info

a work in progress, but should be somewhat useful and Not Broken™

### requires

Python 3, Limnoria, Requests, and a [Finnhub](https://finnhub.io) API key

### usage

```stock <symbol>```
```stock <symbol.exchange>```
```stock <^index>```

`stock indices` will give you a summary of popular index prices.

Exchange is optional, omitting it tends to lean toward US markets. Will do the
best it can to fetch things like ETFs, ADRs, and B/C stocks gracefully.

See `codes.txt` for useful symbols and exchanges.

### todo

Will get around to crypto markets and easy access to futures eventually.
