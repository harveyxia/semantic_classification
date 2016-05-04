import os
import noun_extractor

directory = "documents/files/"
all_files = os.listdir(directory)

avg_len = 0.
avg_nouns = 0.
avg_distinct_nouns = 0.
for my_file in all_files:
	fin = open(directory+my_file, 'r')
	for line in fin:
		line = line.split(" ")
		avg_len += len(line)
	num_nouns = noun_extractor.get_nouns(directory+my_file)
	for item in num_nouns.keys():
		avg_distinct_nouns +=1
		avg_nouns += num_nouns[item]

avg_len /= len(all_files)
avg_nouns /= len(all_files)
avg_distinct_nouns /= len(all_files)
print "Average length of file: " + str(avg_len)
print "Average number of nouns: " + str(avg_nouns)
print "Average number of distinct nouns: " + str(avg_distinct_nouns)