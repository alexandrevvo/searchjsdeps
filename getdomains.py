import json
import requests

#BUSCA DOMÍNIOS DE CADA PROGRAMA PRESENTE NO ESCOPO, DE ACORDO COM https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-programs/master/chaos-bugbounty-list.json;

URL = "https://raw.githubusercontent.com/projectdiscovery/public-bugbounty-programs/master/chaos-bugbounty-list.json"

r = requests.get(URL)
dados = json.loads(r.content)
for program in dados['programs']:
	#print(program['bounty'])
	if program['bounty']:
		for domain in program['domains']:
			print(domain)
