import zipfile
import os
import pymysql
from bs4 import BeautifulSoup
import urllib.request
import requests
from socket import inet_aton
from struct import unpack
import csv
import re
import pythonwhois  # i'm using this http://cryto.net/pythonwhois
'''
create table victim (`id` int(11) PRIMARY KEY AUTO_INCREMENT, `time` bigint(100), `lastname` varchar(255), `bank` varchar(50), `Address` bigint(50), `ip` bigint(50), `country` varchar(100));

'''

def targetip(ip):
	
	try:

		a = pythonwhois.get_whois(ip)['raw']

		b = re.findall(r'ountry: +\w+',a[0])
		print((b[0].split(' ')[-1]))
		return (b[0].split(' ')[-1])

	except:
		return "Nop"


def ip2long(ip_addr): ## ip값을 int형으로 변한해주는 함수

	try : return unpack("!I", inet_aton(ip_addr))[0]

	except IOError : return None

def webdownload():
	url = 'http://107.174.85.141/cert/'
	realpath = 'C:/test/zip/'
	with open('finaltarget.txt', 'r') as testfile:
		with open('test6.csv', 'a') as writefiles:
			writer = csv.writer(writefiles)
    		
    		
			while True:
				readline = testfile.readline()
				ip = readline.split('.zip')[0]
				date = readline.split('zip')[1]
				
				
				if not readline:
					break
				
				#print(os.path.join(url,ip+'.zip'))
				#print(os.path.join(realpath,ip+'.zip'))
				
				urllib.request.urlretrieve(os.path.join(url,ip+'.zip'), os.path.join(realpath,ip+'.zip'))
				unzip(os.path.join(realpath,ip+'.zip'),date)
				onesheet = readunzip(ip,date)
				
				writer.writerow(onesheet)
				
				#curs.execute(sql, (onesheet[0],onesheet[1],onesheet[2],onesheet[3],onesheet[4],onesheet[5]))
				



def unzip(target,date):
	#print("uzip")
	#print(target)
	
	with zipfile.ZipFile(target,"r") as zip_ref:
		zip_ref.extractall("targetdir")
	#readunzip(target.split('.zip')[0].split('zip/')[-1],date)

# 디렉토리끍어서 여기루 보내기
def get_country_code(ip):
    url = "http://whois.kisa.or.kr/openapi/ipascc.jsp?query={}&key=%EC%9D%B4%EA%B3%B3%EC%97%90%ED%82%A4%EC%9E%85%EB%A0%A5&answer=json"
    req = requests.get(url.format(ip))
    data = req.json()
    return data.get('whois').get('countryCode')


def readunzip(target,date):
	#print("readunzip")
	#print(target,date)
	with open("./targetdir/signCert.cert",'r',encoding='euc-kr') as files:
		readall = files.read()
		test = (readall.split(','))
		#피해시각, 피해자의 이름, 은행명, 계좌번호, ip주소 , 소재지
		

		date = (date[:-1])
		name = (test[0].split('()')[0].split('=')[1]) #name
		country = targetip(target)
		bank = (test[1].split('=')[1]) # bank
		address = (test[0].split('()')[1]) #address

		return [date,name,bank,address,ip2long(target),country]

#unzip('100.101.120.45.zip')
#readunzip('./targetdir/signCert.cert')

db = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='hl1kej',db='cert',charset='utf8mb4')
curs = db.cursor()
sql = "insert into victim(time,lastname,bank,Address,ip,country) values (%s,%s,%s,%s,%s,%s)"
webdownload()
db.commit()
db.close()


#dbconnect()

