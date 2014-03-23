#BBCode to HTML Converter
import os
import re

DIRECTORY = os.getcwd()

filename = "ffxiiiguide"

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

print bbFile
i = 0
htmlCode = []
for line in bbFile:
	i = i + 1
	print str(i) + " " + line;
	htmlCode.append(line)
bbFile.close()
paragraphTag = 0
htmlFile = open(filename+".html","w")
for line in htmlCode:
	style = ""
	line = replaceBBTag("B","b",line)
	if "[COLOR=#800080]" in line:
		style = style + "color:purple "
		paragraphTag = 1
		line = line.replace("[COLOR=#800080]","")
		print "true"
	if "[COLOR=#ffd700]" in line:
		style = style + "color:purple "
		paragraphTag = 1
		line = line.replace("[COLOR=#ffd700]","")
		print "true"
	line = line.replace("[/COLOR]","")
	if paragraphTag == 1 and "\n" in line:
		line = "<p style=\""+style+"\">" + line
		line = line.replace("\n","</p>\n")
		paragraphTag = 0
	else:
		line = line + "<br>"
	htmlFile.write(line)
#print htmlCode

