#!/bin/bash
if [ "$1" != "" ]; then
  while read -r line;
    do
      if (($(wc -l < ../programs/"$line"/apis.txt) > 0)); then
          echo "$line"
      fi
    done < "$1"
else
  echo """Example Usage:
  ./find_apis.sh {list of handles}"""
fi
