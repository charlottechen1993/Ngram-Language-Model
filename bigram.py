import re
import math
from unigram import *
# dictionary of dictionary: vertical - current char; horizontal - previous char
d = {}
unigram_d = {}
def BigramModel(all_sentence):
	unigram_d = UnigramModel(all_sentence)
	# =======================
	# Contruct 2-d dictionary
	# =======================
	# iterate through each sentence
	for sentence in all_sentence:
		char_in_sentence = (re.split('\s+', sentence))
		# update each word in each sentence in dictionary
		for i in range(len(char_in_sentence)-1):
			prev = char_in_sentence[i]
			cur = char_in_sentence[i+1]
			if cur not in d:
				d[cur] = {prev : 1}
			else:
				if prev not in d[cur]:
					d[cur][prev] = 1
				else:
					d[cur][prev] = d[cur][prev]+1
	
	print '\n=============================================='
	print '===== Unsmoothed Bigram Train Probability ===='
	print '==============================================\n'
	print d, "\n"
	for cur in d:
		for prev in d[cur]:
			print cur + '|' + prev + ' : ', d[cur][prev], ' -- ', float(d[cur][prev])/unigram_d[prev]
	return d

def getUnsmoothedBigramPerplexity(all_train_sentence, all_test_sentence, bigram_d):
	s = {}
	for char in bigram_d:
		s[char] = 0
		for child in bigram_d[char]:
			s[char] += bigram_d[char][child]
		s['<s>'] = len(all_train_sentence)
	print s

	print '\n========================================='
	print '====== Unsmoothed Bigram Perplexity ====='
	print '=========================================\n'
	for sentence in all_test_sentence:
		# entropy = 0-log(Pr(word_1))....-log(Pr(word_n))
		entropy = 0.0
		char_in_sentence = (re.split('\s', sentence))
		infinite = False
		for i in range(len(char_in_sentence)-1):
			prev = char_in_sentence[i]
			cur = char_in_sentence[i+1]
			if cur not in d:
				# <unk>|<unk>
				# if prev not in d['<unk>']:
				# 	if '<unk>' not in d['<unk>']:
				infinite = True
				break
				# 	else:
				# 		pair_prob = float(d['<unk>']['<unk>'])/s['<unk>']
				# 	log_prob = math.log(pair_prob, 2)
				# 	entropy = entropy - log_prob
				# # previous|<unk>
				# else:
				# 	pair_prob = float(d['<unk>'][prev])/s[prev]
				# 	log_prob = math.log(pair_prob, 2)
				# 	entropy = entropy - log_prob
			else:
				# <unk>|cur
				if prev not in d[cur]:
					infinite = True
					break
				# prev/cur
				else:
					pair_prob = float(d[cur][prev])/s[prev]
					log_prob = math.log(pair_prob, 2)
					entropy = entropy - log_prob

		if (infinite == True):
			per_word_perplexity = 'infinite'
		else:
			per_word_entropy = entropy/(len(char_in_sentence)-1)
			per_word_perplexity = math.pow(2, per_word_entropy)

		print sentence + " : " + str(per_word_perplexity)

def getSmoothedBigramPerplexity(all_test_sentence, d):
	print '\n======================================='
	print '====== Smoothed Bigram Perplexity ====='
	print '=======================================\n'



