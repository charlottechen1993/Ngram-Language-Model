import sys
import re
import os
import string
from unigram import *
from bigram import *
from trigram import *
from preprocess import *

model = sys.argv[1]
trainfile = sys.argv[2]
devfile = sys.argv[3]
testfile = sys.argv[4]

path = trainfile

if '.txt' not in trainfile:
	train_text =[]
	ori_directory = os.getcwd()
	files = os.listdir('Holmes_Training_Data')
	os.chdir(path)
	full_train = ""
	for trainfile in files:
		with open(trainfile, 'r') as train:
			for line in train:
				print line
				full_train = "%s%s"%(full_train,line)
	filelist = os.listdir(os.getcwd())
	os.chdir(ori_directory)
else:
	with open(trainfile, 'r') as train:
		train_text = train.read()
with open(devfile, 'r') as dev:
	dev_text = dev.read()
with open(testfile, 'r') as test:
	test_text = test.read()


if '.txt' in trainfile:
	# format train input sentence
	all_train_sentence = (re.split('\n+', train_text))
else:
	all_train_sentence = (re.split('\n+', full_train))

# format test input sentence
all_test_sentence = (re.split('\n+', test_text))
# format dev input sentence
all_dev_sentence = (re.split('\n+', dev_text))

# contains all unique words in training text, exclude <s> and </s>
s = set()
type(s)
# preprocess train text; replace special character and replace unknown
s = preprocessText(train_text, all_train_sentence, all_test_sentence, all_dev_sentence)
# preprocess test file to replace word with <unk> according to unigram
all_test_sentence_cpy = replaceTestUnknown(all_train_sentence, all_test_sentence, s)

d = {}
bigram_perplexity_list = {}
# cases for each model
if model=='1':
	d = UnigramModel(all_train_sentence)
	printUnigramProb(all_train_sentence, d)
	getUnigramPerplexity(all_test_sentence, d)
	print "\n"
elif model=='2':
	# preprocess test file
	d = BigramModel(all_train_sentence)
	printBigramProb(all_train_sentence, d)
	getUnsmoothedBigramPerplexity(all_train_sentence, all_test_sentence_cpy, all_test_sentence, d)
	print "\n"
elif model=='2s':
	d = BigramModel(all_train_sentence)
	# preprocess dev file to replace word with <unk> according to unigram
	all_dev_sentence_cpy = replaceTestUnknown(all_train_sentence, all_dev_sentence, s)
	bigram_perplexity_list = getSmoothedBigramPerplexity(all_train_sentence, all_dev_sentence_cpy, all_test_sentence_cpy, all_test_sentence, True, d)
	print "\n"
elif model=='3':
	d = TrigramModel(all_train_sentence)
	getUnsmoothedTrigramPerplexity(all_train_sentence, all_test_sentence_cpy, all_test_sentence, d)
	print "\n"
elif model=='3s':
	trigram_d = TrigramModel(all_train_sentence)
	bigram_d = BigramModel(all_train_sentence)
	all_dev_sentence_cpy = replaceTestUnknown(all_train_sentence, all_dev_sentence, s)
	bigram_perplexity_list = getSmoothedBigramPerplexity(all_train_sentence, all_dev_sentence_cpy, all_test_sentence_cpy, all_test_sentence, False, bigram_d)
	getSmoothedTrigramPerplexity(all_train_sentence, all_dev_sentence_cpy, all_test_sentence_cpy, all_test_sentence, bigram_perplexity_list, trigram_d)
