#!/bin/bash
touch precincts.bak;
cat precincts.txt | sed 's/, /\n/g' > precincts.bak;
cat precincts.bak | sed "s/'//g" > precincts.txt;
cat precincts.txt | tr -d '][' > precincts.bak;
sort precincts.bak | awk '!seen[$0]++' > precincts.txt;
exit
