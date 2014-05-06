####### BBCode to HTML Converter ###############
import os
import re

###### CHANGE FILE NAME ########################
filename = "storyffxv"

###### CHANGE BB_TAGS ##########################
BB_TAGS = ["B", "I", "U", "TD","TR","LIST=1","LIST", "TABLE", "*","HR"]
HTML_TAGS = ["b", "i", "u","td","tr","ol","ul","table","li","hr"]

##### BOOLS FOR STRUCTURES #####################
TABLE_EXISTS = False
LIST_UNORDERED_EXISTS = 1
LIST_ORDERED_EXISTS = 0

##### IF TABLE EXISTS CHANGE THESE #############
TABLE_STAT_STARTING_LINE = 4
TABLE_STAT_ENDING_LINE = 8
DELIMITER = ":"

##### IF UNORDERED LIST EXISTS CHANGE THESE ####
LIST_UNORDERED_KEYWORD = "treasures"

##### IF ORDERED LIST EXISTS CHANGE THESE ######
LIST_ORDERED_KEYWORD = False

##### DON'T TOUCH ##############################
bbFile = open(filename+".txt", "r")
ENEMY_STATS = []
DIRECTORY = os.getcwd()
NUM_OF_STATS = TABLE_STAT_ENDING_LINE - TABLE_STAT_STARTING_LINE + 1
CURRENT_LIST_SIZE = 0
PREV_PARAGRAPH = False

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
# Function: 	Creates Table Tags
# Returns: 		New HTML code
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
			newLine = "\n	<tr>\n		<td class=\"content_headerrow\">" + rows[0].strip() + "</td>\n" + "		<td class=\"content_headerrow\">" + rows[1].strip() + "</td>\n	</tr>\n"	
			if statNum + 1 == NUM_OF_STATS:
				newLine = newLine + "</table>\n"
			htmlCode[lineNum+statNum+1] = newLine
		except:
			if len(rows) == 1:
				print "Unable to break data in lines " + str(lineNum+statNum+2)
	return htmlCode

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  createList    **                                                                                     
#  
# Arguments: 	Line Number, htmlCode
# Function: 	Creates List tags
# Returns: 		New HTML Code
# 
#                                                                                                  
##########################################################################################
def createList(lineNum, htmlCode, listType):
	count=0
	while len(htmlCode[lineNum+count+1]) <= 2:
		count = count + 1
	spaces = count
	count = 0
	while len(htmlCode[lineNum+count+spaces+1]) > 2:
		htmlCode[lineNum+count+spaces+1] = "	<li>" +  htmlCode[lineNum+count+spaces+1]
		htmlCode[lineNum+count+spaces+1] = htmlCode[lineNum+count+spaces+1][:len(htmlCode[lineNum+count+spaces+1])-1] + "</li>\n"
		count = count + 1
	if listType == "UNORDERED":
		htmlCode[lineNum+spaces+1] = "<ul>\n" + htmlCode[lineNum+spaces+1]
		htmlCode[lineNum+count+spaces+1] = htmlCode[lineNum+count+spaces+1][:len(htmlCode[lineNum])-1] + "</ul>\n" 
		#print htmlCode[lineNum+count+1]
	data = [htmlCode, count]
	
	return data

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
	if "[*]" in line:
		if BBTag == "*":
			line = line[:len(line)-1] + "</li> \n"
	# print "["+BBTag+"]"
	line = line.replace("["+BBTag+"]","<"+HTMLTag+">")
	if BBTag != "*" and BBTag !=  "HR":
		line = line.replace("[/"+BBTag+"]","</"+HTMLTag+">")
	elif BBTag == "HR":
		# print "hit"
		line = line.replace("[/"+BBTag+"]","")
	# print line
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
	print PREV_PARAGRAPH
	if "<li>"in line or  "<ul>" in line or "</ul>" in line or "<table>" in line or "</table>" in line or "<td>" in line or "<tr>" in line or "</td>" in line or "</tr>" in line:
		return line
	# if "<ul>" in line:
	# 	return line
	#If many characters in the line, assume a paragraph has been written and add paragraph tags
	if len(line) >= 100:
		line = "<p>"+str(line[:len(line)-1])+"</p>\n" #Add code to give line a paragraph tag
		# PREV_PARAGRAPH = True
	#otherwise assume that it was just a small line break and add a break tag
	else:
		if "\n" in line[len(line)-1:]:
			if PREV_PARAGRAPH == False:
				line = str(line[:len(line)-1])+"<br>\n"
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
listexists = 0
#Fix each line of BBCode into HTML Code
for line in htmlCode:
	count = count + 1
	if LIST_UNORDERED_EXISTS == 1 and LIST_UNORDERED_KEYWORD in htmlCode[lineNum].lower():
		data = createList(lineNum, htmlCode, "UNORDERED")
		htmlCode = data[0]
		line = htmlCode[lineNum]
		listexists = 1
		listCounter = 0

	# Checks if enemy table is about to start, doesn't check if we are on the last line of the file
	if TABLE_EXISTS == 1: 
		if lineNum + 1 < len(htmlCode):
			if ENEMY_STATS[0][0].lower() + DELIMITER in htmlCode[lineNum+1].lower():
				htmlCode = createTable(lineNum, htmlCode)
				line = htmlCode[lineNum]
				#New table found, set table boolean to true and counter to zero for paragraph handling
				table = 1
				tableCounter=0

	#Replace BB Code Tags with HTML Tags For line
	tagNum = 0
	for tag in BB_TAGS:
		line = replaceBBTag(tag,HTML_TAGS[tagNum],line)
		tagNum = tagNum + 1

	#Remove all BBCode tags that will not be used for EoFF's static content
	line = removeColorTagInstances(line)
	line = removeSizeTagInstances(line)

	#Handle end of line adding paragraph tag or line break where necessary
	if table == 0 and listexists == 0:
		line = endOfLineHandling(line)
	elif table == 1:
		tableCounter=tableCounter+1
		if tableCounter == NUM_OF_STATS+1:
			table=0
	elif listexists == 1:
		listCounter = listCounter + 1
		# print listCounter
		# print CURRENT_LIST_SIZE
		if listCounter == data[1] + 2:
			listexists = 0 

	#Write New Line to File
	htmlFile.write(line)
	# Increment Line Counter before begin handling next line
	lineNum = lineNum + 1