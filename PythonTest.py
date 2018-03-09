#Import everything here
import datetime, os
from win32com.shell import shell, shellcon


#Global variables
currentdate = datetime.datetime.now()	#Use to call for times (currentdate.year, currentdate.month, etc.)
exitflag = False
loginfo = []
operationlogpath = ''
ReadHerepath = ''


#Helper functions
def readfile(celltype, flasknumber):	#Reads ReadHere.txt, searches for celltype+flasknumber (both strings), and prints a list of chunkdata per date for a cell type + flask number
										#Assumes that celltype is a sanitized string (all lowercase)
	f = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\ReadHere.txt', 'r')	#open ReadHere.txt for reading
	print('\n')
	print('Date\t\tChecked?\tSplit?\tSplitfraction\tCell Count\tComments')
	global loginfo 
	loginfo = [celltype, flasknumber]
	for line in f:
		splitline = line.split(',')							#Seperating the list into chunks deliniated by commas. splitline[0] = cell+flasknumber, while splitline[1:] = 'date ifchecked ifsplit splitfraction cellcount comments'
		if splitline[0] == celltype + ' ' + flasknumber:	#Checks to see if current line has the correct celltype+flasknumber
			for element in splitline[1:]:					#Remember that element is a str
				chunkdata = element.split(' ')				#Now chunkdata has ['date', 'ifchecked', 'ifsplit', 'splitfraction', 'cellcount', 'comments']
				print(chunkdata[0] + '\t' + chunkdata[1] + '\t\t' + chunkdata[2] + '\t' + chunkdata[3] + '\t\t' + chunkdata[4] + '\t\t' + chunkdata[5])
			print('\n')
		else:
			print('We couldn\'t find the cell line or flask number you\'re inputting \n')
			break
	f.close()												#close ReadHere.txt
	

def do_all_the_read():
	celltype = input('What cell type? ').lower()
	flasknumber = str(input('What flask number? '))
	readfile(celltype, flasknumber)

	
def writeinfo(celltype, flasknumber, date, ifchecked, ifsplit, splitfraction, cellcount, comments):
	#Writes in new info into ReadHere.txt, all variables are strings. Doesn't print or return anything, just writes to file
	#All local variables go here
	line = ''
	newline = ''
	
	f = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\ReadHere.txt', 'r')	#open ReadHere.txt for reading and writing
	newinfo = date + ' ' + ifchecked + ' ' + ifsplit + ' ' + splitfraction + ' ' + cellcount + ' ' + comments
	for line in f:
		splitline = line.split(',')							#Seperating the list into chunks deliniated by commas. splitline[0] = cell+flasknumber, while splitline[1:] = 'date ifchecked ifsplit splitfraction cellcount comments'
		if splitline[0] == celltype + ' ' + flasknumber:	#Checks to see if current line has the correct celltype+flasknumber
			newline = line + ',' + newinfo					#newline currently equals the line and the newinfo, now we'll open the file, copy/paste the entire file, and search/replace the line with newline
	f.close()
	
	file = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\ReadHere.txt', 'r')
	filedata = file.read()
	file.close()
	
	newfiledata = filedata.replace(line, newline)
	f = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\ReadHere.txt', 'w')
	f.write(newfiledata)
	f.close()
	

def do_all_the_write():
	splitfraction = ''
	cellcount = ''
	celltype = input('What cell type? ').lower()
	flasknumber = str(input('What flask number? '))
	date = str(currentdate.day) + '/' + str(currentdate.month) + '/' + str(currentdate.year)
	ifchecked = input('Did you check these cells today? (yes/no)')
	ifsplit = input('Did you split these cells today? (yes/no)')
	if ifsplit == 'yes':
		splitfraction = str(input('What was the splitting fraction? '))
		cellcountdo = input('Did you do a cell count? (yes/no)')
		if cellcountdo == 'yes':
			cellcount = str(input('Enter the raw number from the cell count: '))
	comments = input('Enter any comments here: ')
	writeinfo(celltype, flasknumber, date, ifchecked, ifsplit, splitfraction, cellcount, comments)
	global loginfo
	loginfo = [celltype, flasknumber, date, ifchecked, ifsplit, splitfraction, cellcount, comments]
	print('Info added successfully \n')
	

