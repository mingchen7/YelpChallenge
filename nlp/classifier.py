import numpy as np
import os
import logging
from os.path import dirname, abspath
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import precision_score, recall_score
from sklearn.grid_search import GridSearchCV

class ReviewClassifier:
	ROOT_DIR = dirname(dirname(abspath(__file__)))
	LOG_FILE = 'training history.log'
	
	def __init__(self):
		np.set_printoptions(threshold=1000)
		logging.basicConfig(filename = self.LOG_FILE, level = logging.DEBUG)    
						

	# loading the training and testing data
	def load_data(self):
		filepath = os.path.join(self.ROOT_DIR, 'dataset/nlp classifier/train.csv')
		training = np.loadtxt(open(filepath, "rb"), delimiter = ",", skiprows = 1)

		filepath = os.path.join(self.ROOT_DIR, 'dataset/nlp classifier/test.csv')
		testing = np.loadtxt(open(filepath, "rb"), delimiter = ",", skiprows = 1)

		combined = np.vstack((training, testing))
		data = combined[:,0:668]
		targets = combined[:,668:673]
		return (data, targets)

	# evaluate the model performance using cross validation
	def evaluate(self, label_index, label):
		data, targets = self.load_data()		
				
		parameters = [
			{'C': [1, 10], 'kernel': ['linear']},
			{'C': [1, 10], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
		]
				
		# cross-validation generator
		n_samples = data.shape[0]
		ss = cross_validation.ShuffleSplit(n_samples, n_iter = 5, test_size = 0.2, random_state = 0)					
		for train_index, test_index in ss:
			print("%s %s" % (train_index, test_index))
		
		# grid search
		print "Training models for %s" % label
		logging.debug("Training models for %s" % label)
		estimator = svm.SVC()
		clf = GridSearchCV(estimator, parameters, verbose = 3, cv=ss, n_jobs = 4)
		clf.fit(data, targets[:, label_index])		

		print "Best parameters set found on development set:"    
		print clf.best_params_

		logging.debug("Best parameters set found on development set:")
		logging.debug(clf.best_params_)

		print "\n"
		print "Grid scores on development set:"
		logging.debug("Grid scores on development set:")
		for params, mean_score, scores in clf.grid_scores_:
			print "%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params)
			logging.debug("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std() * 2, params))		

		# scores = cross_validation.cross_val_score(clf, data, targets[:, label], cv = ss)				
		# print ("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


	def train(self, label_index, label, params):
		data, targets = self.load_data()
		X_train, X_test, y_train, y_test = cross_validation.train_test_split(data, targets[:,label_index], test_size = 0.2, random_state = 0)		
		
		print "classifier for %s" % label
		if params[0] == 'linear':
			clf = svm.SVC(kernel = 'linear', C = params[1]).fit(X_train, y_train)
			# print clf.get_params()
		elif params[0] == 'rbf':			
			clf = svm.SVC(kernel = 'rbf', C = params[1], gamma = params[2]).fit(X_train, y_train)		
			# print clf.get_params()
		
		y_pred = clf.predict(X_test)					
		print "Mean accuracy : %0.3f" % clf.score(X_test, y_test)
		print "Precision     : %0.3f" % precision_score(y_test, y_pred)
		print "Recall        : %0.3f" % recall_score(y_test, y_pred)
		return clf



if __name__ == '__main__':	
	labels = {}
	labels['IsFoodGood'] = 0
	labels['IsServiceGood'] = 1
	labels['IsAmbianceGood'] = 2
	labels['IsDealsGood'] = 3
	labels['IsPriceGood'] = 4	

	clf = ReviewClassifier().evaluate(labels['IsPriceGood'], 'price')
	# ReviewClassifier().train()





