#!/usr/bin/python

import matplotlib.pyplot as plt  #a module for plotting stuff
import re                        #for regex

print ("\n\n**************************************************************************************\n"
           "Welcome to the CIGAR_CONOISSEUR, a program that converts cigar strings from SAM format\n"
           "alignments into percent sequence identities and plots them. Useful for visualizing the\n"
           "alignments from different sources against the same genomic reference.\n"
           "**************************************************************************************\n\n")

### First, define a function #############################################################

def cigar_smoker(file_name):
	"This function converts the CIGAR strings of SAM into a percent identities"
	
	### Part I, get cigar strings from .sam file.

	cigars = []
	try:
	
		for line in open(file_name):
			if not line.startswith('@'):
				line = line.strip().split()
			if not line[5] == "*" and not line[5] == "D" and not line[5] == "N":
				cigars.append(line[5])
			                                        
	except IOError:
		raise ValueError("file does not exist (blows a puff of smoke)")          

	### In Part II two we need to accomplish three things:                   

	ident = []

	for cig in cigars:
		matches = 0
		length = 0
		breakdown = re.findall('\d+|\D+', cig) #split each cigar string into a list of numbers and chars
	
		### 1) find the total length of the aligned segment: all M's, N's, I's, S's, etc.
	
		nums = breakdown[::2]     # extract all list items at even positions
		for integer in nums:
			length += int(integer)          #sum all the values under the length variable
                                        # must convert number strings to actual integers		
		### 2) just the length of the matches (M's)
	
		symbols = breakdown[1::2] # extract all list items at odd positions
		counter = 0
		for match in symbols:
			if match == "M":
				matches += int(nums[counter])  #sum just the M values
			counter += 1
			
		### 3) Calculate the percent identity: 100 * M / total length
		
		ident.append(100 * matches / length)
		
	return ident
	file_name.close()
	
########### End of Function #############################################################

### Now, ask for .sam files and check for user errors.

number_of = raw_input("\n\nHow many .sam files do you want to plot?\nThe max is three "
                      "because any more than that is just too messy.\nSo what will it be?: ") 

fname = raw_input("\n\nNow, enter %s .sam file(s), or the paths to each file, "
                      "separated by spaces: " % number_of)

if len(fname) == 0:
	print ("Hmm... you didn't enter anything. (blows a puff of smoke)\n"
	       "Come back when you are ready.")
	sys.exit()       
	
files = fname.split()

if len(files) > 3:
	print ("Sorry, too many files,  (blows a puff of smoke)"
	       "three or less please.")
	sys.exit()
	
for file in files:
	if not file.endswith(".sam"):
		print ("I don't think this is a SAM file,  (blows a puff of smoke)\n" 
		       "make sure that it ends with .sam")
		sys.exit()		       

### convert input data into percent identities

data = []

for F in files:
	alignment = cigar_smoker(F)
	data.append(alignment)
	
### Time to plot

if number_of == "3" or number_of == "three" or number_of == "Three":
	plt.plot(data[0], 'bs', data[1], 'ro', data[2], 'g^')
	plt.ylabel('perecnt identity of read alignments')
	plt.text(50, 80, "%s" % files[0], color='blue')
	plt.text(50, 75, "%s" % files[1], color='red')
	plt.text(50, 70, "%s" % files[2], color='green')
	plt.show()
	
elif number_of == "2" or number_of == "two" or number_of == "Two":
	plt.plot(data[0], 'bs', data[1], 'ro')
	plt.ylabel('perecnt identity of read alignments')
	plt.text(50, 80, "%s" % files[0], color='blue')
	plt.text(50, 75, "%s" % files[1], color='red')
	plt.show()
	
elif number_of == "1" or number_of == "one" or number_of == "One":
	plt.plot(data[0], 'bs')
	plt.ylabel('perecnt identity of read alignments')
	plt.text(50, 80, "%s" % files[0], color='blue')
	plt.show()

else:
	raise ValueError("\n\nSorry, there seems to be a problem with the number of files entered"
	                 "(blows a puff of smoke)\n"
	                 "I need '1' or 'two' or 'Three', in one of those forms.\n")





       
    
    
