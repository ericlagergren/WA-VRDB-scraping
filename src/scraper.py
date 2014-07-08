#!/usr/bin/env python

'''
 ----------------------------------------------------------------------------
 "THE BEER-WARE LICENSE" (as modified by Eric Lagergren) (Revision 43):
 Eric Lagergren <contact@ericlagergren.com> wrote this file. As long as you retain this notice you
 can do whatever you want with this stuff. If we meet some day, and you think
 this stuff is worth it, you can buy me a beer in return
 Also, you can't use this if you're a Democrat, Liberal, Socialist, or really anybody who doesn't like Republican.
Well, I *might* make an exception for Socialists because it's not like they win anything outside of Seattle...
 ----------------------------------------------------------------------------
 '''

from __future__ import division
import csv
import datetime
import subprocess
import gc

import cherrypy
import dowser

def start(port):
    cherrypy.tree.mount(dowser.Root())
    cherrypy.config.update({
        'environment': 'embedded',
        'server.socket_port': port
    })
    cherrypy.server.quickstart()
    cherrypy.engine.start(blocking=False)

vrdb = 'active.txt'

# Write headings to three output files

with open('legdata.txt', 'wb+') as myfile:
    myfile.write('LegDist,AvgAge,NumMales,PerMales,Q1,Q2,Q3,Q4,Q5,Q6,NumFemales,PerFemales,Q1,Q2,Q3,Q4,Q5,Q6' + '\r\n')

with open('citydata.txt', 'wb+') as myfile:
    myfile.write('City,AvgAge,NumMales,PerMales,NumFemales,Q1,Q2,Q3,Q4,Q5,Q6,PerFemales,Q1,Q2,Q3,Q4,Q5,Q6' + '\r\n')

with open('precinctdata.txt', 'wb+') as myfile:
    myfile.write('Precinct,AvgAge,NumMales,PerMales,NumFemales,Q1,Q2,Q3,Q4,Q5,Q6,PerFemales,Q1,Q2,Q3,Q4,Q5,Q6' + '\r\n')

with open('congressdata.txt', 'wb+') as myfile:
    myfile.write('Precinct,AvgAge,NumMales,PerMales,NumFemales,Q1,Q2,Q3,Q4,Q5,Q6,PerFemales,Q1,Q2,Q3,Q4,Q5,Q6' + '\r\n')

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

	# Here we have the different quantiles
	# m denotes male, f denotes female

	fq1 = 0 # 18 - 25
	fq2 = 0 # 26 - 35
	fq3 = 0 # 36 - 45
	fq4 = 0 # 46 - 55
	fq5 = 0 # 56 - 65
	fq6 = 0 # 66 +

	mq1 = 0 # 18 - 25
	mq2 = 0 # 26 - 35
	mq3 = 0 # 36 - 45
	mq4 = 0 # 46 - 55
	mq5 = 0 # 56 - 65
	mq6 = 0 # 66 +

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
		age = datetime.timedelta.total_seconds(dates) / 31556952
		ages.append(age)
		if value['Gender'] == "M":
			nummale += 1
			if 18 <= age < 26:
				mq1 += 1
			if 26 <= age < 35:
				mq2 += 1
			if 36 <= age < 45:
				mq3 += 1
			if 46 <= age < 55:
				mq4 += 1
			if 56 <= age < 65:
				mq5 += 1
			if 66 <= age:
				mq6 += 1
		if value['Gender'] == "F":
			numfemale += 1
			if 18 <= age < 26:
				fq1 += 1
			if 26 <= age < 35:
				fq2 += 1
			if 36 <= age < 45:
				fq3 += 1
			if 46 <= age < 55:
				fq4 += 1
			if 56 <= age < 65:
				fq5 += 1
			if 66 <= age:
				fq6 += 1

	# This defines the ages. Takes the sum of all the ages and divides it by the total values
	# It also takes the total number of each gender and divides that by the total
	# This gives us a percentage with 3 decimal places

	total_values = len(ages)
	average_age = sum(ages) / total_values

	perfemale = '{percent:.3%}'.format(percent=numfemale/total_values)
	permale = '{percent:.3%}'.format(percent=nummale/total_values)

	results = str(identifier) + ',' + str(average_age) + ',' + str(nummale) + ',' + str(permale) + ',' + str(mq1)+ ',' + str(mq2) + ',' + str(mq3) + ',' + str(mq4) + ',' + str(mq5) + ',' + str(mq6) + ',' + str(numfemale) + ',' +  str(perfemale) + str(fq1)+ ',' + str(fq2) + ',' + str(fq3) + ',' + str(fq4) + ',' + str(fq5) + ',' + str(fq6)
	
	# Prints output to console so we can see our script is working
	# `with... as myfile` appends each line to with \r\n so we can work with both unix and windows

	print results

	with open(output_file, 'ab+') as myfile:
	    myfile.write(results + '\r\n')

	gc.collect()	

# We define set useprecincts to false because we turn it to true later so we can use a modified for-loop to handle the precincts

useprecincts = False

# Gets Congressional District data

for e in xrange(1,11):
	getInformation('CongressionalDistrict', e, 'congressdata.txt')

# Gets Legislative District data

for r in xrange(1, 50):
	getInformation('LegislativeDistrict', r, 'legdata.txt')

# Gets city data

getCities()
sortLists(getCities, 'citylist.txt', './shellsubprocess.sh')
listofcities = [line.rstrip() for line in open('citylist.txt')]

for i in listofcities:
	getInformation('RegCity', i, 'citydata.txt')
# Gets precinct data

getPrecincts()
sortLists(getPrecincts, 'precinctlist.txt', './subshellprecincts.sh')
listofprecincts = [line.rstrip() for line in open('precincts.txt')]
useprecincts = True

# I'm passing 'a' because getInformation takes 3 args when I only need to pass two
# I suppose I *could* implement *args, but this works for such a simple scraper script

for c in listofprecincts:
	getInformation('a', c, 'precinctdata.txt')
