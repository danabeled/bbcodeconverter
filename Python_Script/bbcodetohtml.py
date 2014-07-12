####### BBCode to HTML Converter ###############
import os
import re

class Converter: 

	def __init__(self,inputFilename,inputTable,inputDelimiter,inputOrderedList,inputUnorderedList):
		###### CHANGE FILE NAME ########################
		self.filename = inputFilename

		###### CHANGE BB_TAGS ##########################
		self.BB_TAGS = ["B", "I", "U", "TD","TR","LIST=1","LIST", "TABLE", "*","HR","URL"]
		self.HTML_TAGS = ["b", "i", "u","td","tr","ol","ul","table","li","hr","a"]

		##### BOOLS FOR STRUCTURES #####################
		self.TABLE_EXISTS = inputTable[0]
		self.LIST_UNORDERED_EXISTS = inputUnorderedList[0]
		self.LIST_ORDERED_EXISTS = inputOrderedList[0]

		##### IF TABLE EXISTS CHANGE THESE #############
		self.DELIMITER = inputDelimiter
		if self.TABLE_EXISTS == True:
			self.TABLE_STAT_STARTING_LINE = inputTable[1]
			self.TABLE_STAT_ENDING_LINE = inputTable[2]
		

		##### IF UNORDERED LIST EXISTS CHANGE THESE ####
		if self.LIST_UNORDERED_EXISTS == True:
			self.LIST_UNORDERED_KEYWORD = inputUnorderedList[1]

		##### IF ORDERED LIST EXISTS CHANGE THESE ######
		if self.LIST_ORDERED_EXISTS == True:
			self.LIST_ORDERED_KEYWORD = inputOrderedList[1]

		##### DON'T TOUCH ##############################
		self.bbFile = open(self.filename+".txt", "r")
		self.ENEMY_STATS = []
		self.DIRECTORY = os.getcwd()
		if self.TABLE_EXISTS == True:
			self.NUM_OF_STATS = self.TABLE_STAT_ENDING_LINE - self.TABLE_STAT_STARTING_LINE + 1
		self.CURRENT_LIST_SIZE = 0
		self.PREV_PARAGRAPH = False

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
	
	def readStats(self,document):
		for statNum in range(self.NUM_OF_STATS):
			#Appended the stat in the following format ABBRV, FULL_NAME to the stats list
			self.ENEMY_STATS.append(document[statNum+self.TABLE_STAT_STARTING_LINE-1].split(self.DELIMITER))

			#Remove all white space
			self.ENEMY_STATS[statNum][0] = self.ENEMY_STATS[statNum][0].strip()
			self.ENEMY_STATS[statNum][1] = self.ENEMY_STATS[statNum][1].strip()

			#Remove the line break
			self.ENEMY_STATS[statNum][1] = self.ENEMY_STATS[statNum][1][:len(self.ENEMY_STATS[statNum][1])]

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
	
	def createTable(self,lineNum, htmlCode):
		htmlCode[lineNum] = "<table class=\"content_infotable\">\n	<tr>\n		<td class=\"content_headerrow\" colspan="+str(len(self.ENEMY_STATS)) + ">" + htmlCode[lineNum][:len(htmlCode[lineNum])-1]
		htmlCode[lineNum] = htmlCode[lineNum] + "</td>\n	</tr>"
		for BBTag in self.BB_TAGS:
			if "[/"+BBTag+"]" in htmlCode[lineNum]:
				htmlCode[lineNum].replace("[/"+BBTag+"]","")
				htmlCode[lineNum] = "[/"+BBTag+"]" + htmlCode[lineNum]
		for statNum in range(self.NUM_OF_STATS):
			rows = htmlCode[lineNum+statNum+1].split(self.DELIMITER)
			try:
				newLine = "\n	<tr>\n		<td class=\"content_headerrow\">" + rows[0].strip() + "</td>\n" + "		<td class=\"content_headerrow\">" + rows[1].strip() + "</td>\n	</tr>\n"	
				if statNum + 1 == self.NUM_OF_STATS:
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
	
	def createList(self,lineNum, htmlCode, listType):
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

	def replaceBBTag(self,BBTag, HTMLTag, line):
		if "[*]" in line:
			if BBTag == "*":
				line = line[:len(line)-1] + "</li> \n"
		# print "["+BBTag+"]"
		if BBTag == "URL":
			line = line.replace("["+BBTag.lower(),"["+BBTag)
			#The following code handles finding the closing bracket of a URL tag
			#because using a replace function woudl replace all ] of other tags
			#but it is impossible to predict how long the URL will be
			lastTagFind = -1
			while line.find("["+BBTag+"=") != -1:
				print line.find("["+BBTag+"=")
				findTagEnd = line.find("["+BBTag+"=")
				while line[findTagEnd] != "]":
					findTagEnd = findTagEnd + 1
				re = list(line)
				re[findTagEnd] = ">"
				tagStart = lastTagFind = line.find("["+BBTag+"=")
				re[tagStart] = "<a href"
				re[tagStart+1] = "" 
				re[tagStart+2] = "" 
				re[tagStart+3] = ""
				line = "".join(re)

		else:
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

	def removeColorTagInstances(self,line):
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

	def removeSizeTagInstances(self,line):
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

	def endOfLineHandling(self,line):
		#print self.PREV_PARAGRAPH
		if "<li>"in line or  "<ul>" in line or "</ul>" in line or "<table>" in line or "</table>" in line or "<td>" in line or "<tr>" in line or "</td>" in line or "</tr>" in line:
			return line
		# if "<ul>" in line:
		# 	return line
		#If many characters in the line, assume a paragraph has been written and add paragraph tags
		if len(line) >= 100:
			line = "<p>"+str(line[:len(line)-1])+"</p>\n" #Add code to give line a paragraph tag
			self.PREV_PARAGRAPH = True
		#otherwise assume that it was just a small line break and add a break tag
		else:
			if "\n" in line[len(line)-1:]:
				if self.PREV_PARAGRAPH == False:
					line = str(line[:len(line)-1])+"<br>\n"
				self.PREV_PARAGRAPH = False
		return line


	######################################## MAIN EXECUTION ########################################
	def executeConversion(self):
		#Initialize the HTML line list
		htmlCode = []

		#Read Each line of BBCode from the BB File and write into a structure that will become HTML
		for line in self.bbFile:
			htmlCode.append(line)
		self.bbFile.close()

		#Read open what will become the HTML File
		htmlFile = open(self.filename+".html","w")
		lineNum = 0

		#Read stats to be read in future tables
		if self.TABLE_EXISTS == 1:
			self.readStats(htmlCode)
		table = 0
		count = 0
		listexists = 0
		#Fix each line of BBCode into HTML Code
		for line in htmlCode:
			count = count + 1
			if self.LIST_UNORDERED_EXISTS == 1 and self.LIST_UNORDERED_KEYWORD in htmlCode[lineNum].lower():
				data = self.createList(lineNum, htmlCode, "UNORDERED")
				htmlCode = data[0]
				line = htmlCode[lineNum]
				listexists = 1
				listCounter = 0

			# Checks if enemy table is about to start, doesn't check if we are on the last line of the file
			if self.TABLE_EXISTS == 1: 
				if lineNum + 1 < len(htmlCode):
					if self.ENEMY_STATS[0][0].lower() + self.DELIMITER in htmlCode[lineNum+1].lower():
						htmlCode = self.createTable(lineNum, htmlCode)
						line = htmlCode[lineNum]
						#New table found, set table boolean to true and counter to zero for paragraph handling
						table = 1
						tableCounter=0

			#Replace BB Code Tags with HTML Tags For line
			tagNum = 0
			for tag in self.BB_TAGS:
				line = self.replaceBBTag(tag,self.HTML_TAGS[tagNum],line)
				tagNum = tagNum + 1

			#Remove all BBCode tags that will not be used for EoFF's static content
			line = self.removeColorTagInstances(line)
			line = self.removeSizeTagInstances(line)

			#Handle end of line adding paragraph tag or line break where necessary
			if table == 0 and listexists == 0:
				line = self.endOfLineHandling(line)
			elif table == 1:
				tableCounter=tableCounter+1
				if tableCounter == self.NUM_OF_STATS+1:
					table=0
			elif listexists == 1:
				listCounter = listCounter + 1
				# print listCounter
				# print self.CURRENT_LIST_SIZE
				if listCounter == data[1] + 2:
					listexists = 0 

			#Write New Line to File
			htmlFile.write(line)
			# Increment Line Counter before begin handling next line
			lineNum = lineNum + 1

#Run this for no input tables, ordered lists, etc.
name = "joinstaff"
tableInfo = [False]
delim = ""
orderedlist = [False]
unorderedList = [False]
convert = Converter(name,tableInfo,delim, orderedlist, unorderedList)
convert.executeConversion()

#Run this for most inputs
# name = "ffxiiiguide"
# tableInfo = [True, 4, 8]
# delim = ":"
# orderedlist = [False]
# unorderedList = [True, "treasures"]
# convert = Converter(name,tableInfo,delim,orderedlist, unorderedList)
# convert.executeConversion()