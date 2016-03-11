#coding = utf-8
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def change(data):
	all_need = {}
	for name,other in data.iteritems():

		name = name.encode('utf-8')
		second = {}

		all_score = change_list(other['score'])
		good = change_list(other['good'])
		bad = change_list(other['bad'])
		rank = other['rank'].encode('utf-8')

		second['all_score'.encode('utf-8')] = all_score
		second['good'.encode('utf-8')] = good
		second['bad'.encode('utf-8')] = bad
		second['rank'.encode('utf-8')] = rank

		koubei = []
		for each in other['koubei']:
			koubei1 = {}
			car = each['car'].encode('utf-8')
			score = change_dict(each['score'])
			comment = change_dict(each['comment'])
			koubei1['car'] = car
			koubei1['score'] = score
			koubei1['comment'] = comment
			koubei.append(koubei1)

		second['koubei'.encode('utf-8')] = koubei
		all_need.setdefault(name,second)

	return all_need





def change_list(data):
	afer_change = []
	for i in data:
		afer_change.append(i.encode('utf-8'))
	return afer_change

def change_dict(data):
	afer_change = {}
	for i,j in data.iteritems():
		if type(j)==list:
			afer_change.setdefault(i.encode('utf-8'),change_list(j))
		else:
			afer_change.setdefault(i.encode('utf-8'),j.encode('utf-8'))
	return afer_change

def save(data,name):
    f = codecs.open('aaa.json','w',encoding='utf-8')
    data = json.dumps(data)
    f.write(data.decode('unicode_escape'))
    f.close()


f = json.load(open('yiche_koubei_other.json','r'))


need = change(f)
save(need,'deal')