def loginput(operationtype, infoneeded):	#infoneeded should contain [celltype, flasknumber, date, ifchecked, ifsplit, splitfraction, cellcount, comments], each as a string
	if operationtype == 'a':
		file = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\operationlog.txt', 'a')
		file.write('\n' + str(currentdate) + ' Appended (' + infoneeded[3] + ', ' + infoneeded[4] + ', ' + infoneeded[5] + ', ' + infoneeded[6] + ', ' + infoneeded[7] + ') onto ' + infoneeded[0] + ' flask number ' + infoneeded[1])
		file.close()
	elif operationtype == 'r':
		file = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\operationlog.txt', 'a')
		file.write('\n' + str(currentdate) + ' Read and showed data regarding ' + infoneeded[0] + ' flask number ' + infoneeded[1])
		file.close()
	elif operationtype == 'quit':
		file = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\operationlog.txt', 'a')
		file.write('\n' + str(currentdate) + ' Exited program')
		file.close
		
	
def ask_for_exit():		#Asks user if he/she wants to exit. If yes, then the exitflag is raised
	userinput = input('Exit the program? (yes/no): ')
	if userinput == 'yes' or userinput == 'Yes' or userinput == 'y' or userinput == 'YES' or userinput == 'Y':
		loginput('quit', loginfo)
		global exitflag
		exitflag = True
	else:
		exitflag = False
		print('\n-------------------------------------------------\n')
	
	
def check_if_files_exist_and_do_something_about_it():	#pretty much as it says
	FlagReadThis = True
	celllinesexhausted = False
	FlagOperationLog = True
	i = 1
	
	while FlagReadThis == True:
		try:
			f = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\ReadHere.txt', 'r')
			f.close()
			FlagReadThis = False
			break
		except IOError:
			file = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\ReadHere.txt', 'w')
			print('No data file was found. We\'ll make a new one, so please supply the cell details below. \n')
			while celllinesexhausted == False:
				userinput1 = input('Enter the name of your first cell line: ')
				userinput2 = input('Enter how many flasks you have of that cell line: ')
				i = 1
				for _ in range(int(userinput2)):
					file.write(userinput1 + ' ' + str(i) + '\n')
					i = i + 1
				doesuserwannakeepadding = input('Do you have any more cell lines to input? (yes/no): ')
				if doesuserwannakeepadding == 'no' or doesuserwannakeepadding == 'No' or doesuserwannakeepadding == 'n' or doesuserwannakeepadding == 'NO' or doesuserwannakeepadding == 'N':
					celllinesexhausted = True
			FlagReadThis = False
			file.close()

	while FlagOperationLog == True:
		try:
			file = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\operationlog.txt', 'r')
			file.close()
		except IOError:
			file = open(r'\\ad.monash.edu\home\User062\mnak0010\Desktop\Script_Stuff\Python\Cell_Check\operationlog.txt', 'w')
			file.close()
		FlagOperationLog = False
		
def find_file_paths():
	x = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
	for root, dirs, files in os.walk(x):
		for name in files:
			if name == 'operationlog.txt':
				global operationlogpath
				operationlogpath = os.path.abspath(os.path.join(root, name))
			elif name == 'ReadHere.txt':
				global ReadHerepath
				ReadHerepath = os.path.abspath(os.path.join(root, name))
	print(ReadHerepath + '\n' + operationlogpath)
	print('Done')
			

#Main function

if __name__ == '__main__':
	check_if_files_exist_and_do_something_about_it()
	while exitflag == False:
		mainchoiceprompt = input('Add new data (a), read data (r), or show filepaths (f): ')
		if mainchoiceprompt == 'a':
			do_all_the_write()
			loginput('a', loginfo)
			ask_for_exit()
		elif mainchoiceprompt == 'r':
			do_all_the_read()
			loginput('r', loginfo)
			ask_for_exit()
		elif mainchoiceprompt == 'f':
			find_file_paths()
			ask_for_exit()
	if exitflag == True:
		os._exit(0)