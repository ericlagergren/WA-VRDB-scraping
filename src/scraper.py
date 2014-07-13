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

from cStringIO import StringIO
import csv
import datetime
import subprocess
import sys

vrdb = 'active.txt'

def write_file(filename, mode, data):
	with open(filename, mode) as f:
		f.write(data)

def getCities():

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	# Gets all cities in the voter reg db

	return [entry.get('RegCity') for entry in reader if entry['RegCity']]

def getPrecincts():

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

	#precincts = []

	# In Washington counties can use their own precinct codes which are the county code (e.g. King is KI) + precinct code + precinct part
	# To keep each unique we concat each part with a '+' -- this keeps the values separate but still unique

	return [str(entry.get('CountyCode')) + '+'  + str(entry.get('PrecinctCode')) + '+' + str(entry.get('PrecinctPart')) for entry in reader if entry['PrecinctCode']]

	#write_file('precincts.txt', 'ab+', str(precincts))
						
def sortLists(function, output_file, shell_script):

	num_cities = function
	num_cities = str(num_cities)

	write_file(output_file, 'ab+', num_cities)

	subprocess.call([shell_script])

def getInformation(input_file, column, output_file):

	identifier = dict.fromkeys([line.rstrip() for line in open(input_file)], 0)
	identifier_length = dict.fromkeys([line.rstrip() for line in open(input_file)], 0)
	nummale = dict.fromkeys([line.rstrip() for line in open(input_file)], 0)
	numfemale = dict.fromkeys([line.rstrip() for line in open(input_file)], 0)

	# Here we have the different quantiles
	# m denotes male, f denotes female

	fq1 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 18 - 25
	fq2 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 26 - 35
	fq3 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 36 - 45
	fq4 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 46 - 55
	fq5 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 56 - 65
	fq6 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 66 +

	mq1 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 18 - 25
	mq2 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 26 - 35
	mq3 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 36 - 45
	mq4 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 46 - 55
	mq5 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 56 - 65
	mq6 = dict.fromkeys([line.rstrip() for line in open(input_file)], 0) # 66 +

	with open(vrdb, 'r') as myfile:
		file_data = myfile.read()

	if precinct == True:
		for entry in csv.DictReader(StringIO(file_data), delimiter='\t'):
			column = str(entry['CountyCode']) + '+' + \
					str(entry['PrecinctCode']) + '+' + \
					str(entry['PrecinctPart'])
			if entry['Birthdate']:
				dates = datetime.datetime.now() - datetime.datetime.strptime(entry['Birthdate'], '%m/%d/%Y')
				age = datetime.timedelta.total_seconds(dates) / 31556952
				i = (str(entry['CountyCode']) + '+' + \
					str(entry['PrecinctCode']) + '+' + \
					str(entry['PrecinctPart']))
				print i
				try:
					identifier[i] += age
					identifier_length[i] += 1
				except KeyError:
					sys.exc_clear()
				if entry['Gender'] == "M":
					try:
						nummale[i] += 1
						if 18 <= age < 26:
							mq1[i] += 1
						elif 26 <= age < 35:
							mq2[i] += 1
						elif 36 <= age < 45:
							mq3[i] += 1
						elif 46 <= age < 55:
							mq4[i] += 1
						elif 56 <= age < 65:
							mq5[i] += 1
						elif 66 <= age:
							mq6[i] += 1
					except KeyError:
						sys.exc_clear()
				elif entry['Gender'] == "F":
					try:
						numfemale[i] += 1
						if 18 <= age < 26:
							fq1[i] += 1
						elif 26 <= age < 35:
							fq2[i] += 1
						elif 36 <= age < 45:
							fq3[i] += 1
						elif 46 <= age < 55:
							fq4[i] += 1
						elif 56 <= age < 65:
							fq5[i] += 1
						elif 66 <= age:
							fq6[i] += 1
					except KeyError:
						sys.exc_clear()
	else:
		for entry in csv.DictReader(StringIO(file_data), delimiter='\t'):
			if entry[column]:
				if entry['Birthdate']:
					dates = datetime.datetime.now() - datetime.datetime.strptime(entry['Birthdate'], '%m/%d/%Y')
					age = datetime.timedelta.total_seconds(dates) / 31556952
					i = entry[column]
					try:
						identifier[i] += age
						identifier_length[i] += 1
					except KeyError:
						sys.exc_clear()
					if entry['Gender'] == "M":
						try:
							nummale[i] += 1
							if 18 <= age < 26:
								mq1[i] += 1
							elif 26 <= age < 35:
								mq2[i] += 1
							elif 36 <= age < 45:
								mq3[i] += 1
							elif 46 <= age < 55:
								mq4[i] += 1
							elif 56 <= age < 65:
								mq5[i] += 1
							elif 66 <= age:
								mq6[i] += 1
						except KeyError:
							sys.exc_clear()
					elif entry['Gender'] == "F":
						try:
							numfemale[i] += 1
							if 18 <= age < 26:
								fq1[i] += 1
							elif 26 <= age < 35:
								fq2[i] += 1
							elif 36 <= age < 45:
								fq3[i] += 1
							elif 46 <= age < 55:
								fq4[i] += 1
							elif 56 <= age < 65:
								fq5[i] += 1
							elif 66 <= age:
								fq6[i] += 1
						except KeyError:
							sys.exc_clear()

	for key in identifier:
		if key in identifier_length:
			identifier[key] = identifier[key] / identifier_length[key]

	results = dict((k, [identifier[k], nummale.get(k), mq1.get(k), mq2.get(k), mq3.get(k), mq4.get(k), mq5.get(k), mq6.get(k), numfemale.get(k), fq1.get(k), fq2.get(k), fq3.get(k), fq4.get(k), fq5.get(k), fq6.get(k)]) for k in identifier)
	
	for key, value in results.items():
		csv.writer(open(output_file, 'ab+')).writerow([key, value])

sortLists(getCities(), 'citylist.txt', './shellsubprocess.sh')
sortLists(getPrecincts(), 'precincts.txt', './subshellprecincts.sh')

# Writes the CDs and LDs to files because they're predefined

for x in range(1,50):
	write_file('ldlist.txt', 'ab+', '%s\n' % x)

for x in range(1,11):
	write_file('cdlist.txt', 'ab+', '%s\n' % x)

# We use `precinct` as a flag to let us know when to use the first `if` portion in our getInformation method

precinct = False

getInformation('ldlist.txt', 'LegislativeDistrict', 'ldages.txt')
getInformation('cdlist.txt', 'CongressionalDistrict', 'cdages.txt')
getInformation('citylist.txt', 'RegCity', 'cityages.txt')

precinct = True

getInformation('precincts.txt', 'Precinct', 'precinctages.txt')