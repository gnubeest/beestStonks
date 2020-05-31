###
# Copyright (c) 2020, Brian McCord
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import requests

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('BeestStonks')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class BeestStonks(callbacks.Plugin):
    """Retrieves market data from Finnhub"""
    pass

    def stock(self, irc, msg, args, symbol):
        """[<symbol.exchange>]
            Get current share prices.
        """

        token = self.registryValue("finnhubKey")
        symbol = symbol.upper()
        bullet = " \x036•\x0f "

        # make silly summary of popular market indices
        if symbol == "INDICES":
            ind_list = ['^DJI', '^IXIC', '^GSPC', '^FTSE', '^GDAXI', '^N225',
                 '^HSI']
            ind_name = ['DJIA', 'NASDAQ', 'S&P', 'FTSE', 'DAX', 'Nikkei',
                'Hang Seng']
            ind_c_lst = []
            ind_pc_lst = []
            ind_string = ''
            for ind_get in ind_list:
                payload = {'symbol': ind_get, 'token': token}
                ind_fetch = requests.get('https://finnhub.io/api/v1/quote',
                    params=payload)
                ind_dec = ind_fetch.json()
                ind_c_lst.append(ind_dec['c'])
                ind_pc_lst.append(ind_dec['pc'])
            for ind_index in range(0, 7):
                qu_cur = "{:.0f} ".format(ind_c_lst[ind_index])
                qu_ch = ((ind_c_lst[ind_index]) - (ind_pc_lst[ind_index]))
                qu_chst = "{:.0f}".format(qu_ch)
                if qu_ch > 0:
                    ch_sym = ("\x0303▲" + qu_chst.replace("-", ""))
                elif qu_ch < 0:
                    ch_sym = ("\x0304▼" + qu_chst.replace("-", ""))
                else:
                    ch_sym = "\x0302▰unch"
                ind_string = (ind_string + bullet + "\x036" + ind_name[ind_index] +
                    "\x0f " + qu_cur + ch_sym)
            irc.reply("\x0303beestDex" + ind_string)
            return

        # match input with symbol, get company name
        payload = {'symbol': symbol, 'token': token}
        quote_url = requests.get('https://finnhub.io/api/v1/quote',
            params=payload)
        company_url = requests.get(
            'https://finnhub.io/api/v1/stock/profile2', params=payload)
        quote = quote_url.json()
        company = company_url.json()

        # separate symbol and exchange from input for display
        # also so workarounds don't break and for later features
        if symbol.rfind('.') != -1:
            sym_sep = symbol[:symbol.rfind('.')]
            exc_sep = symbol[(symbol.rfind('.') + 1):]
        else:
            sym_sep = symbol
            exc_sep = ""

        try:
            comp_nm = "\x036" + (company['exchange']) + ":\x0f " + (
                company['name']) + " (" + sym_sep + ")"
        except KeyError:
                # lame workaround to fetch market index names
                payload = {'exchange': 'indices', 'token': token}
                ex_url = requests.get(
                    'https://finnhub.io/api/v1/stock/symbol', params=payload)
                ex_sym = ex_url.json()
                try:
                    for sym_ind in range(0, 200):
                        search_sym = ex_sym[sym_ind]['symbol']
                        if search_sym == symbol:
                            comp_nm = "\x036" + (ex_sym[sym_ind]
                                ['description']) + "\x0f (" + symbol.replace(
                                "^", "") + ")"
                            break
                except IndexError:
                    # even lamer workaround for symbols with no company lookups
                    # (usually certain funds and B/C stocks)
                    if exc_sep == "":
                        exc_sep = "US"
                    payload = {'exchange': exc_sep, 'token': token}
                    ex_url = requests.get(
                        'https://finnhub.io/api/v1/stock/symbol',
                        params=payload)
                    ex_sym = ex_url.json()
                    try:
                        for sym_ind in range(0, 20000):
                            search_sym = ex_sym[sym_ind]['symbol']
                            if search_sym == sym_sep:
                                comp_nm = "\x036" + (ex_sym[sym_ind]
                                    ['description']) + (
                                    "\x0f (" + search_sym + ")")
                                break
                    except IndexError:
                            comp_nm = "\x036Special:\x0f " + symbol

        # format prices, calculate change since close
        try:
            qu_ch = ((quote['c']) - (quote['pc']))
        except KeyError:
            irc.reply("Error 02: Invalid or unknown symbol or exchange")
            return
        if quote['c'] < 1:
            qu_rnd = "{:.4f}"
        else:
            qu_rnd = "{:.2f}"
        qu_cur = (qu_rnd + " ").format(quote['c'])
        qu_chst = qu_rnd.format(qu_ch)
        qu_hi = qu_rnd.format(quote['h'])
        qu_lo = qu_rnd.format(quote['l'])
        qu_chpc = ((qu_ch / (quote['pc'])) * 100)
        if abs(qu_chpc) < 0.9:
            qu_chpcst = "{:.1f}".format(qu_chpc)
        else:
            qu_chpcst = "{:.0f}".format(qu_chpc)
        ch_pcren = (qu_chst + " (" +
            qu_chpcst + "%)").replace("-", "")
        if qu_ch > 0:
            ch_sym = "\x0303▲"
        elif qu_ch < 0:
            ch_sym = "\x0304▼"
        else:
            ch_sym = "\x0302▰unch"
            ch_pcren = ""
 
        # render final output
        irc.reply(comp_nm + bullet + qu_cur + ch_sym + ch_pcren + bullet +
            qu_lo + " - " + qu_hi)

    stock = wrap(stock, ['somethingWithoutSpaces'])

Class = BeestStonks


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
