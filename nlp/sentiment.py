import os
import csv
import unicodecsv
import nltk
import operator
import codecs
from os.path import dirname, abspath
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

class ReviewAnalyzer:
	ROOT_DIR = dirname(dirname(abspath(__file__)))
	
	def __init__(self):
		pass

	def load_business(self):
		firstline = True
		filepath = os.path.join(self.ROOT_DIR, 'dataset/data_business_ids.csv')

		business_ids = []
		with open(filepath, 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				if firstline:
					firstline = False

				business_id = row[0]
				business_ids.append(business_id)

		return business_ids


	def filter(self):	
		firstline = True
		row_count = 1		
		filepath = os.path.join(self.ROOT_DIR, 'dataset/yelp_academic_dataset_review.csv')
		business_ids = self.load_business()		

		with open(filepath, 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				if firstline: 
					firstline = False
					continue

				print "row #: %d" % row_count
				user_id = row[0]
				review_id = row[1]
				review_text = row[2]
				business_id = row[4]				

				# print review_text
				# print "\n"

				outpath = os.path.join(self.ROOT_DIR, 'dataset/filtered_reviews.csv')
				if business_id in business_ids:
					with open(outpath, 'a') as f_write:
						writer = csv.writer(f_write)
						writer.writerow(row)										
											
				row_count = row_count + 1

	def extractNoun(self):
		firstline = True
		row_count = 1

		filepath = os.path.join(self.ROOT_DIR, 'dataset/large votes reviews.csv')
		word_freq = {}

		with open(filepath, 'rb') as f:		
			reader = unicodecsv.reader(f)
			for row in reader:
				if firstline:
					firstline = False
					continue

				print "row #: %d" % row_count		
				review_text = row[2]
				
				sentences = tokenize.sent_tokenize(review_text)
				for sentence in sentences:
					text = tokenize.word_tokenize(sentence)
					pos_tags = nltk.pos_tag(text)
					for (word, tag) in pos_tags:
						if tag == 'NN':
							if word in word_freq:
								word_freq[word] = word_freq[word] + 1
							else:
								word_freq[word] = 1

				row_count = row_count + 1
				# if row_count > 5:
				# 	break

		self.writeWordFreq(word_freq)

	def writeWordFreq(self, word_freq):
		sorted_list = sorted(word_freq.items(), key=operator.itemgetter(1), reverse = True)
		# print sorted_list
		with open('word_freq.csv', 'a')	as f:
			writer = csv.writer(f)
			for (word, freq) in sorted_list:
				writer.writerow(["%s, %d" % (word, freq)])
		
				
ReviewAnalyzer().extractNoun()