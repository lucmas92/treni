import calendar
import datetime
import time
from urllib import parse

import requests


class TrenoRepository:
    def __init__(self):
        self.base_url = "http://www.viaggiatreno.it/infomobilita/resteasy/viaggiatreno"
        pass

    def news(self):
        url = self.base_url + "/news/0/it"
        return requests.get(url).json()

    def regioneStazione(self, stazione):
        url = self.base_url + f"/regione/{stazione}"
        return requests.get(url).json()

    def dettaglioStazione(self, stazione, regione):
        url = self.base_url + f"/dettaglioStazione/{stazione}/{regione}"
        return requests.get(url).json()

    def elencoStazioniCitta(self, citta):
        url = self.base_url + f"/elencoStazioniCitta/{citta}"
        return requests.get(url).json()

    def elencoStazioni(self):
        stazioni = []
        # for page in range(22):
        for page in range(2):
            url = self.base_url + f"/elencoStazioni/{page}"
            stazioni.append(requests.get(url).json())
        return stazioni

    def dateTime(self):
        # Wed%20Jun%2008%202022%2021:03:34%20GMT+0200%20(Ora%20legale%20dell%E2%80%99Europa%20centrale)
        now = datetime.datetime.now()

        data =  parse.quote(now.strftime("%a %b %d %Y "))
        ora = now.strftime("%H:%M:%S")
        str = data + ora + parse.quote(" ") \
              + "GMT+0200" + parse.quote(" ") \
              + "(" + parse.quote("Ora legale dell’Europa centrale") + ")"
        return str

    def cercaTreno(self, num):
        url = self.base_url + f"/cercaNumeroTrenoTrenoAutocomplete/{num}"
        info = requests.get(url).text
        if "\n" in info:
            info = info.split("\n")[0]

        while " " in info:
            info = info.replace(" ", "")
        return info

    def andamentoTreno(self, treno):
        data = treno[treno.find("|") + 1:].split("-")
        url = self.base_url + f"/andamentoTreno/{data[1]}/{data[0]}/{data[2]}"
        return requests.get(url).json()

    def tratteTreno(self, treno):
        data = treno[treno.find("|") + 1:].split("-")
        url = self.base_url + f"/tratteCanvas/{data[1]}/{data[0]}/{data[2]}"
        return requests.get(url).json()

    def statistiche(self):
        ts = calendar.timegm(time.gmtime())
        url = self.base_url + f"/statistiche/{ts}"
        return requests.get(url).json()

    def partenze(self, stazione):
        url = self.base_url + f"/partenze/{stazione}/{self.dateTime()}"
        return requests.get(url).json()

    def arrivi(self, stazione):
        url = self.base_url + f"/arrivi/{stazione}/{self.dateTime()}"
        return requests.get(url).json()
