#!/usr/bin/bash
echo "Analisando entradas do arquivo domains.txt.. verifique se existe esse arquivo no diretório atual!\n";

amass enum -df domains.txt -o amass.txt;
echo "amass done\n";
subfinder -dL domains.txt -o subfinder.txt;
echo "subfinder done\n";
cat amass.txt subfinder.txt | sort -u | tee amass_subf.txt;
cat amass_subf.txt | httprobe --prefer-https | tee probed.txt
echo "httprobe done\n";
for dom in $(cat domains.txt); do waybackurls $dom | cut -d/ -f1-4 | sort -u >> wayback.txt;done;
echo "wayback done\n";

cat probed.txt wayback.txt > allhosts.txt;

cat allhosts.txt | subjs | sort -u | grep -v "cloudflare|jquery|bootstrapcdn|google" | tee jsfiles.txt;

python3 searchjsdeps.py -s jsfiles.txt;

