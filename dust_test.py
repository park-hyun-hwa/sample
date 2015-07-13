import os
import sys
import urllib2
import httplib
import time
import datetime

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
    value=[]

    for line in b.split('<td>'):
       if len(line) < 30:
           line = line.strip()
           #line = line.split(' ')
           #print line
           #r = r+line+' '
           #print r
       else:
           line = line.strip()
           print line
           r = r+line+'\n'
           value.append(line)
    return value

def get_page():
    page = urllib2.urlopen("http://www.airkorea.or.kr/index")
    text = page.read()
    return text

def print_dust(value):
    print "seoul : "+value[1]
    print "busan : "+value[2]
    print "deagu : "+value[3]
    print "incheon : "+value[4]
    print "gwangju : "+value[5]
    print "daejeon : "+value[6]
	
if __name__ == '__main__':
  try:
    buffers = get_page()
    current_time = getDatetime(buffers)
    dust = getDatablocks(buffers)
    
    print datetime.datetime.today()
    print_dust(dust)
    
  except KeyboardInterrupt:
    pass
