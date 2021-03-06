

import json
import requests
import argparse as ap
import base64
from termcolor import colored

def getorg():
    orgs = []
    #fetching data from this github repository. 
    URL = "https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/34928597d1c16ac3e12d05b9020e984b514b7e99/data/intigriti_data.json"
    r = requests.get(URL, headers={"Accept":"application/vnd.github.v3+json", "Authorization": "token "+"<token>"})
    arquivo = r.json()
    for x in range(len(arquivo)):
        orgs.append(arquivo[x]['handle'])
        if arquivo[x]['company_handle'] not in orgs:
            orgs.append(arquivo[x]['company_handle'])
    if orgs:
        for organization in orgs:
            search(organization)

def check_principal_pkg_name(pkgname):
    url_npm = f"https://registry.npmjs.org/{pkgname}"
    headers = {"Connection": "close", "accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}
    r = requests.get(url_npm, headers=headers)
    print(colored("Checking package name.","blue"))
    if r.status_code != 200:
        print(colored(f"Pacote: {pkgname} não encontrado! Versão solicitada: xxx", "red"))
        pwnd.append(f"{pkgname}, xxx")
    else:
        print(f"Pacote {pkgname} encontrado!")



def search(org):
    urls = []
    org_invalida = []
    org_sem_package = []
    org_lowercase = org.lower()
    org_capitalized = org.capitalize()
    try:
        # Falta tratar a pesquisa nas outras páginas qdo o resultado contem mais de 100 registros.. Além disso, o github limita a pesquisa aos primeiros 1000 results.
        URL = "https://api.github.com/search/code?per_page=100&q="+"filename:package.json"+"+org:"+org_lowercase
        fp = requests.get(URL, headers={"Accept":"application/vnd.github.v3+json", "Authorization": "token "+"<token>"})
        js = json.loads(fp.content)
        if fp.status_code !=200:
            URL = "https://api.github.com/search/code?per_page=100&q="+"filename:package.json"+"+org:"+ org_capitalized
            fp = requests.get(URL, headers={"Accept":"application/vnd.github.v3+json", "Authorization": "token "+"<token>"})
            js = json.loads(fp.content)
            if fp.status_code !=200:
                return
        for url in js['items']:
            if "package.json" in (url['url']):
                if "package.json.meta" in (url['url']):
                    continue
                if "package.json~" in (url['url']):
                    continue
                urls.append(url["url"])
        if not urls:
            #print(f"A empresa {org} não possui arquivos package.json")
            org_sem_package.append(org)
            return

        print(f"{len(urls)} arquivos encontrados")

        with open(org, 'a') as output:
            with open(f"{org}+dev", 'a') as output2:
                for URL in urls:
                #exemplo de URL = "https://api.github.com/repositories/309216415/contents/package.json?ref=6f0107c3cbc0983b4d0364c87e2168b2d21f63c7"
                    r = requests.get(URL, headers={"Accept":"application/vnd.github.v3+json", "Authorization": "token "+"<token>"})
                    dp = {}
                    
                    try:
                        js = json.loads(r.content)
                        arquivo64 = base64.b64decode(js['content'])
                        arquivo = arquivo64.decode('utf-8')
                        js2 = json.loads(arquivo)
                        #print(js2)
                        download_url = js['download_url']
                    
                        for pacote in js2['dependencies'].keys():
                            dp[pacote] = js2['dependencies'][pacote]
                        json.dump(js2['dependencies'],output)
                    except Exception as e:
                        pass

                    print(colored(f"URL: {download_url}",'green'))
                    ##Adicionando a verificação do nome do pacote principal no npm;
                    try:
                        check_principal_pkg_name(js2['name'])
                    except Exception as e:
                        pass

                    try:
                        #Fazer a verificação nas devDependencies tbm ?
                        #for pacote in js2['devDependencies'].keys():
                        #    dp[pacote] = js2['devDependencies'][pacote]
                        json.dump(js2['devDependencies'],output2)
                    except Exception as e:
                        pass
                    if dp:   
                        print(colored("Checking dependencies.","blue"))                   
                        for package in dp.keys():
                            url_npm = f"https://registry.npmjs.org/{package}"
                            headers = {"Connection": "close", "accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"}
                            r = requests.get(url_npm, headers=headers)
                            if r.status_code != 200:
                                print(colored(f"Pacote: {package} não encontrado! Versão solicitada: {dp[package]}", "red"))
                                pwnd.append(f"{package}, {dp[package]}")
                            else:
                                print(f"Pacote {package} encontrado!")
                        print("")
                    else:
                        print(f"O pacote não possui dependencies")
        for i in pwnd:
            print(f"Dep não encontradas: {i}")
        for i in org_invalida:
            print(f"Orgs não encontradas: {i}")
    except Exception as e:
        raise e

if __name__=='__main__':
    pwnd = []
    parser = ap.ArgumentParser()
    parser.add_argument('-o','--org', help="organization that will be search", required=False)
    parser.add_argument('-a','--aut',required=False, type=bool)
    args = parser.parse_args()
    if args.org:
        search(args.org)
    if args.aut:
        getorg()
