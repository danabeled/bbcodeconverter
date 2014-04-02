#BBCode to HTML Converter
import os
import re

###### CHANGE FILE NAME ##################
filename = "ffxiiiguide"


###### CHANGE BB_TAGS ####################
BB_TAGS = ["B", "I", "U"]
HTML_TAGS = ["b", "i", "u"]

##### CHECK FOR TABLES ###################
TABLE_EXISTS = 1

##### IF TABLE EXISTS CHANGE THESE #######
TABLE_STAT_STARTING_LINE = 4
TABLE_STAT_ENDING_LINE = 8
DELIMITER = ":"

##### DON'T TOUCH ########################
bbFile = open(filename+".txt", "r")
ENEMY_STATS = []
DIRECTORY = os.getcwd()
NUM_OF_STATS = TABLE_STAT_ENDING_LINE - TABLE_STAT_STARTING_LINE + 1

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  readStats    **                                                                                     
#  
# Arguments: 	Read info
# Function: 	Reads Info for enemy stats to create tables off of
# Returns: 		N/A
# 
#                                                                                                  
##########################################################################################
def readStats(document):
	for statNum in range(NUM_OF_STATS):
		#Appended the stat in the following format ABBRV, FULL_NAME to the stats list
		ENEMY_STATS.append(document[statNum+TABLE_STAT_STARTING_LINE-1].split(DELIMITER))

		#Remove all white space
		ENEMY_STATS[statNum][0] = ENEMY_STATS[statNum][0].strip()
		ENEMY_STATS[statNum][1] = ENEMY_STATS[statNum][1].strip()

		#Remove the line break
		ENEMY_STATS[statNum][1] = ENEMY_STATS[statNum][1][:len(ENEMY_STATS[statNum][1])]

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  createTable    **                                                                                     
#  
# Arguments: 	Line Number, htmlCode
# Function: 	Creates Enemy Table
# Returns: 		
# 
#                                                                                                  
##########################################################################################
def createTable(lineNum, htmlCode):
	htmlCode[lineNum] = "<table class=\"content_infotable\">\n	<tr>\n		<td class=\"content_headerrow\" colspan="+str(len(ENEMY_STATS)) + ">" + htmlCode[lineNum][:len(htmlCode[lineNum])-1]
	htmlCode[lineNum] = htmlCode[lineNum] + "</td>\n	</tr>"
	for BBTag in BB_TAGS:
		if "[/"+BBTag+"]" in htmlCode[lineNum]:
			htmlCode[lineNum].replace("[/"+BBTag+"]","")
			htmlCode[lineNum] = "[/"+BBTag+"]" + htmlCode[lineNum]
	for statNum in range(NUM_OF_STATS):
		rows = htmlCode[lineNum+statNum+1].split(DELIMITER)
		try:
			newLine = "\n	<tr>\n		<td class=\"content_headerrow\">" + rows[0].strip() + "</td>\n" + "		<td class=\"content_headerrow\">" + rows[1].strip() + "</td>\n	</tr>"
			htmlCode[lineNum+statNum+1] = newLine
		except:
			if len(rows) == 1:
				print "Unable to break data in lines " + str(lineNum+statNum+2)
	return htmlCode

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  replaceBBTag    **                                                                                     
#  
# Arguments: 	BB Tag Contents, HTML Code, Line Information
# Function: 	Converts any tags with certain BB Code information to input HTML.
# Returns: 		Updated Line information
# 
#                                                                                                  
##########################################################################################

def replaceBBTag(BBTag, HTMLTag, line):
	line = line.replace("["+BBTag+"]","<"+HTMLTag+">")
	line = line.replace("[/"+BBTag+"]","</"+HTMLTag+">")
	return line

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  removeColorTagInstances    **                                                                                     
#  
# Arguments: 	Line Information
# Function: 	Removes any tags with color BB Code information
# Returns: 		Updated Line information
# 
#                                                                                                  
##########################################################################################

def removeColorTagInstances(line):
	#Remove openning tag if it exists
	if "[COLOR=#" in line:
		tagIndex = line.find("[COLOR=#")
		line = line[:tagIndex] + line[tagIndex+15:]
	#Remove closing tag if it exists
	if "[/COLOR]" in line: 
		line = line.replace("[/COLOR]","")
	return line

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  removeSizeTagInstances    **                                                                                     
#  
# Arguments: 	Line Information
# Function: 	Removes any tags with size BB Code information
# Returns: 		Updated Line information
# 
#                                                                                                  
##########################################################################################

def removeSizeTagInstances(line):
	#Remove openning tag if it exists
	if "[SIZE=" in line:
		tagIndex = line.find("[SIZE=")
		line = line[:tagIndex] + line[tagIndex+8:]
	#Remove closing tag if it exists
	if "[/SIZE]" in line:
		line = line.replace("[/SIZE]","")
	return line

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  endOfLineHandling    **                                                                                     
#  
# Arguments: 	Line Information
# Function: 	Handles if at the end of a line what type of tag we should be adding
# Returns: 		Updated Line information
# 
#                                                                                                  
##########################################################################################

def endOfLineHandling(line):
	#If many characters in the line, assume a paragraph has been written and add paragraph tags
	if len(line) >= 100:
		line = "<p>"+str(line)+"</p>" #Add code to give line a paragraph tag

	#otherwise assume that it was just a small line break and add a break tag
	else:
		line = str(line) + "<br>"
	return line


######################################## MAIN EXECUTION ########################################

#Initialize the HTML line list
htmlCode = []

#Read Each line of BBCode from the BB File and write into a structure that will become HTML
for line in bbFile:
	htmlCode.append(line)
bbFile.close()

#Read open what will become the HTML File
htmlFile = open(filename+".html","w")
lineNum = 0

#Read stats to be read in future tables
if TABLE_EXISTS == 1:
	readStats(htmlCode)
table = 0
count = 0
#Fix each line of BBCode into HTML Code
for line in htmlCode:
	count = count + 1
	print str(count) + " " + line
	# Checks if enemy table is about to start, doesn't check if we are on the last line of the file
	if lineNum + 1 < len(htmlCode):
		if ENEMY_STATS[0][0].lower() + DELIMITER in htmlCode[lineNum+1].lower():
			htmlCode = createTable(lineNum, htmlCode)
			line = htmlCode[lineNum]
			table = 1
			tableCounter=0
	# Increment Line Counter
	lineNum = lineNum + 1

	#Replace BB Code Tags with HTML Tags For line
	tagNum = 0
	for tag in BB_TAGS:
		line = replaceBBTag(tag,HTML_TAGS[tagNum],line)
		tagNum = tagNum + 1

	#Remove all BBCode tags that will not be used for EoFF's static content
	line = removeColorTagInstances(line)
	line = removeSizeTagInstances(line)

	#Handle end of line adding paragraph tag or line break where necessary
	if table == 0:
		line = endOfLineHandling(line)
	else:
		tableCounter=tableCounter+1
		print "NUM OF STATS: " + str(NUM_OF_STATS+1)
		print "TABLE COUNTER: " + str(tableCounter)
		if tableCounter == NUM_OF_STATS+1:
			table=0

	#Write New Line to File
	htmlFile.write(line)