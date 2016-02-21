import re
import math
# dictionary to store occurence of each word
d = {}

def printUnigramProb(all_sentence, d):
	total = 0;
	for sentence in all_sentence:
		char_in_sentence = (re.split('\s+', sentence))
		for char in char_in_sentence:
			# if not <s> increment total
			if char != '<s>':
				total += 1
	print '\n======================================'
	print '====== Unigram Train Probability ====='
	print '======================================\n'
	for word in d:
		print word + " : ", d[word], " -- ", str(float(d[word])/total)

def UnigramModel(all_sentence):
	total = 0;
	# ===================
	# Contruct dictionary
	# ===================
	# iterate through each sentence
	for sentence in all_sentence:
		char_in_sentence = (re.split('\s+', sentence))
		# update each word in each sentence in dictionary
		for char in char_in_sentence:
			# if not <s> increment total
			if char != '<s>':
				total += 1
			if char in d:
				d[char] = d[char]+1
			else:
				d[char] = 1
	return d

def getUnigramPerplexity(all_sentence, d):
	total = 0
	for c in d:
		if c != '<s>':
			total += d[c]

	print '\n==============================='
	print '====== Unigram Perplexity ====='
	print '===============================\n'
	for sentence in all_sentence:
		# entropy = 0-log(Pr(word_1))....-log(Pr(word_n))
		entropy = 0.0
		
		char_in_sentence = (re.split('\s', sentence))
		for char in char_in_sentence:
			log_prob = 0.0
			# Pr(<s>) is always going to be 1
			if char == '<s>':
				continue
			# <unk> characters
			elif char not in d:
				char_prob = float(d['<unk>'])/total
				log_prob = math.log(char_prob, 2)
				entropy = entropy - log_prob
			# in dictionary characters
			else:
				char_prob = float(d[char])/total
				log_prob = math.log(char_prob, 2)
				entropy = entropy - log_prob

		per_word_entropy = entropy/(len(char_in_sentence)-1)
		per_word_perplexity = math.pow(2, per_word_entropy)

		print sentence + " : " + str(per_word_perplexity)

