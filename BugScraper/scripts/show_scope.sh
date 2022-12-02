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
    echo "----Scope Targets----";
    while read -r scope;
    do
      echo "$scope"
    done < ../programs/"$line"/scope.txt
    echo "----Scope Wildcards----";
    while read -r scopew;
    do
      echo "$scopew"
    done < ../programs/"$line"/scope_wildcards.txt
    echo "----APIs----";
    while read -r apis;
    do
      echo "$apis"
    done < ../programs/"$line"/apis.txt
    echo "----Targets Out of Scope----";
    while read -r oos;
    do
      echo "$oos"
    done < ../programs/"$line"/oos.txt
    echo "----Wildcards Out of Scope----";
    while read -r oosw;
    do
      echo "$oosw"
    done < ../programs/"$line"/oos_wildcards.txt
  done < "$flag_f"
elif [ "$1" == "" ]; then
  echo """Example Usage:
  ./show_scope.sh {program handle}
  ./show_scope.sh -L {list of handles}"""
else
  handle=$1;
  echo "====Results For ""$handle""===="
  echo "----Scope Targets----";
  while read -r scope;
  do
    echo "$scope"
  done < ../programs/"$handle"/scope.txt
  echo "----Scope Wildcards----";
  while read -r scopew;
  do
    echo "$scopew"
  done < ../programs/"$handle"/scope_wildcards.txt
  echo "----APIs----";
  while read -r apis;
  do
    echo "$apis"
  done < ../programs/"$handle"/apis.txt
  echo "----Targets Out of Scope----";
  while read -r oos;
  do
    echo "$oos"
  done < ../programs/"$handle"/oos.txt
  echo "----Wildcards Out of Scope----";
  while read -r oosw;
  do
    echo "$oosw"
  done < ../programs/"$handle"/oos_wildcards.txt
fi