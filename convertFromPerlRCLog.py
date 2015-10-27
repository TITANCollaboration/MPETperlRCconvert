import fnmatch
import time
import datetime
#import subprocess
import os
import os.path

# open PerlRC.log
f = open('/titan/data5/mpet/PerlRC.log')

# get lines
lines = f.readlines()

f.close()

# the last entry in this list is the beginning of the last scan
filtered = fnmatch.filter(lines,'=== Number of runs in this scan is *===\n')
#print filtered[-1]

# get the last index:
i = 0
while True:
	i += 1
	if lines[-i] == filtered[-1]:
		break

lastScan = lines[-i:]

# get rid of '#' and '>' from run number. Also split the string
lastScan = [l.replace('#','') for l in lastScan]
lastScan = [l.replace('>','') for l in lastScan]
lastScan = [l.replace('===',' ') for l in lastScan] # this insures that all lines have more than one element
lastScan = [l.split(' ') for l in lastScan]

#print lastScan

filesToConvert = []
for i in range(0,len(lastScan)):
	if lastScan[i][1].isdigit():
		filesToConvert.append(lastScan[i][1])

#print filesToConvert

# Get the date the run was started on
filtered = fnmatch.filter(lines,'=== NEW PerlRC scan at * ===\n')

dateLine = filtered[-1].split(' ')
s = dateLine[7]+" "+dateLine[8]+" "+dateLine[9]
t = time.strptime(s,"%b %d, %Y")[0:3]
dateStart = datetime.date(t[0],t[1],t[2])
dateTomorrow = dateStart + datetime.timedelta(days=1)

# convert the files
date = dateStart
#print date.strftime("%Y%m%d")
for i in range(0,len(filesToConvert)):
	fpath = "/titan/data5/mpet/"+date.strftime("%Y%m%d")+"/"
	fname = "run"+filesToConvert[i]+".mid"
	# check file is there
	ff = fpath+fname
	#print ff
	if os.path.exists(ff) == False: #try tomorrow's date
		date = dateTomorrow
		fpath = "/titan/data5/mpet/"+date.strftime("%Y%m%d")+"/"
	#subprocess.call(["m2e",ff])
	os.system("m2e"+" -d/titan/data5/mpet/S1374/ "+ff)
