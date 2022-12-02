#!/bin/bash
# This runs terribly, but works
if [ "$1" == "" ]; then
  echo """Example Usage:
  ./return_urls.sh {list of handles}"""
else
  while read -r line
    do
      csvsql --query "SELECT URL FROM bugbounty WHERE Handle='$line'" "../bugbounty.csv" | sed -n '2 p'
    done < "$1"
fi