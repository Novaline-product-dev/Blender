import bz2

# First step is just handling files.  I haven't trained a thing yet.  
# I think the thing to do is add the punkt sentence tokenizer, then 
# iterate through the .txt files to produce 1-per-line sentences?  
# Not sure yet.  Baby steps for a while.

# Directory with the files
dirpath = './extracted/AA'

# Gets the list of files in the specified directory
files = os.listdir(dirpath)

# gets only the ones that end with .bz2
files = [file for file in files if file.endswith('.bz2')]

# loop over files ending in .bz2
for filename in files:

	# creates a string with joined paths, handles any forward slashes
    filepath = os.path.join(dirpath, filename) # to get compressed file
    newfilepath = os.path.join(dirpath, filename[:-4] + '.txt') # for output file

    # opens two files, one is blank and the other is a bz2 file opened with the
    # bz2 module 
    with open(newfilepath, 'wb') as new_file, bz2.BZ2File(filepath, 'rb') as file:
        
    	# iterates over the opened file, reading it in pieces
        for data in iter(lambda : file.read(), b''):

        	# sequentially writes pieces to the new file
            new_file.write(data)