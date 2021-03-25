# searchjsdeps
Search javascript files looking for potential dependency confusion

# USAGE
* -s,--search, File containing a list of js urls to search npm dependencies
* -t,--threads, Number of threads; Default = 8
* -u,--url, Single url of the javascript file
* -d,--download, Download the content of the javascripts urls in a file
* -p,--path, Directory path to save the js contents

Generating the file with js urls:

Enumerating subdomains
* amass enum -d d1.com, d2.com -o amass.txt
* subfinder [-d d1.com] [-dL file.txt] -o subfinder.txt
* cat amass.txt subfinder.txt | sort -u | tee amass_subf.txt
* cat amass_subf.txt | httprobe --prefer-https | tee probed.txt
* echo d1.com | waybackurls | cut -d/ -f1-4 | sort -u | tee wayback.txt
  *  _In case of having multiple domais to search in waybackurls;_   
  * for dom in $(cat domains.txt); do waybackurls $dom | cut -d/ -f1-4 | sort -u >> wayback.txt;done


Generating the file with all hosts in the format "http://sub.domain.com/path"
* cat probed.txt wayback.txt > allhosts.txt 

Extracting all javascript files from each subdomain URL
* cat allhosts.txt | subjs | sort -u | grep -v "cloudflare\|jquery\|bootstrapcdn\|google" | tee jsfiles.txt 

**./searchjsdeps.py -f jsfiles.txt**
