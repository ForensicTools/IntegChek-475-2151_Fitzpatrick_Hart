#IntegFunctions.py


from optparse import OptionParser   	#depenency for command line options
import os                       	#import os module for os.walk function
import hashlib                      	#import hashlib module for those juicy hash digests
import errno		         	#import errno  module for error handling
import system 				#import system module for handling system calls
import urllib2				#import urllib2 module for creating URL's
import time				#import time module for managing time
import datetime 			#import datetime  module for prettier time outputs
import fileinput			#import fileinput module for file things
import shutil				#import shutul module for advanced file manipulation
from tempfile import mkstemp		#import mkstemp from tempfile module for handling tempfiles 
from shutil import Move 		#import move from shututil module for jankiness
from os import remove, close	 	#import remove, close from os for handling files
from os import path 			#import path from os module for path parsing
import json	 			#import json module cause everyone love json

#############################################################################################
#Constant Variables for Meta-Scan  API

global GLOB_APIKEY
global GLOB_HASHURL
global GLOB_HASHRESULTURL
global GLOB_UPURL

#Metascan API key
GLOB_APIKEY = 'cc4b5689ebd080c09606708c127645f4'   
#Metascan API hash lookup URL                   
GLOB_HASHURL = 'https://hashlookup.metascan-online.com/v2/hash/'
#Metascan API hash/file result URL
GLOB_HASHRESULTURL = 'https://metascan-online.com/en/scanresult/file/'  
#Metascan API file scan upload URL
GLOB_UPURL = 'https://scan.metascan-online.com/v2/file'        

#############################################################################################

#START OF FUNCTIONS

#############################################################################################
##Function: updateFile
##Purpose: Updates the .html file for visual representation of data
##Returns: string
#############################################################################################
def updateFile(data1, data2, data3, data4):
	##
	##README
	##
	##You need to replace the path to your python directory. This can vary from system to system but generally should fall under C:\PythonXX
	
	#makes copy of base index.html file
	shutil.copyfile('C:\Python27\Visual\index.html', 'C:\Python27\Visual\index.html.tmp')

	#calls replace function and modifies index.html.tmp file to update data passed into function
	replace("C:\Python27\Visual\index.html.tmp", "data-actual=0.9 indicator-widget></div><!--rep1-->", "data-actual=" + str(data1) + " indicator-widget></div><!--rep1-->")
	replace("C:\Python27\Visual\index.html.tmp", "data-actual=0.90 indicator-widget></div><!--rep2-->", "data-actual=" + str(data2) + " indicator-widget></div><!--rep2-->")
	replace("C:\Python27\Visual\index.html.tmp", "data-actual=0.2 indicator-widget></div><!--rep3-->" , "data-actual=" + str(data3) + " indicator-widget></div><!--rep2-->")
	replace("C:\Python27\Visual\index.html.tmp", "data-actual=0.05 indicator-widget></div><!--rep4-->", "data-actual=" + str(data4) + " indicator-widget></div><!--rep4-->")
	
	#generate date time variable
	dt = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
	
	#create variables for index.html.tmp file and report file name (using dt variable)
	src = 'C:\Python27\Visual\index.html.tmp'
	dst = 'C:\\Python27\\Visual\\report'+dt+'.html'

	#renames index.html.tmp file to new report name
	shutil.move(src,dst)
	
#############################################################################################

#############################################################################################
##Function: replace
##Purpose: replaces function to assist UpdateFile function in changing data
##Returns: string
#############################################################################################
def replace(file_path, pattern, subst):
    
    #Create temp file
    fh, abs_path = mkstemp()
    
    #Loops through and writes old file to new temporary file
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)

    #Remove original file
    remove(file_path)

    #Move new file
    move(abs_path, file_path)

#############################################################################################

#############################################################################################
##Function: hashFile
##Purpose: Hashes the current file
##Returns: string
#############################################################################################
def hashFile(fname):

	#Declares $F variable, filename passed to function
	F = fname

	#Declares $BLOCKSIZE variable, 65536 bytes
	BLOCKSIZE = 65536

	#Declare $hasher variable, 
	hasher = hashlib.md5() 	#---->TODO Change this to global hash function option from command line
	
	#hash the file passed to the function
	try:
		with open( F, 'rb') as theFile:
			buf = theFile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = theFile.read(BLOCKSIZE)
		return hasher.hexdigest()

	#Error handling
	except IOError, ioex:
		print "Error Hashing File: " + F
		print 'errno:', ioex.errno
		print 'err code:', errno.errorcode[ioex.errno]
		print 'err message:', os.strerror(ioex.errno)
	
#############################################################################################

#############################################################################################
##Function: getOptions
##Purpose: Reads in command line arguments from the user and assigns them to global variables 
##Returns: None
#############################################################################################
def getOptions():
     
	#Decalre $parser variable, creates an instance of OptionParser
     parser = OptionParser()
     
     #Add parser option for directory
     parser.add_option("-d",
                       dest="dirName",
                       help="Directory to start hashing from",
                       metavar="DIRECTORY"
                       )
     #Add parser option for output file
     parser.add_option("-o",
					   dest="outFile",
                       help="Output file errors",
                       metavar="OUTPUT_FILE"
                       )
     #Add parser option for desired hash function
     parser.add_option("-m",
                       dest="digest",
                       help="Desired hashing funtion (MD5,SHA256)",
                       metavar="HASHING_METHOD"
                       )

     #Create global options
     global glob_args        #arguments taken from command line
     global glob_digest      #hash function specified in command line
     global glob_dir         #directory specified in command line
     global glob_output      #output file specified in command line

     #magic
     (options, args)  = parser.parse_args()
 
     #Assign command line input to global variables
     glob_digest = options.digest
     glob_dir = options.dirName
     glob_output = options.outFile
     
	 
