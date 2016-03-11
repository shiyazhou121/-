#coding=utf-8
import urllib2
from lxml import etree
import re
import codecs
import json
import time
import sys


def crawler(url):
	html = urllib2.urlopen(url).read()
	con = etree.HTML(html)
	return con, html

def clean_list(data):
	z = []
	for each in data:
		k = each.strip().replace('#*#',' ')
		z.append(k.replace(' ',''))
	return z

#处理列表数据
def deal_list(data):
	if len(data)==0:
		k = ''
	elif len(data) ==1:
		k = data[0].strip().replace('#*#',' ')
	else:
		z = clean_list(data)
		k = ' '.join(z)
	return k.encode('utf-8')


#处理单个数据
def deal_one(data):
	if len(data)==0:
		k = ''
	else:
		k = data[0].strip().replace('#*#',' ')
	return k.encode('utf-8')
	
#得到每种车系口碑的总页数
def get_num(url):
	html = urllib2.urlopen(url).read()
	req = re.compile(r'tags/%e7%bb%bc%e5%90%88/page(\d+)/')
	a = req.findall(html)
	b = [int(i) for i in a]
	if len(b)==0:
		return 1
	else:
		return max(b)

#得到评论的总页数
def get_num_pinglun(html):
	req = re.compile(r'#lastcomment">(\d+)</a>')
	a = req.findall(html)
	b = [int(i) for i in a]
	if len(b)==0:
		return 1
	else:
		return max(b) 

#得到每种车系第一页的汇总信息，返回成字典，包含（车名、排名、总分数、好印象、坏印象）
def get_first(url):
	con, html = crawler(url)
	name = deal_one(con.xpath('//h1/a/text()'))
	rank = deal_one(con.xpath('//strong[@class="s-t"]/text()'))
	score = deal_list(con.xpath('//p[@class="red_txt"]/text()'))
	good = deal_list(con.xpath('//div[@class="word_box"][1]/span/a/text()'))
	bad = deal_list(con.xpath('//div[@class="word_box"][2]/span/a/text()'))
	compete1 = clean_list(con.xpath('//ul[@class="pic_list"]//p/a/text()'))
	compete2 = clean_list(con.xpath('//ul[@class="pic_list"]//span[@class="fen"]/text()'))
	compete =str(zip(compete1, compete2))
	item = name.replace('#*#', ' ')+'#*#'+rank.replace('#*#', ' ')+'#*#'+score.replace('#*#', ' ')+'#*#'+good.replace('#*#', ' ')+'#*#'+bad.replace('#*#', ' ')+'#*#'+compete.replace('#*#', ' ')
	return item, name


def get_second_url(url):
	get_url = url + 'tags/%E7%BB%BC%E5%90%88/page1'#第一页的url
	num = get_num(get_url) #得到口碑总页数
	url_list = []
	for each in range(1,num+1):      #遍历这种车系的每一页
		each_url = url + 'tags/%E7%BB%BC%E5%90%88/page'+str(each)+'/'  #该页的url
		con, html = crawler(each_url)
		x = con.xpath('//em[@class="zuijia"]/../a/@href')
		y = con.xpath('//div[@class="titbox"]/a/@href')
		z = []
		for i in y:
			new_url = i
			for j in x:
				if(i==j):
					new_url = i+'&'
			z.append(new_url)
		url_list.extend(z)
	return url_list

def get_second(url, point1):
	url_list = get_second_url(url)
	content_second = []
	point2 = 1
	for each in url_list:
		print '第 %s 车系，第 %s 口碑..' %(point1 , point2)
		point2 = point2 + 1
		z = each.find('&')
		k = '0'
		if z>0:
			k = '1'
			each = each[:z]
		con, html = crawler(each)
		first = get_second_first(con, html)
		second = get_second_second(con, html)
		thrid = get_second_thrid(con, html)
		forth = get_second_forth(con, html, each)
		total = second+'&*&'+k+'&*&'+first+'&*&'+thrid+'&*&'+str(forth)
		content_second.append(total)
	return content_second


def get_second_first(con, html):
	name = deal_one(con.xpath('//div[@class="tit1"]/a/text()'))
	get_price = deal_one(con.xpath('//span[@class="red_bold"]/text()'))
	all_score = deal_one(con.xpath('//div[@class="big_start_box"]/strong/text()'))
	li = con.xpath('//ul/li')
	area = ''
	time = ''
	agency = ''
	waiguan = '0'
	neishi = '0'
	kongjian = '0'
	dongli = '0'
	caokong = '0'
	peizhi = '0'
	xingjiabi = '0'
	shushidu = '0'
	youhao = '0'
	for each in li:
		x1 = deal_one(each.xpath('span[1]/text()'))
		x2 = deal_one(each.xpath('span[2]/text()'))
		x3 = deal_one(each.xpath('span[@class="label"]/text()'))
		x4 = deal_one(each.xpath('div/span[2]/text()'))
		if x1 =='购车城市：':
			area = x2
		elif x1 =='上牌时间：':
			time = x2
		elif x1 =='经 销 商：':
			agency = x2

		if x3 =='外  观：':
			waiguan = x4
		elif x3 =='内  饰：':
			neishi = x4
		elif x3 =='空  间：':
			kongjian = x4 
		elif x3 =='动  力：':
			dongli = x4
		elif x3 =='操  控：':
			caokong = x4
		elif x3 =='配  置：':
			peizhi = x4 
		elif x3 =='性 价 比：':
			xingjiabi = x4
		elif x3 =='舒 适 度：':
			shushidu = x4
		elif x3 =='油  耗：':
			youhao = x4 
	first = name.replace('&*&',' ')+'&*&'+get_price.replace('&*&',' ')+'&*&'+area.replace('&*&',' ')+'&*&'+time.replace('&*&',' ')+'&*&'+agency.replace('&*&',' ')+'&*&'+all_score.replace('&*&',' ')
	second = waiguan+' '+neishi+' '+dongli+' '+caokong+' '+peizhi+' '+xingjiabi+' '+shushidu+' '+youhao
	return first+'&*&'+second

