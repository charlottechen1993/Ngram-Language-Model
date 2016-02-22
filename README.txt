Charlotte Chen
Assignment 2: README

--------------------------------
Instruction on running the code:
--------------------------------
To run my program on the sample toy problem, you can type into the command line:
- Ngram.py <1|2|2s|3|3s> <trainfile> <devfile> <testfile>
- Example) Ngram.py 1 train.txt dev.txt test.txt

To run my program on the PART III you can type in 
- python Ngram.py 1 Holmes_Training_Data Holmes.lm_format.questions.txt Holmes.lm_format.questions.txt

-----
Bugs:
-----
My N-gram model works successfully on the sample toy problem without problem regardless of the model I’m choosing. 
However, when my N-gram model is implemented on the Project Gutenberg data, I experienced a lot of sentence parsing issue. My code took a long time to run on the unigram model using only 2 training files. My perplexity per word prints but their values are all the same because I don’t have enough training files and I have sentence parsing problems. My bigram and trigram models takes too long to run so I was unable to get the output

-------------------
Part III Pipeline :
-------------------
I did not use an off-the shelf tokenizer (I wrote my own). As my program enters, I identify whether the second argument is a txt file (Part II) or a directory (Part III). For part III, I wrote a for loop to iterate through all training files in the directory, and for every file I append per sentences into a string called “full_train”, which contains all sentence in all the training files. Then I split the string into a list of sentences parsing by the “\n”. 

For the list of training sentences, I clean them up by dealing with the trailing spaces, commas, periods, and some other special characters. 

Assuming the threshold k=1, I replaced all non-frequent characters with “<unk>”, and stored all unique characters in training file into a set. Using the set, I preprocessed the dev file and test files by replacing characters that doesn’t appear in the set with <unk>

With all the sentences preprocessed,  I ran the Ngram model depending on the users’ choices