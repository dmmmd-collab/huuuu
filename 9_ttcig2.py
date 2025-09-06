import json
import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from pystyle import Write, Colors, Colorate
from datetime import datetime
import cloudscraper
import socket
import subprocess
from time import strftime
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from colorama import Fore, init
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.console import Console
from rich.text import Text

thanh = "\033[1;32m--------------------------------------------"

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Diagonal(Colors.cyan_to_green, """
    [1;31m██████╗░░█████╗░███╗░░██╗░██████╗░  ██╗░░██╗
[1;34m██╔══██╗██╔══██╗████╗░██║██╔════╝░  ╚██╗██╔╝
[1;33m██████╦╝██║░░██║██╔██╗██║██║░░██╗░  ░╚███╔╝░
[1;32m██╔══██╗██║░░██║██║╚████║██║░░╚██╗  ░██╔██╗░
[1;35m██████╦╝╚█████╔╝██║░╚███║╚██████╔╝  ██╔╝╚██╗
[1;36m╚═════╝░░╚════╝░╚═╝░░╚══╝░╚═════╝░  ╚═╝░░╚═╝

[1;97mTool By: [1;32mBóng X🚀                      [1;97mPhiên Bản: [1;32mVIP👑     
[1;97mTên Thật: [1;33mTrần Đức Doanh💎            [1;97mTelegram: [1;36mhttps://t.me/doanhvip1
[1;37m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1;32m[•] TOOL GOLIKE LINKEDIN AUTO 100% VIP 🚀
[1;36m[•] CONTACT: https://t.me/doanhvip1 💬
[1;33m[•] ADMIN: Bóng X 🎯
[1;31m[•] CHANNEL: @doanhvip1 📢
[1;34m[•] FACEBOOK: https://www.facebook.com/share/ đéo cho 
[1;37m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━           
"""))


red = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
cam = "\033[38;5;208m"
tim = "\033[1;35m"
lam = "\033[1;36m"
trang = "\033[1;37m"        
den = '\x1b[1;90m'
luc = '\x1b[1;32m'
trang = '\x1b[1;37m'
red = '\x1b[1;31m'
vang = '\x1b[1;33m'
tim = '\x1b[1;35m'
lamd = '\x1b[1;34m'
lam = '\x1b[1;36m'
purple = '\\e[35m'
hong = '\x1b[1;95m'
thanh_xau="\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1;32m"
thanh_dep="\033[1;31m[\033[1;37m=.=\033[1;31m] \033[1;37m=> \033[1;32m"
from bs4 import BeautifulSoup
import json
import requests
import os, sys, re, json
from time import sleep
from datetime import datetime
import random
import time
import os
dem = 0
list=''
os.system("cls" if os.name == "nt" else "clear")
banner()
list_cookie = []
def coin(ckvp):
	h_xu = {'user-agent':'Mozilla/5.0 (Linux; Android 11; Live 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.28 Mobile Safari/537.36','cookie':ckvp}
	x = requests.post('https://vipig.net/home.php', headers=h_xu).text
	xu = x.split('"soduchinh">')[1].split('<')[0]
	return xu

def cookie(token):
	ck = requests.post('https://vipig.net/logintoken.php',headers={'Content-type':'application/x-www-form-urlencoded',},data={'access_token':token})
	cookie = 'PHPSESSID='+(ck.cookies)['PHPSESSID']
	return cookie
def get_nv(type, ckvp):
	headers={'content-type':'text/html; charset=UTF-8','accept':'application/json, text/javascript, */*; q=0.01','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','referer':'https://vipig.net/kiemtien/','x-requested-with':'XMLHttpRequest','sec-ch-ua-mobile':'?1','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-platform':'"Android"','sec-fetch-site':'same-origin','sec-fetch-mode':'cors','sec-fetch-dest':'empty','cookie':ckvp}
	a = requests.post(f'https://vipig.net/kiemtien{type}/getpost.php', headers=headers).json()
	return a
