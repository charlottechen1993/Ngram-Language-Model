import re
import math
from unigram import *
# dictionary of dictionary: vertical - current char; horizontal - previous char
bigram_d = {}
unigram_d = {}

def printBigramProb(all_sentence, bigram_d):
	unigram_d = UnigramModel(all_sentence)
	print '\n==================================='
	print '===== Bigram Train Probability ===='
	print '===================================\n'
	for cur in bigram_d:
		for prev in bigram_d[cur]:
			print cur + '|' + prev + ' : ', bigram_d[cur][prev], ' -- ', float(bigram_d[cur][prev])/unigram_d[prev]


def BigramModel(all_sentence):
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
			if cur not in bigram_d:
				bigram_d[cur] = {prev : 1}
			else:
				if prev not in bigram_d[cur]:
					bigram_d[cur][prev] = 1
				else:
					bigram_d[cur][prev] = bigram_d[cur][prev]+1
	return bigram_d

def getUnsmoothedBigramPerplexity(all_train_sentence, all_test_sentence, all_test_sentence_ori, bigram_d):
	bigram_s = {}
	for char in bigram_d:
		bigram_s[char] = 0
		for child in bigram_d[char]:
			bigram_s[char] += bigram_d[char][child]
		bigram_s['<s>'] = len(all_train_sentence)

	ori_list = []
	for i in range(len(all_test_sentence_ori)):
		ori_list.insert(i, all_test_sentence_ori[i])
	count = 0
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
			if cur not in bigram_d:
				infinite = True
				break
			else:
				if prev not in bigram_d[cur]:
					infinite = True
					break
				else:
					# print cur, ' | ', prev, ' : ', float(bigram_d[cur][prev]), " / ", bigram_s[prev]
					pair_prob = float(bigram_d[cur][prev])/bigram_s[prev]
					log_prob = math.log(pair_prob, 2)
					entropy = entropy - log_prob

		if infinite == True:
			per_word_perplexity = 'infinite'
		else:
			per_word_entropy = entropy/(len(char_in_sentence)-1)
			per_word_perplexity = math.pow(2, per_word_entropy)

		print ori_list[count] + " : " + str(per_word_perplexity)
		count += 1


def getSmoothedBigramPerplexity(all_train_sentence, all_dev_sentence, all_test_sentence, all_test_sentence_ori, bigram_d):
	lamb_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
	bigram_s = {}
	for char in bigram_d:
		bigram_s[char] = 0
		for child in bigram_d[char]:
			bigram_s[char] += bigram_d[char][child]
		bigram_s['<s>'] = len(all_train_sentence)

	ori_list = []
	for i in range(len(all_test_sentence_ori)):
		ori_list.insert(i, all_test_sentence_ori[i])
	count = 0
	print '\n======================================='
	print '====== Smoothed Bigram Perplexity ====='
	print '=======================================\n'

	# Use dev file to find best lamba value
	unigram_d = UnigramModel(all_train_sentence)
	total = 0
	for word in unigram_d:
		if word != '<s>':
			total += unigram_d[word]
	
	weight = -1
	choosen_lamb = 0
	for lamb in lamb_list:
		avg_perplexity = 0;
		for sentence in all_dev_sentence:
			entropy = 0.0
			char_in_sentence = (re.split('\s', sentence))
			
			for i in range(len(char_in_sentence)-1):
				prev = char_in_sentence[i]
				cur = char_in_sentence[i+1]
				pair_prob = 0
				if cur not in bigram_d:
					pair_prob = (1-lamb)*(float(unigram_d[cur])/total)
				else:
					if prev not in bigram_d[cur]:
						pair_prob = (1-lamb)*(float(unigram_d[cur])/total)
					else:
						# print cur, ' | ', prev, ' : ', float(bigram_d[cur][prev]), " / ", bigram_s[prev]
						pair_prob = lamb*(float(bigram_d[cur][prev])/bigram_s[prev]) + (1-lamb)*(float(unigram_d[cur])/total)
				log_prob = math.log(pair_prob, 2)
				entropy = entropy - log_prob

			per_word_entropy = entropy/(len(char_in_sentence)-1)
			per_word_perplexity = math.pow(2, per_word_entropy)
			avg_perplexity += per_word_perplexity
		if weight == -1:
			weight = avg_perplexity
		else:
			if weight > avg_perplexity:
				weight = avg_perplexity
				choosen_lamb = lamb
	print "Lambda: ", choosen_lamb

	# use the found lambda to find the perplexity for the test file
	for sentence in all_test_sentence:
		entropy = 0.0
		char_in_sentence = (re.split('\s', sentence))
		
		for i in range(len(char_in_sentence)-1):
			prev = char_in_sentence[i]
			cur = char_in_sentence[i+1]
			pair_prob = 0
			if cur not in bigram_d:
				pair_prob = (1-choosen_lamb)*(float(unigram_d[cur])/total)
			else:
				if prev not in bigram_d[cur]:
					pair_prob = (1-choosen_lamb)*(float(unigram_d[cur])/total)
				else:
					pair_prob = choosen_lamb*(float(bigram_d[cur][prev])/bigram_s[prev]) + (1-choosen_lamb)*(float(unigram_d[cur])/total)
			# print cur, " | ", prev, " = ", pair_prob
			log_prob = math.log(pair_prob, 2)
			entropy = entropy - log_prob

		per_word_entropy = entropy/(len(char_in_sentence)-1)
		per_word_perplexity = math.pow(2, per_word_entropy)

		print ori_list[count] + " : " + str(per_word_perplexity)
		count += 1



