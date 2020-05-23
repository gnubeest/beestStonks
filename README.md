# beestStonks

## a plugin for Limnoria that fetches market info

### requires Python 3, Limnoria, a Finnhub API key, and requests


Still a work in progress, but mostly not broken.

Usage:
`stock <symbol>`
`stock <symbol.exchange>`
`stock <^index>`
`stock indices`

Exchange is optional, omitting it tends to lean toward US markets. Will do the
best it can to fetch things like ETFs, ADRs, and B/C stocks gracefully.

See `codes.txt` for useful symbols and exchanges.
