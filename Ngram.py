import sys
import re
import string
from unigram import *
from bigram import *
from trigram import *
from preprocess import *

model = sys.argv[1]
trainfile = sys.argv[2]
devfile = sys.argv[3]
testfile = sys.argv[4]

with open(trainfile, 'r') as train:
	train_text = train.read()
with open(devfile, 'r') as dev:
	dev_text = dev.read()
with open(testfile, 'r') as test:
	test_text = test.read()
 
# format train input sentence
all_train_sentence = (re.split('\n+', train_text))
# format test input sentence
all_test_sentence = (re.split('\n+', test_text))

# contains all unique words in training text, exclude <s> and </s>
s = set()
type(s)
# preprocess train text; replace special character and replace unknown
s = preprocessText(train_text, all_train_sentence, all_test_sentence)

d = {}
# cases for each model
if model=='1':
	d = UnigramModel(all_train_sentence)
	getUnigramPerplexity(all_test_sentence, d)
	print "\n"
elif model=='2':
	# preprocess test file
	replaceTestUnknown(all_train_sentence, all_test_sentence, s)
	d = BigramModel(all_train_sentence)
	getUnsmoothedBigramPerplexity(all_train_sentence, all_test_sentence, d)
	print "\n"
elif model=='2s':
	total3 = BigramModel(all_train_sentence)
	getSmoothedBigramPerplexity(all_test_sentence, total3)
elif model=='3':
	Trigram()
elif model=='3s':
	TriBiUni()




