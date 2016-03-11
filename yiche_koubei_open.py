#coding = utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json

def test1(test):
    print test['score']
    print '#'*60

    print test['rank']
    print '#'*60

    for i in  test['good']:
        print i
    print '#'*60

    for j in  test['bad']:
        print j
    print '#'*60

    koubei = test['koubei']
    for i in koubei:
        print '%'*60
        print i['car']

        for k,j in i['score'].items():
            print k,j

        for k,j in i['comment'].items():
            print k,j
    print len(koubei)

z = json.load(open('11.json','r'))
print z
print type(z)
print len(z)

for i in z:
    print i['car']