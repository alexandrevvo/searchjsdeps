#!/usr/bin/python3

import requests
import re
import json
from termcolor import colored
import argparse as ap
from urllib.parse import urlparse
import hashlib
import os


requests.packages.urllib3.disable_warnings() 

def search_url(single_url):
	r = requests.get(single_url, verify=False)

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




def search(jsfile):
	pwnd = []
	with open(jsfile,"r") as f:
		urls = f.readlines()
		for url in urls:
				
			headers = {"accept": "text/html,application/xhtml+xml,application/xml,application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36","accept-encoding": "gzip, deflate, br", "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}
			r = requests.get(url.rstrip("\n"), headers= headers, verify=False)
			#print(r.text)
			print(colored(f"Pesquisando arquivo {url}", "blue"), end='') 

			print(colored(f"{r.status_code}\n", "blue"))

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
					r2 = requests.get(url_npm, headers=headers)

					if r2.status_code != 200:
						print(colored(f"Pacote: {package} não encontrado! Versão solicitada: {version}", "red"))
						pwnd.append(f"{package}, {version}")
					else:
						print(colored(f"Pacote {package} encontrado!", "green"))
			#else:
				#print("no dependencies\n")
	print(pwnd)

#usage example: cat enum-spotify.net | httprobe --prefer-https | subjs | grep -v "cloudflare\|jquery\|bootstrapcdn\|google" | sort -u > javascripts.txt; python3 find-deps.py

if __name__=='__main__':
	parser = ap.ArgumentParser()
	parser.add_argument('-s','--search', help="File containing a list of js urls to search npm dependencies", required=False)
	parser.add_argument('-u','--url',help="Single url of the javascript file",required=False)
	parser.add_argument('-d','--download',help="Download the content of the javascripts urls in a file",required=False)
	parser.add_argument('-p','--path',help="Directory path to save the js contents",required=False)
	args = parser.parse_args()

	if args.search:
		search(args.search)
	if args.url:
		search_url(args.url)
	if args.download:
		if args.path is None:
			parser.error('Please provide the directory path to save the js contents (-p)')
		else:
			download(args.download, args.path)
