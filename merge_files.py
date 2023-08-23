import os
# Python program to
# demonstrate merging of
# two files

# Creating a list of filenames
filenames = ['csv_sample1.csv', 'csv_sample2.csv', 'csv_sample3.csv' ]

# Open file3 in write mode
with open('file3.txt', 'w') as outfile:

	# Iterate through list
	for names in filenames:

		# Open each file in read mode
		with open(names) as infile:

			# read the data from file1 and
			# file2 and write it in file3
			outfile.write(infile.read())

		# Add '\n' to enter data of file2
		# from next line
		#outfile.write("\n")
