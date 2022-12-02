#!/bin/bash
while read -r handle; do
    kr scan "../programs/$handle/apis.txt" -w /tools/seclists/kiterunner/routes-large.kite -o "../programs/$handle/kr_large.txt" -x 10;
done < "$1"
