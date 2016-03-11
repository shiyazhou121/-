#coding=utf-8
import urllib2
import re
from lxml import etree
import requests
import sys
import time


def crawler(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
	for i in range(10):
		try:
			req = urllib2.Request(url, headers = headers)
			html = urllib2.urlopen(req).read()
			break
		except:
			if i<9:
				continue
			else:
				print 'error',str(i)
				logging.error("Has tried %d times to access url %s, all failed!", 10, url)
				break
	con = etree.HTML(html)
	return con, html

def download_1(url):
	con, html = crawler(url)
	time.sleep(0.5)
	req = re.compile(r'>(\d+)</a><a href="http://baa.bitauto.com/')
	a = req.findall(html)
	b = [int(i) for i in a]
	need = 0
	if len(b)==0:
		point = con.xpath('//div[@class="postslist_xh"]')
		need = len(point)
	else:
		need = max(b)*10
	return str(need)

def download_2(url):
	con, html = crawler(url)
	time.sleep(0.5)
	a = con.xpath("//div[@class='the_pages']/div/a[not(@class='next_on')]/text()")
	b = [int(i) for i in a]
	need = 0
	if len(b)==0:
		point = con.xpath('//div[@class="myquestion"]')
		need = 0
	else:
		need = max(b)*10
	return str(need)

def get_all(each):
	note = 'http://baa.bitauto.com/iyiche/ireplytopic-'+str(each)+'.html'
	replynote = 'http://baa.bitauto.com/iyiche/itopic-'+str(each)+'.html'
	tiwen = 'http://ask.bitauto.com/u'+str(each)+'/!ask/t0/'
	answei = 'http://ask.bitauto.com/u'+str(each)+'/!ask/t1/'
	need1 = download_1(note)
	need2 = download_1(replynote)
	need3 = download_2(tiwen)
	need4 = download_2(answei)
	return str(each)+'|'+need1+'|'+need2+'|'+need3+'|'+need4

def judge(num):
	url = 'http://i.yiche.com/u'+str(num)+'/!forum/topics/'
	con, html = crawler(url)
	p = con.xpath('//div[@class="mybox_page"]')
	if len(p)!=0:
		print num
		need = get_all(num).encode('utf-8')
		print need
		f = open('koubei+wenda.txt','a+')
		f.write(need+'\n')
		f.close()


if __name__=='__main__':
	num = 16789940
	for i in range(1,5000):
		try:
			judge(i)
		except Exception,e:
			print e
			f = open('koubei+wenda_error.txt','a+')
			f.write(str(i)+'\n')
			f.close()
			time.sleep(3)
