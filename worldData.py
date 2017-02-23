# Group Members: Steven Chau (390464) and Paulo Zavaleta (667259)
import os
import csv
import operator
import math

# Opens the CSV source file and converts it to a 2D list
file = open('demographics_2001_2006.csv', 'r')
data = csv.reader(file)
data2d = list(data)


# A dictionary was created to make extracting the data easier later on
# It takes the GDP, the population and the GDP per capita for each country for 2001 and 2006 years
# The code creates a key for every country and inside them 2 keys for 2001 and 2006 data, each year key stores values
# If the GDP field is blank in any of the years, the key for that year is not even created 
GDP = 0.0
countrydict = {}
GDPC = 0.0
countryname = ""
for row in data2d:
	year = row[6]
	if (year == '2006' or year == '2001') and row[10] != " ":
		for countryname in row[0]:
				countryname = row[0]
				if countryname not in countrydict.keys():
					countrydict[countryname] = {}

		if row[10] != " ":
			GDPC = ((float(row[10])/float(row[7])))
			countrydict[countryname][year] = [float(row[10]), int(row[7]), GDPC]

# Question 1 starts here

# Gathers all GDP data from GDP column (row[10]) of 2006(row[6]) in CSV source file
# TotalGDP is float because data has decimal places
# Counter counts the GDP column with numerical data only, hence it is set to skip empty rows in GDP column
# It prints the sum of all GDP values divided by the counter to get the average
def GDPavg(datalist):
	totalGDP = 0.00
	counter = 0
	for row in datalist:
		if row[6] == '2006':
			if row[10] == ' ': 
				counter += 0
			else:
				totalGDP += float(row[10])
				counter += 1
	result = totalGDP/counter
	# Result is divided by one billion to make it three digits
	print "The world's average GDP in 2006 was USD %d billion. \n" % (result/1000000000)
	file.close()

GDPavg(data2d)
# Question 1 stops here

# Question 2 Starts here

# GDPdict is a dictionary made to sort the GDP capita and to include data that is missing GDP capita data
# If there is no GDP Capita for 2006, it only shows the 2001 capita and the remaining values as 0
# If there is no data for both years, it shows the country's values all as 0
# This dictionary calculates the data needed for question 2 and also the data needed for further questions
GDPdict = {}
for ckey in  countrydict:
        if len(countrydict[ckey].keys()) < 2:
            if countrydict[ckey]['2001'][2] != ' ':
                GDPdict[ckey] = (countrydict[ckey]['2001'][2], 0, 0, 0)
            else:
            	GDPdict[ckey] = (0, 0, 0, 0)
        else:
                difGDP = countrydict[ckey]['2006'][2] - countrydict[ckey]['2001'][2]
                GDPyrinc = difGDP/5
                GDPperinc = (GDPyrinc * 100)/countrydict[ckey]['2001'][2]
                GDPdict[ckey] = (countrydict[ckey]['2001'][2], countrydict[ckey]['2006'][2], GDPyrinc, GDPperinc)

# These two variables sort the GDP dictionary by GDP capita in 2001 from lowest to highest (lowsort) and highest to lowest (highsort)
# The variables are lists so it makes easier to work with the values
lowsort = sorted(GDPdict.items(), key=lambda x:x[1])
highsort = sorted(GDPdict.items(), key=lambda x:x[1], reverse = True)

lowfile = "gdp0106l.csv"
highfile = "gdp0106g.csv"

# This function takes as parameter the sorted list by 2001 GDP (lowsort and highsort) with all the 
# fields of data requested in question 2 as an input and the output parameter is the csv filename.
# It takes the sortin list and takes the first 20 elements, each element of the list contains a list with the data
# for one country, the first element of that list is the country name, the second element is another list with the 
# numeric data to be stored in the CSV file. It takes the country name and then splits the numeric data, converts 
# it to a string and add it to the countryname string then writes all the string as a row into the CSV file. Does the 
# same procedure for every country's data.
def csvsort(sortin, csvout):
	fileout = open(csvout,'w')
	for item in sortin[:20]:
		s = item[0]
		for data in item[1]:
			s += ','
			s += str("%0.2f" %data)
		s += '\n' #At this point the string is the countryname with it's correspondant numeric data
		fileout.write(s)
	fileout.close()

csvsort(lowsort, lowfile)
csvsort(highsort, highfile)

