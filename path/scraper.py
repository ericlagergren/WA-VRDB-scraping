#!/usr/bin/env python

'''
 ----------------------------------------------------------------------------
 "THE BEER-WARE LICENSE" (as modified by Eric Lagergren) (Revision 43.69):
 Eric Lagergren <contact@ericlagergren.com> wrote this file. As long as you
 retain this notice you can do whatever you want with this stuff. If we meet
 some day, and you think this stuff is worth it, you can buy me a beer in
 return.
 ----------------------------------------------------------------------------
'''

import argparse
from cStringIO import StringIO
import csv
from functools import wraps
import datetime
import subprocess
import sys

init = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Sorts Washington\'s VRDB by Leg.'
                                             ' District, Con. District, city, '
                                             'and precinct',
                                 epilog='e.g. ./scraper.py "201205Delimited '
                                 'Active.txt"')
parser.add_argument('filename', type=str, help="Path to WA VRDB")
args = parser.parse_args()

# vrdb takes cli file input, e.g. script.py file.txt

vrdb = args.filename


def timed(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        start = datetime.datetime.now()
        result = f(*args, **kwds)
        elapsed = datetime.datetime.now() - start
        print "> %s took %s to finish" % (f.__name__, elapsed)
        return result
    return wrapper


def write_file(filename, mode, data):
    with open(filename, mode) as f:
        f.write(data)


@timed
def getCities():

    reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

    # Gets all cities in the voter reg db

    return [entry.get('RegCity') for entry in reader if entry['RegCity']]


@timed
def getPrecincts():

    reader = csv.DictReader(open(vrdb, 'rb'), delimiter='\t')

    '''
    In Washington counties can use their own precinct codes which are the
    county code (e.g. King is KI) + precinct code + precinct part
    To keep each unique we concat each part with a '+' -- this keeps the
    values separate but still unique
    '''

    # return [str(entry.get('CountyCode')) + '+' + str(entry.get('PrecinctCode'))
    #        for entry in reader if entry['PrecinctCode']]

    return ['{0}+{1}'.format(entry.get('CountyCode'), entry.get('PrecinctCode'))
            for entry in reader if entry['PrecinctCode']]


@timed
def sortLists(function, output_file, shell_script):

    num_cities = function
    num_cities = str(num_cities)

    write_file(output_file, 'ab+', num_cities)

    subprocess.call([shell_script])


@timed
def getInformation(input_file, column, output_file):

    prefix = column

    if precinct is True:
        prefix = 'Precinct'
    else:
        pass

    print 'Parsing %s data...' % prefix

    identifier = dict.fromkeys([line.rstrip() for line in open(input_file)], 0)
    identifier_length = dict.fromkeys(
        [line.rstrip() for line in open(input_file)], 0)
    nummale = dict.fromkeys([line.rstrip() for line in open(input_file)], 0)
    numfemale = dict.fromkeys([line.rstrip() for line in open(input_file)], 0)

    # Here we have the different quantiles
    # m denotes male, f denotes female

    fq1 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 18 - 25
    fq2 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 26 - 35
    fq3 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 36 - 45
    fq4 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 46 - 55
    fq5 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 56 - 65
    fq6 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 66 +

    mq1 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 18 - 25
    mq2 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 26 - 35
    mq3 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 36 - 45
    mq4 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 46 - 55
    mq5 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 56 - 65
    mq6 = dict.fromkeys([line.rstrip()
                         for line in open(input_file)], 0)  # 66 +

    with open(vrdb, 'r') as myfile:
        file_data = myfile.read()

    for entry in csv.DictReader(StringIO(file_data), delimiter='\t'):
        if precinct is True:
            i = '{0}+{1}'.format(entry['CountyCode'], entry['PrecinctCode'])
            prefix = 'Precinct'
        else:
            i = entry[column]
        if entry['Birthdate']:
            dates = datetime.datetime.now() - datetime.datetime.strptime(
                entry['Birthdate'], '%m/%d/%Y')
            age = datetime.timedelta.total_seconds(dates) / 31556952
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

    results = dict((k, [identifier[k], nummale.get(k), mq1.get(k), mq2.get(k),
                        mq3.get(k), mq4.get(k), mq5.get(k), mq6.get(k),
                        numfemale.get(k), fq1.get(k), fq2.get(k), fq3.get(k),
                        fq4.get(k), fq5.get(k), fq6.get(k)])
                   for k in identifier)

    heading = ('%s,AverageAge,NumberMale,Q1,Q2,Q3,Q4,Q5,Q6,NumFemale,Q1,'
               'Q2,Q3,Q4,Q5,Q6\n') % prefix

    write_file(output_file, 'ab+', heading)

    print 'Writing {0} data to {1}.'.format(prefix, output_file)

    for key, value in results.items():
        csv.writer(open(output_file, 'ab+')).writerow([key, value])

    print 'Done writing {0} data to {1}.'.format(prefix, output_file)

print 'Fetching data... \nFetching cities.'

sortLists(getCities(), 'citylist.txt', './shellsubprocess.sh')

print '1/4: Cities fetched. \nNow fetching precincts.'

sortLists(getPrecincts(), 'precinctlist.txt', './subshellprecincts.sh')

print '2/4: Precincts fetched. \nNow fetching Legislative Districts.'

# Writes the CDs and LDs to files because they're predefined

for x in range(1, 50):
    write_file('ldlist.txt', 'ab+', '%s\n' % x)

print('3/4: Legislative Districts fetched. \nNow fetching Congressional '
      'Districts.')

for x in range(1, 11):
    write_file('cdlist.txt', 'ab+', '%s\n' % x)

print "4/4: Done fetching data."


# We use `precinct` as a flag to let us know when to use the first `if`
# portion in our getInformation method

precinct = False

print 'Parsing strings... '

getInformation('ldlist.txt', 'LegislativeDistrict', 'ldages.txt')
getInformation('cdlist.txt', 'CongressionalDistrict', 'cdages.txt')
getInformation('citylist.txt', 'RegCity', 'cityages.txt')

precinct = True

getInformation('precinctlist.txt', 'Precinct', 'precinctages.txt')

print 'Cleaning up files... '

subprocess.call(['./final.sh'])

print 'Files cleaned. Use `cd results/` for results.'
print 'Script took %s to execute' % str(datetime.datetime.now() - init)
