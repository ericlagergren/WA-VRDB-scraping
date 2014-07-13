#!/bin/bash
tr -d '\t ]["' < ldages.txt > ldages.bak;
tr -d '\t ]["' < cdages.txt > cdages.bak;
tr -d '\t ]["' < precinctages.txt > precinctages.bak;
tr -d '\t ]["' < cityages.txt > cityages.bak;
sort -n ldages.bak > ldages.txt;
sort -n cdages.bak > cdages.txt;
sort -n precinctages.bak > precinctages.txt;
sort -n cityages.bak > cityages.txt;
rm *.bak
exit