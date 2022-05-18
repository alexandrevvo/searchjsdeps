#!/usr/bin/python3

import os
import requests
import re
import json
from termcolor import colored
import argparse as ap
from urllib.parse import urlparse
import hashlib
import os
import time
from threading import Thread
import queue

requests.packages.urllib3.disable_warnings() 

def search_url(single_url):
	try:
		r = requests.get(single_url, verify=False)
	except:
		print("Failed to connect.")
		return False

	dependencies_regex = re.compile("\"dependencies\":{")
	check_deps = dependencies_regex.findall(r.text)

	pkgs_regex = re.compile("\"[-_.@/\w]{1,50}\":\"[\^~]?[\d]{1,2}\.[\d]{1,2}\.[\d]{1,2}\"")
	pkgs = pkgs_regex.findall(r.text)

	#print(pkgs)

	for pkg in pkgs:
		package = pkg.split(":")[0].strip ('"')
		version = pkg.split(":")[1].strip ('"')
		#print(package)
		url_npm = f"https://registry.npmjs.org/{package}"
		headers = {"Connection": "close", "accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}
		
		r2 = requests.get(url_npm, headers=headers)

		if r2.status_code != 200:
			print(colored(f"Pacote: {package} não encontrado! Versão solicitada: {package}", "red"))
			pwnd.append(f"{package}, {version}")
		else:
			print(colored(f"Pacote {package} encontrado!", "green"))


def download(jsfile, content_path):
	try:
		#content_path="./jscontents"
		os.mkdir(content_path)
	except OSError:
		print ("Creation of the directory %s failed" % content_path)

	with open(jsfile,"r") as f:
		urls = f.readlines()
		for url in urls:
			url = url.rstrip("\n")
			#make the request for each url and parse creating the filename as domain.com-a6s5d4f6a56s4as65df4
			print(f"Downloading {url}")
			headers = {"accept": "text/html,application/xhtml+xml,application/xml,application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36","accept-encoding": "gzip, deflate, br", "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}
			r = requests.get(url, headers= headers, verify=False)
			host= urlparse(url).netloc
			path= hashlib.md5(urlparse(url).path.encode("utf8")).hexdigest()
			filename= host+"-"+path

			with open(content_path+"/"+filename, "a") as file:
				file.write(url+"\n")
				file.write(r.text)
				print(f"saved to {content_path}/{filename}\n")
				file.close()




def search():
	while not fila.empty():

		try:
			url = fila.get()
			headers = {"Connection": "close", "accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}

			r = requests.get(url.rstrip("\n"), headers=headers, verify=False)
		
			print(colored(f"Searching {url} - {r.status_code}", "blue")) 

			dependencies_regex = re.compile("\"dependencies\":{")
			check_deps = dependencies_regex.findall(r.text)

			
			if check_deps != []:
				pkgs_regex = re.compile("\"[-_.@/\w]{1,50}\":\"[\^~]?[\d]{1,2}\.[\d]{1,2}\.[\d]{1,2}\"")
				pkgs = pkgs_regex.findall(r.text)

				for pkg in pkgs:
					package = pkg.split(":")[0].strip ('"')
					version = pkg.split(":")[1].strip ('"')
					#print(package)
					url_npm = f"https://registry.npmjs.org/{package}"
					headers = {"Connection": "close", "accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}
					
					try:

						r2 = requests.get(url_npm, headers=headers)

						if r2.status_code != 200:
							print(colored(f"Package: {package} not found! Version: {version}", "red"))
							pwnd.append(f"{url} - {package}:{version}")
						else:
							print(colored(f"Pacote {package} encontrado!", "green"))
					except:
						continue
			#else:
				#print("no deps")
		except:
			pass

		fila.task_done()
		

if __name__=='__main__':
	pwnd=[]
	t0 = time.time()
	fila = queue.Queue()
	num_threads = 8

	parser = ap.ArgumentParser()
	parser.add_argument('-s','--search', help="File containing a list of js urls to search npm dependencies", required=False)
	parser.add_argument('-t','--threads', help="Number of threads; Default = 8", required=False)
	parser.add_argument('-u','--url',help="Single url of the javascript file",required=False)
	parser.add_argument('-d','--download',help="Download the content of the javascripts urls in a file",required=False)
	parser.add_argument('-p','--path',help="Directory path to save the js contents",required=False)
	args = parser.parse_args()

	if args.threads:
		num_threads = int(args.threads)

	if args.search:
		threadList = []
		with open(args.search,"r") as f:
			for url in f:
				url = url.rstrip("\n")
				fila.put(url)
			try:
				for k in range(num_threads):
					threadList.append(Thread(target=search))

				[t.start() for t in threadList]
				fila.join()
			except KeyboardInterrupt:
				exit(0)

		if pwnd != []:
			print(colored("\nPackages not found in the public NPM registry:\n","green"))
			for pkg in pwnd:
				print(colored(pkg,"red"))
				##insert a webhook alert here##
		else:
			print(colored("\nNo unpublished packages found.\n","green"))
		duration = time.time() - t0
		print(f"Time running: {duration}")	

	if args.url:
		search_url(args.url)
	if args.download:
		if args.path is None:
			parser.error('Please provide the directory path to save the js contents (-p)')
		else:
			download(args.download, args.path)
