#!/usr/local/bin/python
#coding:utf-8
import sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'jtravel.settings'
import datetime, json, time, urllib2, logging, re, random
#import gevent, gevent.monkey
#gevent.monkey.patch_all()
import net
import BeautifulSoup
from jtravel import models

class Feeyo():
    @staticmethod
    def getAirlineList():
        r = []
        url = 'http://www.feeyo.com/flightsearch_number.htm'
        html, res = net.urlfetch(url)
        s = BeautifulSoup.BeautifulSoup(html)
        s = s.find('div', attrs={'class':'cityli'})
        l = s.findAll('a')
        for a in l:
            r.append(a.contents[0])
        return r

    @staticmethod
    def filterChinaAirlineCorporations(l):
        acs = set(map(lambda x: x.code, models.AirlineCorporation.objects.all()))
        r = filter(lambda x: x[:2] in acs, l)
        return r

    @staticmethod
    def getFlightInfo(code):
        def _parseAirportCode(s):
            url = s.find('a')['href']
            return url.split('/')[-1].split('.')[0]
        def _parseValidDate(s):
            return datetime.datetime.strptime("2013年"+s.encode('utf8'),"%Y年%m月%d日")

        url = 'http://www.feeyo.com/flight/num/%s.htm' % code
        html, res = net.urlfetch(url)
        s = BeautifulSoup.BeautifulSoup(html)
        s = s.find('table', {'id':'flighttab'})
        l = s.findAll('tr', bgcolor=re.compile("#.*") )
        r = []
        for a in l:
            tds = a.findAll('td')
            p = {
                'flight_no': tds[0].contents[2].contents[0],
                'is_codeshare':  u'共享' in tds[1].contents[0],
                'depart_time' : tds[2].contents[0],
                'depart_airport' : _parseAirportCode(tds[2]),
                'arrive_time' : tds[3].contents[0],
                'arrive_airport' : _parseAirportCode(tds[3]),
                'plane_model' : tds[4].contents[2].contents[0],
                'weekly_schedule' : tds[5].contents[0],
                'stop_count' : tds[6].text, #contents[0].__str__(),
                #'have_meal': u'配有餐食' in tds[7].contents[0]['alt'],
                'have_meal': len(tds[7].contents) > 0,
                'valid_begin': _parseValidDate(tds[8].contents[0].split(' - ')[0]),
                'valid_end': _parseValidDate(tds[8].contents[0].split(' - ')[1]),
            }
            r.append(p)
            
        return r


    @staticmethod
    def getAll():
        all_codes = Feeyo.getAirlineList()
        print len(all_codes)
        china_codes = Feeyo.filterChinaAirlineCorporations(all_codes)
        print len(china_codes)
        for c in china_codes:
            print c, ":"
            infos = Feeyo.getFlightInfo(c)
            Feeyo.saveAll(infos)
            time.sleep(random.randint(1,3))


    @staticmethod
    def saveAll(l):
        for p in l:
            airline_info = models.AirlineInfo(**p)
            airline_info.save()
            print "\t".join([p['flight_no'], p['depart_airport'], p['depart_time'], p['arrive_airport'],p['arrive_time'], p['plane_model'], p['weekly_schedule'], p['stop_count']])


if __name__ == "__main__":
    #l = Feeyo.getFlightInfo('CA907')
    #Feeyo.saveAll(l)
    Feeyo.getAll()
    #Feeyo.getFlightInfo('UO4708')
    #Feeyo.getFlightInfo('CA101')


