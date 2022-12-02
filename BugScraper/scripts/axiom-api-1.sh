#!/bin/bash
axiom-fleet recon -i=15 -t=2;
while read -r handle; do
    axiom-scan ../programs/"$handle"/apis.txt -m krscan -w routes-large.kite -o ../programs/"$handle"/kite.txt;
done < "$1"
axiom-rm "recon*" -f;