def nhan_tien(list, ckvp, type):
	data_xu='id='+str(list)
	data_nhan=str(len(data_xu))
	headers={'content-length':data_nhan,'sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','content-type':'application/x-www-form-urlencoded; charset=UTF-8','accept':'*/*','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-mobile':'?1','x-requested-with':'XMLHttpRequest','sec-fetch-site':'same-origin','origin':'https://vipig.net','sec-ch-ua-platform':'"Android"','sec-fetch-mode':'cors','sec-fetch-dest':'empty','referer':'https://vipig.net/kiemtien'+type+'/','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cookie':ckvp}
	a = requests.post(f'https://vipig.net/kiemtien{type}/nhantien.php',headers=headers,data=data_xu).text
	return a
def nhan_sub(list, ckvp):
	data_xu='id='+str(list[0:len(list)-1])
	data_nhan=str(len(data_xu))
	headers={'content-length':data_nhan,'sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','content-type':'application/x-www-form-urlencoded; charset=UTF-8','accept':'*/*','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-mobile':'?1','x-requested-with':'XMLHttpRequest','sec-fetch-site':'same-origin','origin':'https://vipig.net','sec-ch-ua-platform':'"Android"','sec-fetch-mode':'cors','sec-fetch-dest':'empty','referer':'https://vipig.net/kiemtien/subcheo','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cookie':ckvp}
	a = requests.post('https://vipig.net/kiemtien/subcheo/nhantien2.php',headers=headers,data=data_xu).json()
	return a

def delay(dl):
  try:
    for i in range(dl, -1, -1):
       print('\033[1;95m[Bóng X]\033[1;93m['+str(i)+' \033[1;92mGiây]           ',end='\r')
       sleep(1)
  except:
     sleep(dl)
     print(dl,end='\r')
     
	
def name(cookie):
    try:
        headers={'Host':'www.instagram.com','cache-control':'max-age=0','viewport-width':'980','sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','sec-ch-ua-mobile':'?1','sec-ch-ua-platform':'"Android"','upgrade-insecure-requests':'1','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','sec-fetch-site':'same-origin','sec-fetch-mode':'navigate','sec-fetch-user':'?1','sec-fetch-dest':'document','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cookie':cookie}
        a = requests.get('https://www.instagram.com/', headers=headers).text
        user = re.search(r'contacts":null,"username":"(.*?)"', a).group(1)
        id = cookie.split('ds_user_id=')[1].split(';')[0]
        return user, id
    except:
        return 'die', 'die'
def bongoc(so):
	a= "────"*so
	for i in range(len(a)):
		sys.stdout.write(a[i])
		sys.stdout.flush()
		sleep(0.003)
	print()
    
	
