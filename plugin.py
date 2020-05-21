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

import urllib.request
import urllib.parse
import json
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

        if symbol == "INDICES":
            ind_list = ['^DJI', '^IXIC', '^GSPC', '^FTSE', '^GDAXI', '^N225', '^HSI']
            ind_name = ['DJIA', 'NASDAQ', 'S&P', 'FTSE', 'DAX', 'Nikkei', 'Hang Seng']
            ind_c_lst = []
            ind_pc_lst = []
            ind_string = ''
            for ind_get in ind_list:
                payload = urllib.parse.urlencode(
                    {'symbol': ind_get, 'token': token})
                ind_fetch = (urllib.request.urlopen(
                    "https://finnhub.io/api/v1/quote?%s" % payload))
                ind_dec = json.loads(ind_fetch.read().decode('utf-8'))
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
        try:
            payload = urllib.parse.urlencode(
                {'symbol': symbol, 'token': token})
            quote_url = (urllib.request.urlopen(
                "https://finnhub.io/api/v1/quote?%s" % payload))
            company_url = (urllib.request.urlopen(
                "https://finnhub.io/api/v1/stock/profile2?%s" % payload))
            quote = json.loads(quote_url.read().decode('utf-8'))
            company = json.loads(company_url.read().decode('utf-8'))
        except json.decoder.JSONDecodeError:
            irc.reply("Error 02: Invalid or unknown symbol or exchange")
            return

        # separate symbol and exchange from input
        # (so workarounds don't break and for later features)
        if symbol.find('.') != -1:
            sym_sep = symbol[:symbol.find('.')]
            exc_sep = symbol[(symbol.find('.') + 1):]
        else:
            sym_sep = symbol
            exc_sep = ""

        try:
            comp_nm = "\x036" + (company['exchange']) + ":\x0f " + (
                company['name']) + " (" + sym_sep + ")"
        except KeyError:
                # lame workaround to fetch market index names
                payload = urllib.parse.urlencode({'token': token})
                ex_url = urllib.request.urlopen(
                "https://finnhub.io/api/v1/stock/symbol?exchange=indices&%s"
                % payload)
                ex_sym = json.loads(ex_url.read().decode('utf-8'))
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
                    payload = urllib.parse.urlencode(
                        {'exchange': exc_sep, 'token': token})
                    ex_url = urllib.request.urlopen(
                        "https://finnhub.io/api/v1/stock/symbol?%s"
                        % payload)
                    ex_sym = json.loads(ex_url.read().decode('utf-8'))
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
        qu_cur = "{:.2f} ".format(quote['c'])
        #qu_open = "{:.2f}".format(quote['o'])
        qu_hi = "{:.2f}".format(quote['h'])
        qu_lo = "{:.2f}".format(quote['l'])
        #qu_pc = (quote['pc'])
        qu_ch = ((quote['c']) - (quote['pc']))
        qu_chpcst = "{:.0f}".format(((qu_ch / (quote['pc'])) * 100))
        qu_chst = "{:.2f}".format(qu_ch)
        if qu_ch > 0:
            ch_sym = ("\x0303▲" + qu_chst.replace("-", "") + " (" +
                qu_chpcst.replace("-", "") + "%)")
        elif qu_ch < 0:
            ch_sym = ("\x0304▼" + qu_chst.replace("-", "") + " (" +
                qu_chpcst.replace("-", "") + "%)")
        else:
            ch_sym = "\x0302▰unch"
 
        # render final output
        irc.reply(comp_nm + bullet + qu_cur + ch_sym + bullet +
            qu_lo + " - " + qu_hi)

    stock = wrap(stock, ['somethingWithoutSpaces'])

Class = BeestStonks


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
