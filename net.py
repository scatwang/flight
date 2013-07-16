
#coding: utf-8
import os,sys,json, platform, logging, datetime, urllib2, time,urllib
import zlib
urllib2.socket.setdefaulttimeout(3) 

default_opener = urllib2.build_opener()
default_header = {'Accept-Encoding':'gzip'}

def urlfetch(url, headers={}, data=None):
    headers.update(default_header)
    opener = default_opener

    # data如果是dict，自动urlencode
    if isinstance(data, dict):
        data = urllib.urlencode(data)

    req = urllib2.Request(url, data, headers)
    res = opener.open(req, timeout=5)
    html = res.read()

    if 'Content-Encoding' in res.headers and  res.headers['Content-Encoding'] == 'gzip':
        try:
            html = zlib.decompress(html, 16+zlib.MAX_WBITS);
        except:
            raise Exception('ungzip error')

    return html, res

