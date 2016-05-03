from nltk.corpus import wordnet as wn
import nltk
import semantic_classifier
import os

directory = "documents/files/"
all_files = os.listdir(directory)

#all_files = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt", "7.txt", "8.txt", "9.txt", "10.txt", "11.txt"]

tag_file = open("documents/tags.txt", 'r')
tags = {}
closestHypernym = {}
print "Compiling all tags..."
for line in tag_file:
	line_num = line.split(":")[0]
	tags[line_num] = []
	line_tags = line.split(":")[1].split(",")
	for tag in line_tags:
		if tag[-1] == "\n":
			tag = tag[:-1]
		tags[line_num].append(tag)
		closestHypernym[(tag, line_num)] = ""

hypernyms = {}
for i in range(len(all_files)):
	hypernyms[str(i)] = []

print "Running all classifications..."
for i in range(len(all_files)):
	print "Working on file: " + str(i) + ".txt..."
	classification = semantic_classifier.run(directory+str(i)+".txt", 2, 99, 0.5)
	hypernyms[str(i)] = classification.hypernyms
	#print hypernyms[str(i)]


print "Computing closest hypernyms..."
total_accuracy = 0.0
for i in range(len(all_files)):
	accuracy = 0.0
	for tag in tags[str(i)]:
		syn_hyp = hypernyms[str(i)][0]
		syn_tag = wn.synsets(tag)[0]
		maxSim = wn.wup_similarity(syn_hyp, syn_tag)
		if maxSim is None:
			maxSim = 0.0
		closestHypernym[(tag, str(i))] = hypernyms[str(i)][0]
		for hypernym in hypernyms[str(i)]:
			syn_hyp = hypernym
			sim = wn.wup_similarity(syn_tag, syn_hyp)
			if sim is None:
				sim = 0.0
			if sim > maxSim:
				maxSim = sim
				closestHypernym[(tag, str(i))] = hypernym
		print "File " + str(i) + ".txt: ",
		print "Tag: " + str(tag) + "; ",
		print "Closest hypernym: " + closestHypernym[(tag, str(i))].name().split(".")[0] + " = " + str(maxSim)
		accuracy += maxSim
	accuracy /= len(tags[str(i)])
	print "Accuracy for file " + str(i) + ".txt: " + str(accuracy)
	total_accuracy += accuracy

print "\n\n AVERAGE ACCURACY = " + str(total_accuracy/len(all_files))
