from optparse import OptionParser   #depenency for command line options
import os                           #import os module for os.walk function
import hashlib                      #import hashlib module for those juicy hash digests
import errno

		
#############################################################################################
##Function: hashFile
##Purpose: Hashes the current file
##Returns: string
#############################################################################################
def hashFile(fname):
	F = fname
	BLOCKSIZE = 65536
	hasher = hashlib.md5() #Change this to global hash function option from command line
	try:
		with open( F, 'rb') as theFile:
			buf = theFile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = theFile.read(BLOCKSIZE)
		return hasher.hexdigest()
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
     parser = OptionParser()
     parser.add_option("-d",
                       dest="dirName",
                       help="Directory to start hashing from",
                       metavar="DIRECTORY"
                       )
     parser.add_option("-o",
					   dest="outFile",
                       help="Output file for hashing results",
                       metavar="OUTPUT_FILE"
                       )
     parser.add_option("-m",
                       dest="digest",
                       help="Desired hashing funtion (MD5,SHA256)",
                       metavar="HASHING_METHOD"
                       )

     #Create global options
     global glob_args        #arguements taken from command line
     global glob_digest      #hash function specified in command line
     global glob_dir         #directory specified in command line
     global glob_output      #output file specified in command line

     (options, args)  = parser.parse_args()
 
     #Assign command line input to global variables
     glob_digest = options.digest
     glob_dir = options.dirName
     glob_output = options.outFile
     
	 
#############################################################################################
def main():
	
	#Call getOptions to grab CLI arguments
	getOptions()
	#create a file counter to keep track of files
	fileCount = 0 
	
	#Open the output file for writing
	f = open(glob_output, "w")
	E = open("Error.log", "w")

	#Set the root directory variable
	rootDir = glob_dir 
	print ("\n" + "="*60)
	print ("Starting at root directory: " + rootDir)
	print ("="*60 + "\n")
	for dName, subList, fList in os.walk(rootDir):
		for fname in fList: 
			fileCount = fileCount + 1 #increment fileCount
			current_file = os.path.join(dName,fname) #create the current_file by joining dirName and fname to get path/file
			current_hash = hashFile(current_file) #create current_hash var by calling hashFile function on our current file 
			print ("Found file " + str(fileCount) + "...hashing...writing to " + glob_output)
			try:
				f.write( current_file + ',' + current_hash +"\n")
			except (RuntimeError, TypeError):
				print "Could not hash file: " + current_file
				E.write( "Error hashing " + current_file + "\nReason: Permission Denied\n")
if __name__ == '__main__':
    main()
