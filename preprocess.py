import re
import string

# find unknown assuming k = 1
def replaceUnknown(train_text, all_train_sentence, k):
	s = set()
	type(s)
	# traverse doc and put words in set
	for i in range(len(all_train_sentence)):
		char_in_sentence = (re.split('\s+', all_train_sentence[i]))
		for char in char_in_sentence:
			s.add(char)
	s.remove('<s>')
	s.remove('</s>')
	# find the occurence of each word
	for word in s:
		if train_text.count(word)<=k:
			for i in range(len(all_train_sentence)):
				all_train_sentence[i] = all_train_sentence[i].replace(word, '<unk>')
		else:
			continue
	return s

# preprocess test file to replace <unk> characters
def replaceTestUnknown(all_train_sentence, all_test_sentence, s):
	# traverse doc and put words in set
	for i in range(len(all_test_sentence)):
		char_in_sentence = (re.split('\s+', all_test_sentence[i]))
		for j in range(len(char_in_sentence)):
			if char_in_sentence[j] not in s and char_in_sentence[j]!='<s>' and char_in_sentence[j]!='</s>':
				all_test_sentence[i] = all_test_sentence[i].replace(' '+char_in_sentence[j]+' ', ' <unk> ')

# parse sentence
def preprocessText(train_text, all_train_sentence, all_test_sentence):
	s = set()
	type(s)
	for i in range(len(all_train_sentence)):
		if '<s>' not in all_train_sentence[i]:
			all_train_sentence[i] = '<s> ' + all_train_sentence[i]
		all_train_sentence[i] = all_train_sentence[i].replace('. ', ' </s>').replace('.', ' </s>').replace('!', ' </s>').replace('?', ' </s>').replace('</s> ', ' </s>')
		all_train_sentence[i] = all_train_sentence[i].replace(',', ' ,')
		all_train_sentence[i] = all_train_sentence[i].replace('  ,', ' ,')

	for j in range(len(all_test_sentence)):
		all_test_sentence[j] = all_test_sentence[j].replace('</s> ', '</s>')

	s = replaceUnknown(train_text, all_train_sentence, 1)
	return s