#############################################################################################

#############################################################################################
##Function: reqUrl()
##Purpose: takes hash and creates URL to request feedback from Metascan-Online
##Returns: string
#############################################################################################
def makeReq(hash):
	
	#declare $requestUrl variable, using constant and hash passed to function
	requestUrl = GLOB_HASHURL + hash
	
	#create actual request
	request = urllib2.Request(requestUrl)

	#add APIKEY to request
	request.add_header('apikey', GLOB_APIKEY)
	
	#declare $hashResult, assign response from request
	try:
		hashResult = urllib2.urlopen(request).read().decode("utf-8")
	
	#Error handling
	except urllib2.HTTPError, e:
		
		#Error code for API key limit
		if "403" in str(e.code):
			print "Oh no! You've reached your API key limit!\n\nYour Current File was: \n\n" + current_file + "\n\nRestart from that directory in one hour."
			#pause
			time.sleep(8)
			#call doMath to exit program
			doMath()
	
	return hashResult

#############################################################################################	

#############################################################################################
##Function: processResult()
##Purpose: takes the result from Meta-Scan and parses for file status (Infected, Suspicious, Clean)
##Returns: string
#############################################################################################

#declare global variables for file count
glob_c = 0 	#c for clean
glob_i = 0	#i for infected
glob_s = 0	#s for suspicious
glob_u = 0	#u for uknown

def processResult(requestResult):
	
	#search results for "clean"
	if "Clean" in requestResult:
		global glob_c								#make variable global
		c.write(current_file + " is clean\n")		#Write out that file is clean
		glob_c = glob_c + 1							#increment counter
	elif "Infected" in requestResult:
		global glob_i								#make variable global
		i.write(current_file + " is infected\n")	#Write out that file is infected
		glob_i = glob_i + 1							#increment counter
	elif "Suspicious" in requestResult:
		global glob_s                          	 	#make variable global
		s.write(current_file + " is suspicious\n")	#Write out that file is suspicious
		glob_s = glob_s + 1							#increment counter
	elif "Not Found" in requestResult:
		global glob_u 															#make variable global							
		f.write(current_file + "\nHASH WAS NOT FOUND...NEED TO UPLOAD FILE\n")  #Write file out to log file
		glob_u = glob_u + 1 													#increment counter
	else:
		pass

#############################################################################################	

#############################################################################################
##Function: doMath
##Purpose: does math for visuals and exits the program
##Returns: none
#############################################################################################
def doMath():

	#does the math things.
	integrity_data = (float(glob_c) + float(glob_s) + float(glob_u)) / (float(fileCount))
	cleaned_data = (float(glob_c))	/ (float(fileCount))
	infected_data = (float(glob_i)) / (float(fileCount))
	suspicious_data = (float(glob_s)) / (float(fileCount))
	updateFile(integrity_data,cleaned_data,infected_data,suspicious_data)
	sys.exit(0)
	
#############################################################################################

#############################################################################################
##Function: processFile
##Purpose: handles the uploading deal.
##Returns: none
#############################################################################################
def processFile(current_file):

	#create current_hash var by calling hashFile function on current_file
	current_hash = hashFile(current_file) 
	#print current working hash
	print "current working hash is....    " + current_hash + "\n"
	#assign $requestResullt, assign result of makeReq
	requestResult = makeReq(current_hash)
	#call process request on requestResult 
	processResult(requestResult)

#############################################################################################

def main():
	
	
	#Call getOptions to grab CLI arguments
	getOptions()

	#Open Log Files
	global f
	global c
	global i
	global s

	c = open("Clean_Files.log", "w")
	i = open("Infected_Files.log", "w")
	s = open("Suspicious_Files.log", "w")
	f = open(glob_output, "w")

	#create a file counter to keep track of files
	global fileCount
	fileCount = 0 
	
	#Set the root directory variable
	rootDir = glob_dir 
	print ("\n" + "="*100)
	print ("Starting at root directory: " + rootDir)
	print ("="*100+ "\n")
	time.sleep(5)
	
	#Start walking through file system
	for dName, subList, fList in os.walk(rootDir):

		for fname in fList: 

			#create the current_file by joining dirName and fname to get path/file
			global current_file
			current_file = os.path.join(dName,fname) 
			#increment file count
			fileCount = fileCount + 1 

			#Condition if file is .exe
			if '.exe' in current_file:
				processFile(current_file)

			#condition if file is .ini
			elif '.ini' in current_file:
				processFile(current_file)

			#Condition if file is .dll
			elif '.dll' in current_file:
				processFile(current_file)
			
			else:
				pass
	doMath()
	
if __name__ == '__main__':
    main()
