#!/usr/bin/env python

'''
 ----------------------------------------------------------------------------
 "THE BEER-WARE LICENSE" (Revision 42):
 Eric Lagergren <contact@ericlagergren.com> wrote this file. As long as you retain this notice you
 can do whatever you want with this stuff. If we meet some day, and you think
 this stuff is worth it, you can buy me a beer in return
 ----------------------------------------------------------------------------
 '''

import csv
import datetime
import subprocess

vrdb = 'active.txt'

def legDistrictAges(ld):

	reader = csv.DictReader(open(vrdb, 'rb'), delimiter= '\t')

	legdistrict = []
	ages = []

	for row in reader:
		if row['LegislativeDistrict'] == str(ld):	
			legdistrict.append(row)

	for x,value in enumerate(legdistrict):
		dates = datetime.datetime.now() - datetime.datetime.strptime(value['Birthdate'], '%m/%d/%Y')
		ages.append(datetime.timedelta.total_seconds(dates) / 31556952)

	total_values = len(ages)
	average_age = sum(ages) / total_values
	output = str(ld) + ',' + str(average_age)
	
	print output

	with open('ldages', 'ab+') as myfile:
	    myfile.write(output + '\r\n')

for i in xrange(1, 49):
	legDistrictAges(i)


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

	for row in reader:
		if row['RegCity'] == city:
			cityages.append(row)

	for x,value in enumerate(cityages):
		dates = datetime.datetime.now() - datetime.datetime.strptime(value['Birthdate'], '%m/%d/%Y')
		ages.append(datetime.timedelta.total_seconds(dates) / 31556952)

	total_values = len(ages)
	average_age = sum(ages) / total_values
	output = str(city) + ',' + str(average_age)

	print output
	
	with open('cityages.txt', 'ab+') as myfile:
	    myfile.write(output + '\r\n')

listofcities = [line.rstrip() for line in open('citylist.txt')]

for v in listofcities:
	cityAges(v)