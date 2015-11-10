from optparse import OptionParser   #depenency for command line options
import os                           #import os module for os.walk function
import hashlib                      #import hashlib module for those juicy hash digests
import csv                          #import csv module for csv formating output file

#Function name: getOptions
#Purpose: read in options from the command line based on flags, stores options to global variables
#Flags:
#        -d directory       - Directory the user wants to start hashing from
#        -o output          - file the user wants to push results to
#        -m hash function   - hashing function the user wants to use (md5 or SHA256)


def getOptions():
    parser = OptionParser()
    parser.add_option("-d",
                      dest="dirName",
                      help="Directory to start hashing from",
                      metavar="DIRECTORY"
                      )
    parser.add_option("-o", dest="outFile",
                      help="Output file for hashing results",
                      metavar="OUTPUT_FILE"
                      )
    parser.add_option("-m", dest="digest",
                      help="Desired hashing funtion (MD5,SHA256)",
                      metavar="HASHING_METHOD"
                      )

    #Create global options
    global glob_args        #arguements taken from command line
    global glob_digest      #hash function specified in command line
    global glob_dir         #directory specified in command line
    global glob_output      #output file specified in command line

    glob_args  = parser.parse_args()

    #Figure out how to assign values in glob_args to Global Variables Below
    #glob_digest = glob_args.digest
    #glob_dir = glob_args.dirName
    #glob_output = glob_args.outFile



#Function name: walkDir
#Purpose: iterate through the desired directory obtained from getOptions, navigate through directories, hash files
#         using hashFile(), write out file name and hash using writeHash()



def walkDir():
    rootDir = 'C:\Users\mhart\Desktop\Tester' #Change this to take the global directory option from command line
    for dName, subList, fList in os.walk(rootDir):
        print('Found directory: %s' % dName)
        for fname in fileList:
            current_file = os.path.join(dirName,fname) #create the current file by joining dirName and fname to get path/file
            hashFile(current_file) #Hash the file
            writeHash(current_file) #Write out filename, hash


#Function name: hashFile
#Purpose: hash files in the filesystem
#Input: string (file path/name)

def hashFile(F):
    BLOCKSIZE = 65536
    hasher = hashlib.md5() #Change this to global hash function option from command line
    with open('F', 'rb') as theFile:
        buf = theFile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = theFile.read(BLOCKSIZE)
    print(hasher.hexdigest())

    #The above code is taken from stack overflow and is being used as a placeholder example.

#Function name: writeHash
#Purpose: write out the current file name as well as the corresponding hash
#Input:

def writeHash():
    #open csv file for writing
    csv_out = open("test.csv", 'wb') #replace "test.cvc" with global output file from command line
    writer = csv.writer(csv_out)
    writer.writerow(filename, hash) #figure out how you want to push filename and corresponding hash value 
