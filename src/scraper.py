#!/usr/bin/env python

'''
 ----------------------------------------------------------------------------
 "THE BEER-WARE LICENSE" (Revision 42):
 Eric Lagergren <contact@ericlagergren.com> wrote this file. As long as you retain this notice you
 can do whatever you want with this stuff. If we meet some day, and you think
 this stuff is worth it, you can buy me a beer in return
 ----------------------------------------------------------------------------
 '''

from __future__ import division
import csv
import datetime
import subprocess
import gc

vrdb = 'active.txt'

# Write headings to three output files

with open('legdata.txt', 'wb+') as myfile:
    myfile.write('LegDist,AvgAge,NumMales,PerMales,NumFemales,PerFemales' + '\r\n')

with open('citydata.txt', 'wb+') as myfile:
    myfile.write('City,AvgAge,NumMales,PerMales,NumFemales,PerFemales' + '\r\n')

with open('precinctdata.txt', 'wb+') as myfile:
    myfile.write('Precinct,AvgAge,NumMales,PerMales,NumFemales,PerFemales' + '\r\n')

def getCities():

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	cities = []

	# Appends all the data from each person inside a specific city

	for row in reader:
		if row['RegCity']:
			cities.append(row.get('RegCity'))

	return cities

def getPrecincts():

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	precincts = []

	# In Washington counties can use their own precinct codes which are the county code (e.g. King is KI) + precinct code + precinct part
	# To keep each unique we concat each part with a '+' -- this keeps the values separate but still unique

	for row in reader:
		if row['PrecinctCode']:
			precincts.append(str(row.get('CountyCode')) + '+'  + str(row.get('PrecinctCode')) + '+' + str(row.get('PrecinctPart')))

	with open('precincts.txt', 'ab+') as myfile:
	    myfile.write(str(precincts))

def sortLists(function, output_file, shell_script):

	numcities = function
	numcities = str(numcities)

	with open(output_file, 'ab+') as myfile:
		myfile.write(numcities)

	subprocess.call([shell_script])

def getInformation(location, identifier, output_file):

	# Opens VRDB and parses it line by line

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter= '\t')

	master_list = []
	ages = []
	nummale = 0
	numfemale = 0

	if useprecincts != True:
		for row in reader:
			if row[location] == str(identifier):	
				master_list.append(row)

	if useprecincts:
		for row in reader:
			if str(row['CountyCode']) + '+' + str(row['PrecinctCode']) + '+' + str(row['PrecinctPart']) == identifier:
				master_list.append(row)

	# For each person in our specific LD/city/precinct, get their information and append it to the correct lists
	# 31556952 is used because it's the representation of 365.2425 days in seconds. 
	# 365.2425 is used because there's only 97 leap years every 400 years, not 100 (Gregorian calendar)
	# We also get the number of each gender

	for x,value in enumerate(master_list):
		dates = datetime.datetime.now() - datetime.datetime.strptime(value['Birthdate'], '%m/%d/%Y')
		ages.append(datetime.timedelta.total_seconds(dates) / 31556952)
		if value['Gender'] == "M":
			nummale += 1
		if value['Gender'] == "F":
			numfemale += 1


	# This defines the ages. Takes the sum of all the ages and divides it by the total values
	# It also takes the total number of each gender and divides that by the total
	# This gives us a percentage with 3 decimal places

	total_values = len(ages)
	average_age = sum(ages) / total_values

	perfemale = '{percent:.3%}'.format(percent=numfemale/total_values)
	permale = '{percent:.3%}'.format(percent=nummale/total_values)

	results = str(identifier) + ',' + str(average_age) + ',' + str(nummale) + ',' + str(permale) + ',' + str(numfemale) +',' +  str(perfemale)
	
	# Prints output to console so we can see our script is working
	# `with... as myfile` appends each line to with \r\n so we can work with both unix and windows

	print results

	with open(output_file, 'ab+') as myfile:
	    myfile.write(results + '\r\n')

	gc.collect()	

# Gets Legislative District data

for i in xrange(1, 50):
	getInformation('LegislativeDistrict', i, 'legdata.txt')

# Gets city data

getCities()
sortLists(getCities, 'citylist.txt', './shellsubprocess.sh')
listofcities = [line.rstrip() for line in open('citylist.txt')]

for v in listofcities:
	getInformation('RegCity', v, 'citydata.txt')
# Gets precinct data

getPrecincts()
sortLists(getPrecincts, 'precinctlist.txt', './subshellprecincts.sh')
listofprecincts = [line.rstrip() for line in open('precincts.txt')]
useprecincts = True

# I'm passing 'a' because getInformation takes 3 args when I only need to pass two
# I suppose I *could* implement *args, but this works for such a simple scraper script

for y in listofprecincts:
	getInformation('a', y, 'precinctdata.txt')
