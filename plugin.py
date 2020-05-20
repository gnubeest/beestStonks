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

        bullet = " \x036•\x0f "

        try:
            comp_nm = "\x036" + (company['exchange']) + ":\x0f " + (
                company['name']) + " (" + (
                    company['ticker']) + ") "
        except KeyError:
            comp_nm = ""

        # workaround for US symbols with no company lookups
        # probably crashes if doing an actual .us lookup
        if comp_nm == "":
            payload = urllib.parse.urlencode({'token': token})
            ex_url = urllib.request.urlopen(
                "https://finnhub.io/api/v1/stock/symbol?exchange=US&%s"
                % payload)
            ex_sym = json.loads(ex_url.read().decode('utf-8'))
            for sym_ind in range(0, 20000):
                search_sym = ex_sym[sym_ind]['symbol']
                if search_sym == symbol:
                    comp_nm = "\x036" + (ex_sym[sym_ind]['description']) + (
                        "\x0f (" + search_sym + ") ")
                    break

        qu_cur = "{:.2f} ".format(quote['c'])
        #qu_open = "{:.2f}".format(quote['o'])
        qu_hi = "{:.2f}".format(quote['h'])
        qu_lo = "{:.2f}".format(quote['l'])
        #qu_pc = (quote['pc'])
        qu_ch = ((quote['c']) - (quote['pc']))
        qu_chst = "{:.2f}".format(qu_ch)
        if qu_ch > 0:
            ch_sym = "\x0303↑"
        elif qu_ch < 0:
            ch_sym = "\x0304↓"
        else:
            ch_sym = "\x0302→"
            qu_chst = "unch"

        irc.reply(comp_nm + qu_cur + ch_sym +
                  qu_chst.replace("-", "") + bullet + "Hi " + qu_hi +
                  " Lo " + qu_lo)


    stock = wrap(stock, ['somethingWithoutSpaces'])

Class = BeestStonks


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
