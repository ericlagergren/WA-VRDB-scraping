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

vrdb = 'active.txt'

# Write headings to three output files

with open('ldages.txt', 'wb+') as myfile:
    myfile.write('LegDist,AvgAge,NumMales,PerMales,NumFemales,PerFemales' + '\r\n')

with open('cityages.txt', 'wb+') as myfile:
    myfile.write('City,AvgAge,NumMales,PerMales,NumFemales,PerFemales' + '\r\n')

with open('precinctages.txt', 'wb+') as myfile:
    myfile.write('Precinct,AvgAge,NumMales,PerMales,NumFemales,PerFemales' + '\r\n')


def legDistrictAges(ld):

	# Opens VRDB and parses it line by line

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter= '\t')

	legdistrict = []
	ages = []
	male = []
	female = []

	for row in reader:
		if row['LegislativeDistrict'] == str(ld):	
			legdistrict.append(row)

	# For each person in our specific LD, get their information and append it to the correct lists
	# 31556952 is used because it's the representation of 365.2425 days in seconds. 365.2425 is used because there's only 97 leap years every 400 years, not 100 (Gregorian calendar)

	for x,value in enumerate(legdistrict):
		dates = datetime.datetime.now() - datetime.datetime.strptime(value['Birthdate'], '%m/%d/%Y')
		ages.append(datetime.timedelta.total_seconds(dates) / 31556952)
		if value['Gender'] == "M":
			male.append(1)
		if value['Gender'] == "F":
			female.append(1)


	# This defines the ages. Takes the sum of all the ages and divides it by the total values

	total_values = len(ages)
	average_age = sum(ages) / total_values

	numfemale = sum(female)
	nummale = sum(male)
	perfemale = '{percent:.3%}'.format(percent=numfemale/total_values)
	permale = '{percent:.3%}'.format(percent=nummale/total_values)

	output = str(ld) + ',' + str(average_age) + ',' + str(nummale) + ',' + str(permale) + ',' + str(perfemale) +',' +  str(numfemale)
	
	# Prints output to console so we can see our script is working and with... as myfile appends each lien to with \r\n so we can work with both unix and windows

	print output

	with open('ldages.txt', 'ab+') as myfile:
	    myfile.write(output + '\r\n')

# In Washington there are 49 LDs, so we spit out each number 1-49 one at a time and feed it to our function that gets the ages

for i in xrange(1, 50):
	legDistrictAges(i)


'''

For the following code is a near duplicate of the first portion, except with values changed because it's formatted for precincts and cities instead of Legislative Districts.

The only real addition would be adding the sorting functions which loop through the file, take all the cities mentioned, add them to an array, pipe that to an external file, strip all formatting, remove duplicates, place all values on their own line, and then reads it as input into a variable that's used to find the ages.
'''


def getCities():

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	cities = []

	for row in reader:
		if row['RegCity']:
			cities.append(row.get('RegCity'))

	return cities

def sortCities():

	numcities = getCities()
	numcities = str(numcities)

	with open('citylist.txt', 'ab+') as myfile:
		myfile.write(numcities)

	subprocess.call(['./shellsubprocess.sh'])

getCities()
sortCities()

def cityAges(city):

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	cityages = []
	ages = []
	male = []
	female = []

	for row in reader:
		if row['RegCity'] == city:
			cityages.append(row)

	for x,value in enumerate(cityages):
		dates = datetime.datetime.now() - datetime.datetime.strptime(value['Birthdate'], '%m/%d/%Y')
		ages.append(datetime.timedelta.total_seconds(dates) / 31556952)
		if value['Gender'] == "M":
			male.append(1)
		if value['Gender'] == "F":
			female.append(1)

	total_values = len(ages)
	average_age = sum(ages) / total_values

	numfemale = sum(female)
	nummale = sum(male)
	perfemale = '{percent:.3%}'.format(percent=numfemale/total_values)
	permale = '{percent:.3%}'.format(percent=nummale/total_values)

	output = str(city) + ',' + str(average_age) + ',' + str(nummale) + ',' + str(permale) + ',' + str(perfemale) +',' +  str(numfemale)

	print output
	
	with open('cityages.txt', 'ab+') as myfile:
	    myfile.write(output + '\r\n')

listofcities = [line.rstrip() for line in open('citylist.txt')]

for v in listofcities:
	cityAges(v)

def getPrecincts():

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	precincts = []

	for row in reader:
		if row['PrecinctCode']:
			precincts.append(str(row.get('CountyCode')) + '+'  + str(row.get('PrecinctCode')) + '+' + str(row.get('PrecinctPart')))

	with open('precincts.txt', 'ab+') as myfile:
	    myfile.write(str(precincts))

def sortPrecincts():

	numprecincts = getPrecincts()
	numprecincts = str(numprecincts)

	with open('citylist.txt', 'ab+') as myfile:
		myfile.write(numprecincts)

	subprocess.call(['./subshellprecincts.sh'])

getPrecincts()
sortPrecincts()

def precinctAges(precinct):

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	precinctages = []
	ages = []
	male = []
	female = []

	for row in reader:
		if str(row['CountyCode']) + '+' + str(row['PrecinctCode']) + '+' + str(row['PrecinctPart']) == precinct:
			precinctages.append(row)

	for x,value in enumerate(precinctages):
		dates = datetime.datetime.now() - datetime.datetime.strptime(value['Birthdate'], '%m/%d/%Y')
		ages.append(datetime.timedelta.total_seconds(dates) / 31556952)
		if value['Gender'] == "M":
			male.append(1)
		if value['Gender'] == "F":
			female.append(1)

	total_values = len(ages)
	average_age = sum(ages) / total_values

	numfemale = sum(female)
	nummale = sum(male)
	perfemale = '{percent:.3%}'.format(percent=numfemale/total_values)
	permale = '{percent:.3%}'.format(percent=nummale/total_values)

	output = str(precinct) + ',' + str(average_age) + ',' + str(nummale) + ',' + str(permale) + ',' + str(perfemale) +',' +  str(numfemale)

	print output
	
	with open('precinctages.txt', 'ab+') as myfile:
	    myfile.write(output + '\r\n')

listofprecincts = [line.rstrip() for line in open('precincts.txt')]

for y in listofprecincts:
	precinctAges(y)





