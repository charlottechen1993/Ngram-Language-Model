import re
import math
from unigram import *
from bigram import *

# dictionary of dictionary: vertical - current char; horizontal - previous char
trigram_d = {}

def TrigramModel(all_sentence):
	bigram_d = {}
	bigram_d = BigramModel(all_sentence)

	for sentence in all_sentence:
		sentence = '<s> ' + sentence
		char_in_sentence = (re.split('\s+', sentence))
		
		for i in range(len(char_in_sentence)-2):
			prevprev = char_in_sentence[i]
			prev = char_in_sentence[i+1]
			cur = char_in_sentence[i+2]

			if cur not in trigram_d:
				trigram_d[cur] = {prev : {prevprev : 1}}
			elif cur in trigram_d and prev not in trigram_d[cur]:
				trigram_d[cur][prev] = {prevprev : 1}
			elif cur in trigram_d and prev in trigram_d[cur] and prevprev not in trigram_d[cur][prev]:
				trigram_d[cur][prev][prevprev] = 1
			else:
				trigram_d[cur][prev][prevprev] += 1

	print '\n=============================================='
	print '==== Unsmoothed Trigram Train Probability ===='
	print '==============================================\n'
	for cur in trigram_d:
		for prev in trigram_d[cur]:
			for prevprev in trigram_d[cur][prev]:
				prob = 0.0
				if prevprev == '<s>' and prev == '<s>':
					prob = bigram_d[cur][prev]
				else:
					prob = bigram_d[prev][prevprev]
				print cur + '|' + prev + prevprev, ' : ', trigram_d[cur][prev][prevprev], ' -- ', float(trigram_d[cur][prev][prevprev])/prob
	return trigram_d


def getUnsmoothedTrigramPerplexity(all_train_sentence, all_test_sentence, all_test_sentence_ori, trigram_d):
	trigram_s = {}
	bigram_d = {}
	bigram_d = BigramModel(all_train_sentence)
	ori_list = []
	for i in range(len(all_test_sentence_ori)):
		ori_list.insert(i, all_test_sentence_ori[i])
	count = 0
	print '\n========================================='
	print '===== Unsmoothed Trigram Perplexity ====='
	print '=========================================\n'
	for sentence in all_test_sentence:
		sentence_cpy = '<s> ' + sentence
		# entropy = 0-log(Pr(word_1))....-log(Pr(word_n))
		entropy = 0.0
		char_in_sentence = (re.split('\s+', sentence_cpy))
		infinite = False
		for i in range(len(char_in_sentence)-2):
			prevprev = char_in_sentence[i]
			prev = char_in_sentence[i+1]
			cur = char_in_sentence[i+2]
			if cur not in trigram_d:
				infinite = True
				break
			elif prev not in trigram_d[cur]:
				infinite = True
				break
			else:
				if prevprev not in trigram_d[cur][prev]:
					infinite = True
					break
				else:
					occur = 0
					if prev == '<s>' and prevprev == '<s>':
						occur = len(all_train_sentence)
					else:
						occur = bigram_d[prev][prevprev]
					tri_prob = float(trigram_d[cur][prev][prevprev])/occur
					log_prob = math.log(tri_prob, 2)
					entropy = entropy - log_prob
		if infinite == True:
			per_word_perplexity = 'infinite'
		else:
			per_word_entropy = entropy/(len(char_in_sentence)-2)
			per_word_perplexity = math.pow(2, per_word_entropy)

		print ori_list[count] + " : " + str(per_word_perplexity)
		count += 1

def getSmoothedTrigramPerplexity(all_train_sentence, all_dev_sentence_cpy, all_test_sentence_cpy, all_test_sentence_ori, bigram_perplexity_list, d):
	lamb_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

	bigram_d = {}
	bigram_d = BigramModel(all_train_sentence)

	ori_list = []
	for i in range(len(all_test_sentence_ori)):
		ori_list.insert(i, all_test_sentence_ori[i])
	count = 0
	print '\n========================================='
	print '====== Smoothed Trigram Perplexity ======'
	print '=========================================\n'
	# print bigram_perplexity_list
	choosen_lambda = 0
	weight = -1
	for lamb in lamb_list:
		avg_perplexity = 0;
		for sentence in all_test_sentence_cpy:
			sentence_cpy = '<s> ' + sentence
			# entropy = 0-log(Pr(word_1))...-log(Pr(word_n))
			entropy = 0.0
			char_in_sentence = (re.split('\s+', sentence_cpy))
			for i in range(len(char_in_sentence)-2):
				prevprev = char_in_sentence[i]
				prev = char_in_sentence[i+1]
				cur = char_in_sentence[i+2]
				tri_prob = 0
				if cur not in trigram_d:
					tri_prob = (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
				elif prev not in trigram_d[cur]:
					tri_prob = (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
				else:
					if prevprev not in trigram_d[cur][prev]:
						tri_prob = (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
					else:
						occur = 0
						if prev == '<s>' and prevprev == '<s>':
							occur = len(all_train_sentence)
						else:
							occur = bigram_d[prev][prevprev]
						tri_prob = choosen_lambda*(float(trigram_d[cur][prev][prevprev])/occur) + (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
				log_prob = math.log(tri_prob, 2)
				entropy = entropy - log_prob
			per_word_entropy = entropy/(len(char_in_sentence)-2)
			per_word_perplexity = math.pow(2, per_word_entropy)
			avg_perplexity += per_word_perplexity
		
		if weight == -1:
			weight = avg_perplexity
			choosen_lambda = lamb
		else:
			if weight > avg_perplexity:
				weight = avg_perplexity
				choosen_lambda = lamb
	print "Lambda: ", choosen_lambda


	for sentence in all_test_sentence_cpy:
		sentence_cpy = '<s> ' + sentence
		# entropy = 0-log(Pr(word_1))...-log(Pr(word_n))
		entropy = 0.0
		char_in_sentence = (re.split('\s+', sentence_cpy))
		for i in range(len(char_in_sentence)-2):
			prevprev = char_in_sentence[i]
			prev = char_in_sentence[i+1]
			cur = char_in_sentence[i+2]
			tri_prob = 0
			if cur not in trigram_d:
				tri_prob = (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
			elif prev not in trigram_d[cur]:
				tri_prob = (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
			else:
				if prevprev not in trigram_d[cur][prev]:
					tri_prob = (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
				else:
					occur = 0
					if prev == '<s>' and prevprev == '<s>':
						occur = len(all_train_sentence)
					else:
						occur = bigram_d[prev][prevprev]
					tri_prob = choosen_lambda*(float(trigram_d[cur][prev][prevprev])/occur) + (1-choosen_lambda)*bigram_perplexity_list[prev][prevprev]
			log_prob = math.log(tri_prob, 2)
			entropy = entropy - log_prob
		per_word_entropy = entropy/(len(char_in_sentence)-2)
		per_word_perplexity = math.pow(2, per_word_entropy)

		print ori_list[count] + " : " + str(per_word_perplexity)
		count+=1

