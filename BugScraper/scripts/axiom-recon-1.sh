#!/usr/bin/env bash
# This all recon scans, short of dictionary attacks and nmap

#
axiom-fleet recon -i=15 -t=2;
while read -r handle; do
    cat ../programs/"$handle"/scope_wildcards.txt | sed 's/*.//' | axiom-scan -m subfinder -o ../programs/"$handle"/subs.txt;
    ./compare_subs.sh ../programs/"$handle"/subs.txt;
    axiom-scan ../programs/"$handle"/subs_cleaned.txt -m  -o ../programs/"$handle"/httpx_tech.txt; # httpx tech
    axiom-scan ../programs/"$handle"/apis.txt -m  -o ../programs/"$handle"/.txt; # resolve ips to scanless
    # wappalyzer-cli

    axiom-scan ../programs/"$handle"/subs_cleaned.txt -m  -o ../programs/"$handle"/hakrawler.txt; # hakrawler
    axiom-scan ../programs/"$handle"/subs_cleaned.txt -m  -o ../programs/"$handle"/paramspider.txt; # paramspider
    axiom-scan ../programs/"$handle"/subs_cleaned.txt -m  -o ../programs/"$handle"/waybackurls.txt; # waybackurls
    axiom-scan ../programs/"$handle"/.txt -m aquatone; # aquatone
done < "$1"
axiom-rm "recon*" -f;
