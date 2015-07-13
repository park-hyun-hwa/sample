import os
import sys
import urllib2
import httplib
import time
conn = httplib.HTTPConnection("192.168.0.16")
data =''
co2 = ''
def getWebpage(url, referer=''):
    debug = 0
    if debug:
        return file(url.split('/')[-1], 'rt').read()
    else:
        opener = urllib2.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'),
            ('Referer', referer),
        ]
        return opener.open(url).read()

def getDataPage():
    return getWebpage('http://www.airkorea.or.kr/index')

    
def normailize(s):
    return s.replace('<td>','').replace('</td>','').replace(' ','')

def printUsing():
    print sys.argv[0], '<output file name>'

def getDatetime(buffers):
    return buffers.split('<p class="now_time">')[1].split('<strong>')[1].split('</strong>')[0]
    
def getDatablocks(buffers):
    a = buffers.split('<tbody id="mt_mmc2_10007">')[1]
    b = a.split('</tbody>')[0].replace('<tr>','').replace('</tr>','').replace('</td>','')
    r = ''
    for line in b.split('<td>'):
       if len(line) < 30:
           line = line.strip()
           r = r+line+' '
       else:
           line = line.strip()
           r = r+line+'\n'
    return r.split('\n')[1:-1]
    
if __name__ == '__main__':
  try:
    print getDataPage()
  except KeyboardInterrupt:
    pass
