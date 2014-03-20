#BBCode to HTML Converter
import os
import re

DIRECTORY = os.getcwd()

filename = "ffxiiiguide"

bbFile = open(filename+".txt", "r")

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
	line = line.replace("[B]","<b>")
	line = line.replace("[/B]","</b>")
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