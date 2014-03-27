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
ENEMY_STAT_STARTING_LINE = 4
ENEMY_STAT_ENDING_LINE = 8
DELIMITER = ":"

##### DON'T TOUCH ########################
bbFile = open(filename+".txt", "r")
ENEMY_STATS = []
DIRECTORY = os.getcwd()
NUM_OF_STATS = ENEMY_STAT_ENDING_LINE - ENEMY_STAT_STARTING_LINE + 1

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  readEnemyStats    **                                                                                     
#  
# Arguments: 	Read info
# Function: 	Reads Info for enemy stats to create tables off of
# Returns: 		N/A
# 
#                                                                                                  
##########################################################################################
def readEnemyStats(document):
	for statNum in range(NUM_OF_STATS):
		#Appended the stat in the following format ABBRV, FULL_NAME to the stats list
		ENEMY_STATS.append(document[statNum+ENEMY_STAT_STARTING_LINE-1].split(DELIMITER))

		#Remove all white space
		ENEMY_STATS[statNum][0] = ENEMY_STATS[statNum][0].strip()
		ENEMY_STATS[statNum][1] = ENEMY_STATS[statNum][1].strip()

		#Remove the line break
		ENEMY_STATS[statNum][1] = ENEMY_STATS[statNum][1][:len(ENEMY_STATS[statNum][1])]

##########################################################################################
#                                                                                            
#                                                                                                
#                                                                                                
#   **  createEnemyTable    **                                                                                     
#  
# Arguments: 	Line Number, htmlCode
# Function: 	Creates Enemy Table
# Returns: 		
# 
#                                                                                                  
##########################################################################################
def createEnemyTable(lineNum, htmlCode):
	htmlCode[lineNum] = "<table class=\"content_infotable\"><tr><td class=\"content_headerrow\" colspan="+str(len(ENEMY_STATS)) + ">" + htmlCode[lineNum]
	htmlCode[lineNum] = htmlCode[lineNum] + "</td></tr>"
	for BBTag in BB_TAGS:
		if "[/"+BBTag+"]" in htmlCode[lineNum]:
			htmlCode[lineNum].replace("[/"+BBTag+"]","")
			htmlCode[lineNum] = "[/"+BBTag+"]" + htmlCode[lineNum]
	for statNum in range(NUM_OF_STATS):
		htmlCode[lineNum+statNum+1] = "<tr><td class=\"content_headerrow\">" + htmlCode[lineNum+statNum+1] + "</td></tr>"
	return htmlCode


	# <tr>
	# 	<td class="content_headerrow" width="145">Weapon</td>
	# </tr>


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
	if "[COLOR=#" in line:
		tagIndex = line.find("[COLOR=#")
		line = line[:tagIndex] + line[tagIndex+15:]
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
	if "[SIZE=" in line:
		tagIndex = line.find("[SIZE=")
		line = line[:tagIndex] + line[tagIndex+8:]
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
	if len(line) >= 100:
		line = "<p>"+str(line)+"</p>" #Add code to give line a paragraph tag
	else:
		line = str(line) + "<br>"
	return line


######################################## MAIN EXECUTION ########################################

htmlCode = []
for line in bbFile:
	htmlCode.append(line)
bbFile.close()
paragraphTag = 0
htmlFile = open(filename+".html","w")
lineNum = 0
readEnemyStats(htmlCode)
table = 0
for line in htmlCode:
	# Checks if enemy table is about to start, doesn't check if we are on the last line of the file
	if lineNum + 1 < len(htmlCode):
		if ENEMY_STATS[0][0].lower() + DELIMITER in htmlCode[lineNum+1].lower():
			htmlCode = createEnemyTable(lineNum, htmlCode)
			line = htmlCode[lineNum]
			table = 1
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
		tableCounter=1
		line = endOfLineHandling(line)
	else:
		tableCounter=tableCounter+1
		if tableCounter == NUM_OF_STATS:
			table=0

	#Write New Line to File
	htmlFile.write(line)