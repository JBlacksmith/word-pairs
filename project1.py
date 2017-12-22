import csv
import re
import copy
from itertools import islice, izip
from collections import Counter
from string import punctuation
from operator import itemgetter

#This function formats the file to be a list of strings instead of its standard format. This helps with removing punctation in later parts of the code
def getFile(file):
	lines = []
	for line in file:
		lines.append(line)
	return lines
#This function counts the number of sentence ending punctuation marks in order to determine the number of sentences in the file.
def getSentences(fileLines):
	countSentences = 0
	for line in fileLines:
		countSentences += line.count(". ") + line.count("! ") + line.count("? ")
	print("There are ", countSentences, "sentences.")
#This function determines when "the" or "The" begins a sentence by checking for all instances in which a punctuation mark is followed by that word.
def sentenceStart(fileLines):
	theCount = 0
	for line in fileLines:
		theCount += line.count(". The") + line.count(". the") + line.count("! The") + line.count("! the") + line.count("? The") + line.count("! the")
	print("There are ", theCount, "sententeces that begin with 'the'.")

#This function uses regular expressions to find all words that appear next to one another using izip and islice to make tuples of these words. Then it determines the frequency at which each of the pairs occur.
def countPairs(fileLines):
	N = 1
	words = re.findall("\w+", str(fileLines))
	pairs = Counter(izip(words, islice(words, 1, None)))
	top_words = sorted(pairs.iteritems(), key=itemgetter(1), reverse=True)[:N]
	for word, frequency in top_words:
		print("%s: %d" % (word, frequency))

#This counts the total number of words in the file after removing punctuation with the getWords() function.
def wordCount(fileLines):
    nwords = len(getWords(fileLines))	
    return nwords

#This function is used to remove special characters from words.
def fix(string):
	newstring = ""
	if string[0] == "\'":
		string = string[1:]
	if string[-1] == "\'":
		string = string[: -1]
	for c in string:
		if not c in "\".?[]()!,*;:":
			newstring += c
	return newstring
#This function formats the words using fix() to remove all special characters and reconstruct the string. It also makes it lowercase and removes instances of "--" that appear in the text to separate two words.
def getWords(fileLines):
	newlines = []
	for line in fileLines:
		newlines.append(line.replace("--", " "))
	words = []
	for line in newlines:
		words += [fix(word) for word in line.lower().split()]
	return words

#This function sorts each word by frequency of appearance and creates a csv file with the percentage of each word and frequency of occurrence. It also accounts for punctuation using the fix() function and makes all the words lowercase to avoid duplicates.
def countWords(fileLines):
    nwords = wordCount(fileLines)	   
    words = {}
    for line in fileLines:	
        for w in map(fix,line.lower().split()):
            words[w] = words.get(w, 0) + 1
    sortedWords = sorted(words.iteritems(), key=itemgetter(1), reverse=True)[0:]	
    myfile = open('results.csv', 'w')
    wr = csv.writer(myfile)
    for w, c in sortedWords:
		percentage = format(((c*1.0)/nwords), '7.9f')
		printList = [w, c, percentage]
		wr.writerow(printList)
        	
    myfile.close()

#This callls all of the functions to produce the otput.
filename = "text.txt"
file = open(filename, 'r')
fileLines = getFile(file)
wordList = getWords(fileLines)
print("There are ", wordCount(fileLines), "words")
file.seek(0,0)
getSentences(fileLines)
file.seek(0,0)
sentenceStart(fileLines)
file.seek(0,0)
countPairs(wordList)
countWords(wordList)
file.close()


