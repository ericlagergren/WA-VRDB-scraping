#!/bin/bash
touch citylist.bak;
cat citylist.txt | sed 's/, /\n/g' > citylist.bak;
cat citylist.bak | sed "s/'//g" > citylist.txt;
cat citylist.txt | tr -d '][' > citylist.bak;
sort citylist.bak | awk '!seen[$0]++' > citylist.txt;
exit