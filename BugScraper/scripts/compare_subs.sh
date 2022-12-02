#!/bin/bash
handle=$1
while read -r sub
do
  while read -r oos
  do
    while read -r oosw
    do
      if [ "$sub" != "$oos" ]; then
        echo > ../programs/"$handle"/subs_cleaned.txt
      elif [ "$sub" != "${oosw//\*/}" ]; then
        echo > ../programs/"$handle"/subs_cleaned.txt
      fi
    done < ../programs/"$handle"/oos.txt
  done < ../programs/"$handle"/oos_wildcards.txt
done < ../programs/"$handle"/subs.txt