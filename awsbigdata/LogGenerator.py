#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 12:01:21 2019

@author: Frank

201226
This generates some fake logs by reading from a csv file and writes to /var/....log file.
usage: sudo python3 LogGenerator.py
source: AWS BigData video
original OnlineRetail.csv has 541k lines vs 10 lines here
"""

import csv
import time
import sys

sourceData = "OnlineRetail.csv"
destFileName = "/var/log/zhaleKinesisTest/%Y%m%d-%H%M%S.log" # need to create the folder manually first?
placeholder = "LastLine.txt"

def GetLineCount():
    with open(sourceData) as f:
        print("open() ok. f:" + str(f))
        for i, l in enumerate(f):
            print("enumerate():" + str(i) + ";" + str(l)) # l is the content of the line: 536365,85123A,WHITE HANGING HEART T-LIGHT HOLDER,6,12/1/2010 8:26,2.55,17850,United Kingdom
            pass
    return i # will error if empty file: UnboundLocalError: local variable 'i' referenced before assignment

# startLine: which line from source file to read
# numLines: how many lines still need to write
def MakeLog(startLine, numLines):
    print("MakeLog(): " + str(startLine) + ";" + str(numLines))
    destData = time.strftime(destFileName)
    with open(sourceData, 'r') as csvfile:
        # with open(destData, 'w') as dstfile: # (over)write
        with open(destData, 'a') as dstfile: # append
            reader = csv.reader(csvfile)
            writer = csv.writer(dstfile)
            next(reader) #skip header
            inputRow = 0
            linesWritten = 0
            for row in reader:
                inputRow += 1
                if (inputRow > startLine):
                    writer.writerow(row)
                    linesWritten += 1
                    if (linesWritten >= numLines):
                        break
            return linesWritten

print("LogGenerator started ...")

numLines = 100
startLine = 0
if (len(sys.argv) > 1):
    numLines = int(sys.argv[1])

try:
    with open(placeholder, 'r') as f:
        for line in f:
             startLine = int(line)
except IOError:
    startLine = 0

print("Writing " + str(numLines) + " lines starting at line " + str(startLine) + "\n")

totalLinesWritten = 0
linesInFile = GetLineCount()
print("linesInFile: " + str(linesInFile))

while (totalLinesWritten < numLines):
    linesWritten = MakeLog(startLine, numLines - totalLinesWritten)
    print("linesWritten:" + str(linesWritten))
    totalLinesWritten += linesWritten
    startLine += linesWritten
    if (startLine >= linesInFile):
        startLine = 0

print("Wrote " + str(totalLinesWritten) + " lines.\n")

with open(placeholder, 'w') as f:
    f.write(str(startLine))

print("LogGenerator ended successfully!")
