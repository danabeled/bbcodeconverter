#BBCode to HTML Converter
import os
import re

DIRECTORY = os.getcwd()

filename = "ffxiiiguide"
BB_TAGS = ["B", "I", "U"]
HTML_TAGS = ["b", "i", "u"]
bbFile = open(filename+".txt", "r")

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
# Arguments: 	BB Tag Contents, HTML Code, Line Information
# Function: 	Converts any tags with certain BB Code information to input HTML.
# Returns: 		Updated Line information
# 
#                                                                                                  
##########################################################################################

def removeColorTagInstances(line):
	if "[COLOR=#" in line:
		print line 
		tagIndex = line.find("[COLOR=#")
		line = line[:tagIndex] + line[tagIndex+15:]
		print line
		line = line.replace("[COLOR=#","")
		line = line.replace("[/COLOR]","")
	return line


#print bbFile
i = 0
htmlCode = []
for line in bbFile:
	i = i + 1
	#print str(i) + " " + line;
	htmlCode.append(line)
bbFile.close()
paragraphTag = 0
htmlFile = open(filename+".html","w")
for line in htmlCode:
	style = ""
	i = 0
	for tag in BB_TAGS:
		line = replaceBBTag(tag,HTML_TAGS[i],line)
		i = i + 1
	line = removeColorTagInstances(line)
	line = line + "<br>"
	htmlFile.write(line)
#print htmlCode

