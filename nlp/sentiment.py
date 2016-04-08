import os
import csv
import unicodecsv
import nltk
import operator
import codecs
import classifier
import numpy as np
from os.path import dirname, abspath
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from nltk.corpus import wordnet as wn

class ReviewAnalyzer:
	ROOT_DIR = dirname(dirname(abspath(__file__)))
	
	def __init__(self):
		pass	

	# loading the selected business IDs
	def load_business(self):
		firstline = True
		filepath = os.path.join(self.ROOT_DIR, 'dataset/phoenix_restaurants_business.csv')

		business_ids = []
		with open(filepath, 'rb') as f:
			reader = csv.reader(f)
			for row in reader:
				if firstline:
					firstline = False

				business_id = row[0]
				business_ids.append(business_id)

		return business_ids

	# filter the review data based on the selected business IDs
	def filter(self):	
		firstline = True
		row_count = 1		
		filepath = os.path.join(self.ROOT_DIR, 'dataset/yelp_academic_dataset_review.csv')
		business_ids = set(self.load_business())		

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

	# extract nouns based on the Part-of-Speech tags
	def extract_noun(self):
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
				tokens = nltk.wordpunct_tokenize(review_text)
				pos_tags = nltk.pos_tag(tokens)
				print pos_tags

				for sentence in sentences:
					text = tokenize.word_tokenize(sentence)
					pos_tags = nltk.pos_tag(text)
					print pos_tags
					for (word, tag) in pos_tags:
						if tag == 'NN':
							if word in word_freq:
								word_freq[word] = word_freq[word] + 1
							else:
								word_freq[word] = 1

				row_count = row_count + 1

		self.write_word_freq(word_freq)

	def write_word_freq(self, word_freq):
		sorted_list = sorted(word_freq.items(), key=operator.itemgetter(1), reverse = True)
		# print sorted_list
		with open('word_freq.csv', 'a')	as f:
			writer = unicodecsv.writer(f)
			for (word, freq) in sorted_list:
				writer.writerow([word, freq])

	# extract bigrams and trigrams
	def process_review(self, clf_food, clf_service, clf_ambiance, clf_price):
		firstline = True
		row_count = 1

		filepath = os.path.join(self.ROOT_DIR, 'dataset/filtered_reviews.csv')
		file_results = os.path.join(self.ROOT_DIR, 'dataset/processed_reviews.csv')
		with open(file_results, 'a') as f_write:
			writer = csv.writer(f_write)
			writer.writerow(['review_id','user_id','business_id','votes_cool','votes_funny','votes_useful','rating','IsFoodGood','IsServiceGood','IsAmbianceGood','IsPriceGood', \
				'vader_compound', 'vader_neg', 'vader_neu', 'vader_pos'])

		features = self.load_features()
		feature_set = set(features)		

		sid = SentimentIntensityAnalyzer()
		
		with open(filepath, 'rb') as f:		
			reader = unicodecsv.reader(f)
			for row in reader:
				if firstline:
					firstline = False
					continue

				print "row #: %d" % row_count						
				user_id = row[0]
				review_id = row[1]
				review_text = row[2]
				votes_cool = row[3]
				business_id = row[4]				
				votes_funny = row[5]
				rating = row[6]
				date = row[7]
				votes_useful = row[9]				
				
				# print review_text
				compound = 0.0
				neg = 0.0
				neu = 0.0
				pos = 0.0
				sent_count = 0
				sentences = tokenize.sent_tokenize(review_text)
				for sentence in sentences:
					ss = sid.polarity_scores(sentence)
					# for k in sorted(ss):
					# 	print '{0}: {1}, '.format(k, ss[k])									
					compound = compound + ss['compound']
					neg = neg + ss['neg']
					neu = neu + ss['neu']
					pos = pos + ss['pos']
					sent_count = sent_count + 1
				
				avg_compound = compound / sent_count
				avg_neg = neg / sent_count
				avg_neu = neu / sent_count
				avg_pos = pos / sent_count

				tokens = nltk.wordpunct_tokenize(review_text)				
				unigrams = set(tokens)				
				bigrams = set(nltk.bigrams(tokens))
				trigrams = set(nltk.trigrams(tokens))
				
				# look up whether the n-gram feature in the review				
				match_features = []
				match_features.extend(self.match_ngrams(unigrams, feature_set))
				match_features.extend(self.match_ngrams(bigrams, feature_set))
				match_features.extend(self.match_ngrams(trigrams, feature_set))

				X = self.construct_feature_array(features, match_features)
				X = np.reshape(X, (1, -1))

				# print match_features				
				
				food_good = clf_food.predict(X)
				service_good = clf_service.predict(X)
				ambiance_good = clf_ambiance.predict(X)				
				price_good = clf_price.predict(X)
				# print [food_good[0], service_good[0], ambiance_good[0], price_good[0]]

				with open(file_results, 'a') as f_write:
					writer = csv.writer(f_write)
					writer.writerow([review_id, user_id, business_id, votes_cool, votes_funny, votes_useful, rating, food_good[0], service_good[0], ambiance_good[0], price_good[0], \
						avg_compound, avg_neg, avg_neu, avg_pos])
				
				# print "\n"
				row_count = row_count + 1
				# if row_count > 10:
				# 	break

	def construct_feature_array(self, features, match_features):
		matches = set(match_features)

		# initialize an all 0 array
		X = np.zeros(len(features))
		for i in range(len(features)):
			if features[i] in matches:
				X[i] = 1

		return X

	def match_ngrams(self, ngrams, features):
		res = []
		for n_gram in ngrams:
			if n_gram in features:
				res.append(n_gram)				
		return res

	def load_features(self):
		filepath = os.path.join(self.ROOT_DIR, 'nlp', 'features.txt')
		features = []

		f = open(filepath, 'r')
		for line in f:
			word = line.strip('\n')
			features.append(word)

		return features

if __name__ == '__main__':	
	# filter reviews based on the phoenix restaurants business ids
	# ReviewAnalyzer().filter()

	# use classifier to process each review
	labels = {}
	labels['IsFoodGood'] = 0
	labels['IsServiceGood'] = 1
	labels['IsAmbianceGood'] = 2
	# labels['IsDealsGood'] = 3
	labels['IsPriceGood'] = 4	

	params_food = ['linear', 10]
	params_service = ['linear', 1]
	params_ambiance = ['rbf', 10, 0.001]
	# params_deals = ['rbf', 10, 0.001]
	params_price = ['linear', 1]

	rc = classifier.ReviewClassifier()
	clf_food = rc.train(labels['IsFoodGood'], 'food', params_food)
	clf_service = rc.train(labels['IsServiceGood'], 'service', params_service)
	clf_ambiance = rc.train(labels['IsAmbianceGood'], 'ambiance', params_ambiance)	
	clf_price = rc.train(labels['IsPriceGood'], 'price', params_price)					
	ReviewAnalyzer().process_review(clf_food, clf_service, clf_ambiance, clf_price)