# This function prints the data stored in the CSV files formatting the data in the way indicated in the assignment.
# First, it opens the given csv file name, reads it and converts it to a 2D list.
# description. For that, we created a list with strings containing the headers of the columns of the data and a string 
# variable that indicates the currency of the GDP values. The names of countries and headers are alligned to the left.
# The numbers are alligned to right. We first print the headers with the spacing allign and formatting, then we print
# every row of the csv file also with the allign and spacing formatting.
def csvtable(csvfilename):
	csvfile = open(csvfilename, 'r')
	csvdata = csv.reader(csvfile)
	csvdata2d = list(csvdata)
	lines = "================================================================================"
	h = ["Country", "GDP/POP in 2001", "GDP/POP in 2006", "Yr Incr", "%/Year"]
	money = "USD"
	print lines
	print "%-20s %9s %17s %10s %10s" % (h[0], h[1], h[2], h[3], h[4])
	print lines
	for item in csvdata2d:
		print "%-20s %s %9s %7s %9s %12s %9s%%" % (item[0], money, item[1], money, item[2], item[3], item[4])
	print "\n"

csvtable(highfile)
csvtable(lowfile)
# question 2 ends here

# Question 3 and 4 starts here

# First, we extract the valid GDP data (no empty values) for every country in 2001 from countrydict and store it in a
# list (capdata). This list is used as the parameter for the histogram function.

capdata = []
for ckey in countrydict.keys():
        capdata.append((countrydict[ckey]['2001'][2]))
        capdata.sort()
# The function generates a category name (buckets), the bar and the frequency the GDP values fall in that specific
# bucket for the html histogram file. The arguments are the category name (label) and the frequency of the category (pixel).
# The function returns the category name plus the bar which its width is determined by the frenquency value multiplied by
# 10 and the frequency value right next to the bar, all stored in a string variable (outString) coded as a html table.
def bar(label, pixels):
    outString = '<table><tr><td width="200">%s</td>' %label
    outString += '<td width="%d" bgcolor="blue"></td>' % (pixels*10)
    outString += '<td>%d </td>' % pixels 
    outString += '</tr></table>'
    return outString

# Takes as argument a list with the frequency of each GDP per capita ordered ascendently in ranges of values that raises
# exponentialy to the power of 10. It creates 2 empty lists: htmlhead stores the headers for every bucket category (string),
# it goes for every element of the argument list and its index is used as the power value of 10 of its current bucket category.
# htmlfile is a 2D list that stores in each of its elements the header of a bucket category (string) and its frequency value,
# this list is then passed to the bar function to generate the bars in html code of each individual bucket for the html histogram.
# Each bar code of every bucket is stored in a single string file (output) that is finally writen in the html file histogram.html
def histogramhtml(histo):
	htmlhead = []
	htmlfile = []
	for n in histo:
		htmlhead.append(str(10**(histo.index(n)+1)) + " < x < " + str(10**(histo.index(n)+2)) + ":")
	for n in range(len(histo)):
		htmlfile.append([htmlhead[n], histo[n]]) # Appends the to the list the bucket header (string) and its frequency (int)
	histhtml = open('histogram.html','w')
	output = "<html><body>"
	for header,count in htmlfile:
	    output += bar(header, count)
	output += "</body></html>"
	histhtml.write(output)
	histhtml.close()
# Takes as parameter the ordered list (from bottom to top) of all the GDP Capita values of 2001 of every country. It creates a
# list that stores the frequency a GDP value is in each bucket (hist), the other variable (count) determines the index of the
# bucket list and the power value of the values range for every bucket. The function starts with the lowest GDP Capita value in
# the list and looks if it's between values to the power of 10 if it's true adds 1 to the frequency value of that bucket. If the
# value is not in the range of values of that bucket it means that is in a higher one, so it creates a new category adding 1 to
# counter, which is the index of each category and then automatically sums 1 to the value of the new bucket. It goes through all
# the values of the list. When the histogram list is completed it prints the bucket range values, goes for every element of hist
# list and prints as a string raising 10 to the power of the hist index value and index values plus 1, then multiplies every
# bucket value by the hashtag character, then prints the bucket range string formated to the right and next to it the hastags
# of that bucket. Lastly it executes the function to create the histogram in a html file passing it the hist list as argument.
def histogram(capdata):
	hist = [0]
	count = 0
	for i in capdata:
		if 1.00 < i < 10.00:
			hist[count] += 1
		if 10.00**(count + 1) < i < 10.00**(count + 2):
			hist[count] += 1		
		else:
			count += 1
			hist.append(1)
	print "Histogram of GDPs per capita in 2001 in order of magnitudes"
	print " -----------------------------------------------------------"
	for n in hist:
		firsthalf = str(10**(hist.index(n))) + "< x <" + str(10**(hist.index(n)+1))
		hashtags = n * '#'
		print "%20s: %s" % (firsthalf, hashtags)
	print "\n"
	histogramhtml(hist)
