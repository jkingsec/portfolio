#!/bin/bash
flag_f="";
while getopts L: flag
do
    case "${flag}" in
      L)flag_f=${OPTARG};;
      *);;
    esac
done;
if [ "$flag_f" != "" ];then
  while read -r line;
  do
    echo "====Results For ""$line""===="
    echo "Scope Targets: " "$(wc -l < ../programs/"$line"/scope.txt)";
    echo "Scope Wildcards: " "$(wc -l < ../programs/"$line"/scope_wildcards.txt)";
    echo "APIs: " "$(wc -l < ../programs/"$line"/apis.txt)";
    echo "Targets Out of Scope: " "$(wc -l < ../programs/"$line"/oos.txt)";
    echo "Wildcards Out of Scope" "$(wc -l < ../programs/"$line"/oos_wildcards.txt)";
  done < "$flag_f"
elif [ "$1" == "" ]; then
  echo """Example Usage:
  ./count_scope.sh {program handle}
  ./count_scope.sh -L {list of handles}"""
else
  handle=$1;
  echo "====Results For ""$handle""===="
  echo "Scope Targets: " "$(wc -l < ../programs/"$handle"/scope.txt)";
  echo "Scope Wildcards: " "$(wc -l < ../programs/"$handle"/scope_wildcards.txt)";
  echo "APIs: " "$(wc -l < ../programs/"$handle"/apis.txt)";
  echo "Targets Out of Scope: " "$(wc -l < ../programs/"$handle"/oos.txt)";
  echo "Wildcards Out of Scope: " "$(wc -l < ../programs/"$handle"/oos_wildcards.txt)";
fi



