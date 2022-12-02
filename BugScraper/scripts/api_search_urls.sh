#!/bin/bash

if [ "$1" != "" ]; then
  while read -r line;
    do
      echo "https://searx.be/search?q=$line+API+documentation" | sed 's/ /+/g'
    done < "$1"
else
  echo """Example Usage:
  ./api_search_urls.sh {list of handles}"""
fi
