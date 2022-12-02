#!/bin/bash
# This runs terribly, but works
if [ "$1" == "" ]; then
  echo """Example Usage:
  ./return_names.sh {list of handles}"""
else
  while read -r line
    do
      csvsql --query "SELECT ProgramName FROM bugbounty WHERE Handle='$line'" "../bugbounty.csv" | sed -n '2 p'
    done < "$1"
fi