def get_second_second(con, html):
	koubei_time = deal_one(con.xpath('//p[@class="article-information"]/span[@class="time"]/text()'))
	author = deal_one(con.xpath('//span[@class="author"]/a/text()'))
	id1 = deal_one(con.xpath('//span[@class="author"]/a/@href'))
	start = id1.find('com/')
	end = id1.find('/', start+4)
	author_id = id1[start+4:end]
	second = koubei_time.replace('&*&',' ')+'&*&'+author.replace('&*&',' ')+'&*&'+author_id.replace('&*&',' ')
	return second

def get_second_thrid(con, html):
	youhao = ''
	dongli = ''
	xingjiabi = ''
	peizhi = ''
	caokong = ''
	kongjian = ''
	waiguan = ''
	shushidu = ''
	neishi = ''
	zongping = ''
	for i in range(1,23):
		k = i + 1
		name = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(i)+']/strong/text()'))
		if name == '油耗':
			youhao = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '动力':
			dongli = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '性价比':
			xingjiabi = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '配置':
			peizhi = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '操控':
			caokong = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '空间':
			kongjian = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '外观':
			waiguan = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '舒适度':
			shushidu = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '内饰':
			neishi = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/text()'))
		elif name == '总评':
			zongping = deal_list(con.xpath('//div[@class="article-contents"]/p['+str(k)+']/p/text()'))
	mark = deal_list(con.xpath('//div[@class="the_pages_tags"]/a/text()'))
	return youhao.replace('|',' ')+'|'+dongli.replace('|',' ')+'|'+xingjiabi.replace('|',' ')+'|'+peizhi.replace('|',' ')+'|'+caokong.replace('|',' ')+'|'+kongjian.replace('|',' ')+'|'+waiguan.replace('|',' ')+'|'+shushidu.replace('|',' ')+'|'+neishi.replace('|',' ')+'|'+zongping.replace('|',' ')+'|'+mark.replace('|',' ')


def get_second_forth(con, html, url):
	num = get_num_pinglun(html)
	comment = []
	for i in range(1,num+1):
		url1 = url +'page'+str(i)+'/'
		con1, html1 = crawler(url1)
		box = con1.xpath('//div[@class="content_box"]')
		for each in box:
			name = deal_one(each.xpath('div[@class="name"]/strong/a/text()'))
			id1 = deal_one(each.xpath('div[@class="name"]/strong/a/@href'))
			start = id1.find('com/')
			end = id1.find('/', start+4)
			comment_id = id1[start+4:end]
			time = deal_one(each.xpath('div[@class="name"]/span/text()'))
			content = deal_one(each.xpath('div[@class="content"]/p/text()'))
			a_con = name.replace('|',' ')+'|'+comment_id.replace('|',' ')+'|'+time.replace('|',' ')+'|'+content.replace('|',' ')
			comment.append(a_con)
	return comment


#得到全部车系的url
def get_url(num):
	all_url = []
	for i in range(1,num):
		url = 'http://koubei.bitauto.com/tree/xuanche/?page=%s' %str(i)
		con, html = crawler(url)
		need_url = con.xpath('//div[@class="title"]/a/@href')
		all_url.extend(need_url)
	return all_url


#保存成json文件
def save(data,name):
	reload(sys)
	sys.setdefaultencoding('utf-8')
	json.dump(data,open(name+'.json','w'),ensure_ascii= False)


if __name__=='__main__':
	car_url = get_url(68)
	print len(car_url)
	yiche_koubei = {}
	k = 1
	for each in car_url:
		try:
			print '第 %s 种车系' %str(k)
			first, name = get_first(each)
			second = get_second(each, k)
			xinxi = first+'#*#'+str(second)
			yiche_koubei.setdefault(name, xinxi)
		except Exception,e:
			print '第 %s 种车系 error' %str(k)
			print e
			f = open('koubei_error_v4.txt','a+')
			f.write(each+':'+str(k)+'\n')
			f.close()
		k += 1
		time.sleep(3)
	print 'download is over..'
	save(yiche_koubei,'yiche_koubei_v4')
	print 'all is over..'