def like(id, cookie):
	headers = {"x-ig-app-id": "1217981644879628","x-asbd-id": "198387","x-instagram-ajax": "c161aac700f","accept": "*/*","content-length": "0","content-type": "application/x-www-form-urlencoded","user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19","x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0],"x-requested-with": "XMLHttpRequest","cookie": cookie}
	like = requests.post(f'https://www.instagram.com/web/likes/{id}/like/',headers=headers).text
	if 'ok' not in like:
		return '1'
	else:
		return '2'
def get_id(link):
	headers = {"x-ig-app-id": "1217981644879628","x-asbd-id": "198387","x-instagram-ajax": "c161aac700f","accept": "*/*","content-length": "0","content-type": "application/x-www-form-urlencoded","user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19","x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0],"x-requested-with": "XMLHttpRequest","cookie": cookie}
	try:
		a = requests.get(link, headers=headers).text
		id = a.split('media?id=')[1].split('"')[0]
		return id
	except:
		return False

def follow(id, cookie):
	headers = {"x-ig-app-id": "1217981644879628","x-asbd-id": "198387","x-instagram-ajax": "c161aac700f","accept": "*/*","content-length": "0","content-type": "application/x-www-form-urlencoded","user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19","x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0],"x-requested-with": "XMLHttpRequest","cookie": cookie}
	fl = requests.post("https://i.instagram.com/web/friendships/"+id+"/follow/", headers=headers).text
	if 'ok' not in fl:
		return '1'
	else:
		return fl
def cmt(msg, id , cookie):
	headers = {"x-ig-app-id": "1217981644879628","x-asbd-id": "198387","x-instagram-ajax": "c161aac700f","accept": "*/*","content-length": "0","content-type": "application/x-www-form-urlencoded","user-agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03S) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19","x-csrftoken": cookie.split('csrftoken=')[1].split(';')[0],"x-requested-with": "XMLHttpRequest","cookie": cookie}
	cmt = requests.post(f'https://i.instagram.com/api/v1/web/comments/{id}/add/', headers=headers, data={'comment_text':msg}).json()
	try:
		cmt['status'] == 'ok'
		return 'ok'
	except:
		return cmt
		
	
def cau_hinh(id_ig, ckvp):
	headers={'content-length':'23','sec-ch-ua':'"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"','accept':'*/*','content-type':'application/x-www-form-urlencoded; charset=UTF-8','x-requested-with':'XMLHttpRequest','sec-ch-ua-mobile':'?1','user-agent':'Mozilla/5.0 (Linux; Android 11; vivo 1904) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36','sec-ch-ua-platform':'"Android"','sec-fetch-site':'same-origin','sec-fetch-mode':'cors','sec-fetch-dest':'empty','referer':'https://vipig.net/cauhinh/datnick.php','accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cookie':ckvp}
	a=requests.post('https://vipig.net/cauhinh/datnick.php', headers=headers, data={'iddat[]':id_ig}).text
	return a

while True:
	print(thanh)
	token = input('\033[1;32mNhập Access_Token Vipig:\033[1;33m ')
	log = requests.post('https://vipig.net/logintoken.php', headers={'Content-type':'application/x-www-form-urlencoded'}, data={'access_token':token}).json()
	if log['status'] == 'success':
		user = log['data']['user']
		xu = log['data']['sodu']
		ckvp = cookie(token)
		print('\033[1;32mĐăng Nhập Thành Công ')
		break
		token.read(token)
	elif log['status'] == 'fail':
		print(log['mess'])
os.system("cls" if os.name == "nt" else "clear")
banner()
x = 0
print('\033[1;32m[LƯU Ý] Muốn Dừng Nhập Cookie Thì Nhấn Enter')
while True:
	x = x +1
	print(thanh)
	cookie = input(Colorate.Diagonal(Colors.red_to_green,f'Nhập Cookie Instagram Thứ {x} : '))
	if cookie == '' and x > 1:
		break
	ten = name(cookie)
	if ten[0] != 'die':
		print(thanh)
		print(f'\033[1;32mUser Acc IG\033[1;95m : {ten[0]} | \033[1;32mCookie : Live ✔️')
		list_cookie.append(cookie)
		
	else:
		print('\033[1;31mCookie Instagram Die Hoạc Sai Định Dạng ! Vui Lòng Nhập Lại !!! ')
		x = x-1
		

os.system("cls" if os.name == "nt" else "clear")
banner()
print(f"{red}════════════════════════════════════════════════════")
print(f"""\033[1;32mTên Tài Khoản: \033[1;33m{user}
\033[1;32mXu : \033[1;33m{xu}
\033[1;32mSố Cookie Đã Lưu: \033[1;33m{len(list_cookie)}""")
print(f"{red}════════════════════════════════════════════════════")

print(Colorate.Diagonal(Colors.green_to_red,"Job Hiện Đang Có : "))
print(Colorate.Diagonal(Colors.green_to_red,"[~♥~] => Nhập [1] Chạy Job LikePost "))
print(Colorate.Diagonal(Colors.green_to_red,"[~♥~] => Nhập [2] Chạy Job FollowCheo "))
print(Colorate.Diagonal(Colors.green_to_red,"[~♥~] => Nhập [3] Chạy Job Cmtcheo"))
print(Colorate.Diagonal(Colors.green_to_red,"[~♥~] => Có thể chạy full NV 😆 VD (123...) "))
print(f"{red}════════════════════════════════════════════════════")
chon = input(Colorate.Diagonal(Colors.blue_to_cyan,'[♡] => Nhập NV Cần Chạy : '))
dl = int(input(Colorate.Diagonal(Colors.cyan_to_green,'Delay Thực Hiện Job: ')))
chong_block = int(input('Sau Bao Nhiêu Nhiệm Vụ Chống Block : '))
print(f'\033[1;32mSau\033[1;33m {chong_block} \033[1;32mNhiệm Vụ Nghỉ Ngơi ____ \033[1;32mGiây       ',end='\r')
delay_block = int(input(f'\033[1;32mSau\033[1;33m {chong_block} \033[1;32mNhiệm Vụ Nghỉ Ngơi '))
doi_acc = int(input('\033[1;32mSau Bao Nhiêu Nhiệm Vụ Thì Đổi Nick IG:\033[1;33m '))
print(f"{red}════════════════════════════════════════════════════")
#cookie='có cặc'

while True:
	x = 0
	rvtool247=0
	if len(list_cookie) == 0:
		print('\033[1;31mToàn Bộ Cookie Đã Out Vui Lòng Nhập Lại !!')
		while True:
			x = x + 1
			cookie = input(f'\033[1;32mNhập Cookie Instagram Thứ {x}:\033[1;33m ')
			if cookie == '' and x > 1:
				break
			ten = name(cookie)
			if ten[0] != 'die':
				print(f'\033[1;33mUser Acc IG\033[1;95m: {ten[0]} ')
				list_cookie.append(cookie)
				
			else:
				print('\033[1;31mCookie Instagram Sai ! Vui Lòng Nhập Lại !!! ')
				x = x - 1
				
	for i in range(len(list_cookie)):
		if rvtool247 == 2:
			break
		loi_like = 0
		loi_cmt = 0
		cookie = list_cookie[i]
		user = name(cookie)
		id_ig=user[1]
		if user[0] == 'die':
			print('\033[1;31mCookie Instagram Die !!!! ')
			list_cookie.remove(cookie)
			continue
		ngoc = cau_hinh(id_ig, ckvp)
		if ngoc == '1':
			
			print(f'\033[1;32mCấu Hình ID Success :\033[1;33m {id_ig} | \033[1;32mUser: \033[1;33m{user[0]}')
			
		else:
			print(f'\033[1;31mCấu Hình Thất Bại ID: \033[1;32m{id_ig} | \033[1;33mUser: \033[1;32m{user[0]} ')
			delay(3)
			list_cookie.remove(cookie)
			continue
		rvtool247=0
		while True:
			if rvtool247 == 1 or rvtool247 == 2:
				break
			if '1' in chon:
				get_like = get_nv('', ckvp)
				if len(get_like) == 0:
					print('Tạm Thời Hết Nhiệm Vụ Like','     ',end ='\r')
				if len(get_like) != 0:
					print(f'\033[1;32mTìm Thấy \033[1;33m{len(get_like)} \033[1;32mNhiệm Vụ Like','     ',end ='\r')
				for x in get_like:
					link = x['link']
					uid = x['idpost']
					id = get_id(link)
					if id == False:
						continue
					lam = like(id, cookie)
					if lam ==  '1':
						user = name(cookie)
						if user[0] == 'die':
							print('\033[1;31mCookie Instagram Die !!!! ')
							list_cookie.remove(cookie)
							rvtool247=2
							break
						else:
							print(f'\033[1;31mTài Khoản {user[0]} Đã Bị Chặn Tương Tác \033[1;36m')
							list_cookie.remove(cookie)
							rvtool247=2
							break
					elif loi_like >= 4:
						print(f'\033[1;31mTài Khoản {user[0]} Đã Bị Chặn Tương Tác')
						list_cookie.remove(cookie)
						rvtool247=2
						break
					elif lam == '2':
						nhan = nhan_tien(uid, ckvp, '')
						if 'mess' in nhan:
							xu=coin(ckvp)
							dem = dem + 1
							tg=datetime.now().strftime("%H:%M:%S") 
							print(f'\033[1;31m|\033[1;33m{dem}\033[1;31m|\033[1;36m{tg}\033[1;31m|\033[1;32mLIKE\033[1;31m|\033[1;95m+300xu\033[1;31m|\033[1;39m{id}\033[1;31m|\033[1;35m{user[0]}\033[1;31m|\033[1;34m{xu}')
							loi_like = 0
							if dem % chong_block == 0:
								delay(delay_block)
							else:
								delay(dl)
							if dem % doi_acc == 0:
									rvtool247=1
									break
						else:
							tg=datetime.now().strftime("%H:%M:%S")
							print(f'\033[1;32m Like : \033[1;39m{id} \033[1;31mThất bại. ')
							loi_like += 1
							delay(dl)
						
			if rvtool247 == 1 or rvtool247 == 2:
				break
			if '2' in chon:
				get_sub = get_nv('/subcheo', ckvp)
				if len(get_sub) == 0:
					print('Tạm Thời Hết Nhiệm Vụ Follow','     ',end ='\r')
				if len(get_sub) != 0:
					print(f'\033[1;32mTìm Thấy \033[1;33m{len(get_sub)} \033[1;32mNhiệm Vụ Follow','     ',end ='\r')
				for x in get_sub:
					id=x['soID']
					lam = follow(id, cookie)
					if lam == '1':
						if user[0] == 'die':
							print(f'\033[1;31mCookie Instagram Die !!!!  ')
							list_cookie.remove(cookie)
						else:
							print(f'\033[1;31mTài Khoản {user[0]} Đã Bị Chặn Tương Tác \033[1;36m')
							list_cookie.remove(cookie)
						rvtool247=2
						break
					data_id = open(f"{id_ig}.txt", "a+")
					data_id.write(str(id) + ',')
					dem = dem + 1
					tg=datetime.now().strftime("%H:%M:%S") 
					print(f'\033[1;31m|\033[1;33m{dem}\033[1;31m|\033[1;36m{tg}\033[1;31m|\033[1;32mFOLLOW\033[1;31m|\033[1;32mSUCCESS\033[1;31m|\033[1;39m{id}')
					data_id = open(f"{id_ig}.txt", "r")
					list = data_id.read()
					dem_sub = len(list.split(','))-1
					if dem % chong_block == 0:
						delay(delay_block)
					else:
						delay(dl)
					if dem_sub >= 6:
						nhan = nhan_sub(list, ckvp)
						try:
							xu_them = nhan['sodu']
							job = xu_them // 600
							xu=coin(ckvp)
							print(f'\033[1;32mNhận Thành Công {job} Nhiệm Vụ Followcheo | {hong}+{xu_them} | {lamd}{xu} ')
						except:
							print(nhan)
						os.remove(f"{id_ig}.txt")
						dem_sub = 0
					if dem % doi_acc == 0:
								rvtool247=1
								break
			if rvtool247 == 1 or rvtool247 == 2:
				break
			if '3' in chon:
				get_cmt = get_nv('/cmtcheo', ckvp)
				
				if len(get_cmt) == 0:
					print('Tạm Thời Hết Nhiệm Vụ Comment','     ',end ='\r')
				if len(get_cmt) != 0:
					print(f'\033[1;32mTìm Thấy \033[1;33m{len(get_cmt)} \033[1;32mNhiệm Vụ Comment','     ',end ='\r')
				for x in get_cmt:
					link = x['link']
					uid = x['idpost']
					msg = random.choice(json.loads(x['nd']))
					id = get_id(link)
					if id == False:
						continue
					lam = cmt(msg, id, cookie)
					if lam ==  '1':
						user = name(cookie)
						if user[0] == 'die':
							print('\033[1;31mCookie Instagram Die !!!! ')
							list_cookie.remove(cookie)
							rvtool247=2
							break
						else:
							print(f'\033[1;31mTài Khoản {user[0]} Đã Bị Chặn Tương Tác ')
							list_cookie.remove(cookie)
							rvtool247=2
							break
					elif loi_cmt >= 4:
						print(f'\033[1;31mTài Khoản {user[0]} Đã Bị Chặn Tương Tác')
						list_cookie.remove(cookie)
						rvtool247=2
						break
					elif lam == 'ok':
						nhan = nhan_tien(uid, ckvp, '/cmtcheo')
						if 'mess' in nhan:
							xu=coin(ckvp)
							dem = dem + 1
							tg=datetime.now().strftime("%H:%M:%S") 
							print(f'\033[1;31m|\033[1;33m{dem}\033[1;31m|\033[1;36m{tg}\033[1;31m|\033[1;32mCMTCHEO\033[1;31m|\033[1;95m+600xu\033[1;31m|\033[1;39m{id}\033[1;31m|\033[1;35m{user[0]}\033[1;31m|\033[1;34m{xu}')
							loi_cmt = 0
							if dem % chong_block == 0:
								delay(delay_block)
							else:
								delay(dl)
							if dem % doi_acc == 0:
									rvtool247=1
									break
						else:
							tg=datetime.now().strftime("%H:%M:%S") 
							print(f'\033[1;32m Commet : \033[1;39m{id} \033[1;31mThất bại. ')
							loi_cmt += 1
							delay(dl)

							