histogram(capdata)

# Question 4 ends here

# Question 5 starts here

# lifelist stores the basic information requested in the assignment description (country name, GDPC, female and male
# life expantancy) for every country from the CSV source file 2D list. If there is a blank GDP value in a country
# it sets the value to 0.
lifelist = []
for row in data2d:
	if row[6] == "2001":
		if row[10] != " ":
			lifelist.append([row[0], float(row[10])/float(row[7]), float(row[12]), float(row[13])])	
		if row[10] == " ":
			lifelist.append([row[0], 0, float(row[12]),float(row[13])])

# This function creates the life expectancy rankings for female and male populations, takes as parameter lifelist list
# index from which lifelist list will be sorted (lifelist index 2 stores the male life expectancy, index 3 is for female
# life expectancy). The list is sorted from top to bottom inside the function and stored in the life variable. The
# function goes in every of indexes of the argument's list and since all the values are ordered from bottom to top it
# appends the rank value (which starts from 1 and goes up as the it goes in the list's elements) as another value to the
# current country list. The rank variable stores the rank in life expectancy in the current country,  secondcounter
# variable is used as internal counter when 2 countries have the same life expectancy value, the same rank value is
# added and is kept the same in case the next country have the same life expectancy value, but the secondcounter
# variable goes up, it goes up until the next life expectancy value of the list is not the same as the previous one,
# sums it to the rank variable then appends that value as the rank of that country's life expectancy. If the life
# expectancy value from the current country in the list is greater than the next one it appends the rank value to that
# element in the list. In this condition it also checks if the secondcounter value is greater than 0 and if that's so it
# turns it to 0. When it reaches to the final index (which is the length of the list) it only appends the current rank
# value to it.
def rankings(positionnumber):
	highlife = sorted(lifelist, key=lambda x:x[positionnumber], reverse = True)
	secondcounter = 0
	rank = 1
	for n in range(len(highlife)):
	        if n == (len(highlife)-1):
	        		highlife[n].append(rank)
	        elif highlife[n][positionnumber] == highlife[n+1][positionnumber]:
	                highlife[n].append(rank)
	                secondcounter += 1   
	        elif highlife[n][positionnumber] > highlife[n+1][positionnumber]:
	                if secondcounter > 0:
	                	highlife[n].append(rank)
	                	rank += secondcounter
	                	rank += 1
	                	secondcounter = 0
	                else:	                           
		                highlife[n].append(rank) 
		                rank += 1       
	        else:
	        	highlife[n].append(rank)

#Call the rankings funtion giving as argument the index 2 (male) and 3 (female) of lifelist to add the life expectancy
# rankings for the female and male population inf the lifelist list.
rankings(2)
rankings(3)
# Sort by GDP Capita and store lifelist into a new list 
finallist = sorted(lifelist, key=lambda x:x[1], reverse = True)
#Create the headers and lines for the columns of the lifelist values
eqlines = "========================================================"
lifetext = "Life Expectancy Rank in Year 2001\n"
singlelines = "--------------------------------------------------------\n"
lifeh = ["Country", "M:Rank", "M:Years", "F:Rank", "F:Years"]
# Formats the columns names values
lifehf = "%8s %16s %9s %9s %8s" % (lifeh[0], lifeh[1], lifeh[2], lifeh[3], lifeh[4]) + "\n"
# Prints the lines, titles, and columns names
print eqlines + "\n" + "%35s" %(lifetext) + singlelines + lifehf + eqlines
#Prints the first 20 elements of the sorted list. The country names formatted to left and the numerical values
# with the same formatting space as the columns names.
for itemf in finallist[:20]:
	print "%-20s %3s %9s %9s %8s" % (itemf[0], itemf[4], itemf[2], itemf[5], itemf[3])




